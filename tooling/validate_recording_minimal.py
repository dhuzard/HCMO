"""Offline validation of HCM Recording Minimal v1 cases and pinned inputs."""
import argparse
import datetime
import hashlib
import json
import math
from pathlib import Path
import re
import sys

import yaml
from rdflib import Graph, Namespace, RDF, URIRef
from rdflib.namespace import OWL

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / 'profiles/hcm-recording-minimal/v1'
SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')


def load_contract():
    contract = yaml.safe_load((PROFILE / 'field-contract.yaml').read_text(encoding='utf-8'))
    graphs = {}
    for name, source in contract['sources'].items():
        data = (ROOT / source['path']).read_bytes()
        if hashlib.sha256(data).hexdigest() != source['sha256']:
            raise ValueError(f'source digest mismatch: {name}')
        if name in ('modality', 'technology'):
            graphs[name] = Graph().parse(data=data, format='turtle')
    for name, spec in contract['fields'].items():
        policy = spec['policy']
        if 'scheme' in policy:
            graph = graphs[policy['source']]
            members = {str(s) for s in graph.subjects(SKOS.inScheme, URIRef(policy['scheme']))
                       if (s, RDF.type, SKOS.Concept) in graph and
                       (s, OWL.deprecated, None) not in graph}
            if set(policy['allowed']) != members:
                raise ValueError(f'allowed set differs from pinned scheme: {name}')
    return contract, graphs


def validate(case, contract, graphs):
    errors = []
    fields = contract['fields']
    if not isinstance(case, dict):
        return ['case must be an object']
    for key in case.keys() - fields.keys():
        errors.append(f'unknown field: {key}')
    for key, spec in fields.items():
        if key not in case:
            if spec['min_count']:
                errors.append(f'missing {key}')
            continue
        value, kind, policy = case[key], spec['value_type'], spec['policy']
        if kind in ('string', 'date', 'time', 'duration'):
            if not isinstance(value, str) or not value.strip():
                errors.append(f'{key}: expected nonempty string')
                continue
            try:
                if kind == 'date':
                    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value): raise ValueError('date')
                    datetime.date.fromisoformat(value)
                if kind == 'time':
                    match = re.fullmatch(r'(\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?(Z|[+-]\d{2}:\d{2})?', value)
                    if not match: raise ValueError('time')
                    hour, minute, second = map(int, match.group(1, 2, 3))
                    if hour > 23 or minute > 59 or second > 59: raise ValueError('time')
                    zone = match.group(5)
                    if zone and zone != 'Z':
                        zh, zm = map(int, zone[1:].split(':'))
                        if zh > 14 or zm > 59 or (zh == 14 and zm != 0): raise ValueError('timezone')
                if kind == 'duration' and (not re.fullmatch(r'P(?=\d|T\d)(?:\d+D)?(?:T(?=\d)(?:\d+H)?(?:\d+M)?(?:\d+(?:\.\d+)?S)?)?', value) or value.endswith('T')):
                    raise ValueError('duration')
            except ValueError:
                errors.append(f'{key}: invalid {kind}')
        elif kind == 'quantity':
            if not isinstance(value, dict) or set(value) != {'numeric_value', 'unit'}:
                errors.append(f'{key}: expected numeric_value and unit')
            elif (isinstance(value['numeric_value'], bool) or not isinstance(value['numeric_value'], (float, int))
                  or (isinstance(value['numeric_value'], float) and not math.isfinite(value['numeric_value'])) or value['numeric_value'] <= 0
                  or value['unit'] not in policy['allowed_units']):
                errors.append(f'{key}: invalid value or unit')
        elif kind == 'mapping':
            if not isinstance(value, dict) or set(value) != {'source_value', 'status', 'iri', 'evidence', 'reviewer', 'alternatives', 'evidence_facts'}:
                errors.append(f'{key}: invalid mapping record')
                continue
            if not isinstance(value['source_value'], str) or not value['source_value'].strip() or not isinstance(value['alternatives'], list) or any(not isinstance(a, str) or not a for a in value['alternatives']):
                errors.append(f'{key}: invalid source or alternatives')
            if key == 'taxon' and value['source_value'] != case.get('species'):
                errors.append('taxon: source must match species exactly')
            if key == 'sensor_technology' and value['source_value'] != case.get('sensor_technology_raw'):
                errors.append('sensor_technology: source must match raw technology exactly')
            if not isinstance(value['evidence_facts'], list) or any(not isinstance(a, str) or not a for a in value['evidence_facts']):
                errors.append(f'{key}: invalid evidence facts')
            if value['evidence'] is not None and not isinstance(value['evidence'], str):
                errors.append(f'{key}: invalid evidence')
            if value['status'] in ('unresolved', 'needs_review'):
                if value['iri'] is not None or value['reviewer'] is not None:
                    errors.append(f'{key}: unresolved must not assert an IRI or reviewer')
            elif value['status'] == 'reviewed' and key != 'taxon':
                iri = value['iri']
                if not isinstance(iri, str) or iri not in policy['allowed']:
                    errors.append(f'{key}: out-of-policy concept')
                if not isinstance(value['evidence'], str) or not value['evidence'].strip() or not isinstance(value['reviewer'], str) or not value['reviewer'].strip():
                    errors.append(f'{key}: reviewed mapping needs evidence and reviewer')
                required = contract['mapping_record']['reviewed_requirements'].get(key, {})
                facts = required.get(iri, required.get('*', [])) if isinstance(iri, str) else []
                if not isinstance(value['evidence_facts'], list) or any(not isinstance(x, str) for x in value['evidence_facts']) or not set(facts).issubset(value['evidence_facts']):
                    errors.append(f'{key}: missing evidence facts')
            else:
                errors.append(f'{key}: unsupported or unreviewed status')
    return errors


def main():
    contract, graphs = load_contract()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=Path, help='Validate one profile JSON object')
    args = parser.parse_args()
    if args.case:
        errors = validate(json.loads(args.case.read_text(encoding='utf-8')), contract, graphs)
        if errors:
            raise ValueError('\n'.join(errors))
        print('Profile case valid')
        return
    fixtures = json.loads((PROFILE / 'fixtures.json').read_text(encoding='utf-8'))
    failures = []
    for fixture in fixtures:
        errors = validate(fixture['case'], contract, graphs)
        if bool(errors) != (fixture['expect'] == 'invalid'):
            failures.append(f"{fixture['name']}: {errors}")
    if failures:
        raise ValueError('\n'.join(failures))
    print(f"Profile sources and {len(fixtures)} synthetic cases verified offline")

if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
