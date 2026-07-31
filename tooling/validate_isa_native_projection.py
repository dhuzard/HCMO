#!/usr/bin/env python3
"""Validate the native ISA overlap without fabricating an animal Sample.

The accepted HCMO policy treats ISA-JSON and ISA-Tab as controlled-loss
projections.  Their executable overlap is deliberately limited to a genuine
material collection: one animal Source is used to generate one distinct tissue
Sample.  HCMO IRIs are carried as explicit comments because ISA-Tab regenerates
its internal JSON identifiers.
"""
from __future__ import annotations

import io
import json
import logging
import sys
import tempfile
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from rdflib import RDF, Graph, Namespace, URIRef

EXPECTED_ISATOOLS = "0.14.3"
ROOT = Path(__file__).resolve().parent.parent
CANONICAL = ROOT / "examples" / "isa-roundtrip" / "canonical.ttl"
SOURCE_IRI = "https://example.org/hcmo/isa-roundtrip/animal-8"
SAMPLE_IRI = "https://example.org/hcmo/isa-roundtrip/tissue-sample-animal-8"
PROCESS_IRI = "https://example.org/hcmo/isa-roundtrip/process-specimen-collection"
SCHEMA = Namespace("http://schema.org/")
PROV = Namespace("http://www.w3.org/ns/prov#")
BIOSCHEMAS = Namespace("https://bioschemas.org/")


def require_canonical_pattern() -> None:
    """Refuse to test a projection that has drifted from canonical HCMO RDF."""
    graph = Graph().parse(CANONICAL, format="turtle")
    source = URIRef(SOURCE_IRI)
    sample = URIRef(SAMPLE_IRI)
    process = URIRef(PROCESS_IRI)
    required = {
        (source, RDF.type, BIOSCHEMAS.Sample),
        (sample, RDF.type, BIOSCHEMAS.Sample),
        (process, SCHEMA.object, source),
        (process, SCHEMA.result, sample),
        (process, PROV.generated, sample),
        (sample, PROV.wasDerivedFrom, source),
    }
    missing = required - set(graph)
    if missing:
        raise AssertionError(f"canonical Source-to-Sample pattern is incomplete: {sorted(map(str, missing))}")
    if source == sample:
        raise AssertionError("canonical Source and Sample identities were conflated")


def validate_json(stream, label: str) -> None:
    from isatools import isajson

    report = isajson.validate(stream, log_level=logging.ERROR)
    if report["errors"]:
        raise AssertionError(f"{label} ISA-JSON errors: {report['errors']}")
    allowed_warning = {
        "message": "Protocol parameter declared in a protocol but never used",
        "supplemental": "protocol declared ['#parameter/Array_Design_REF'] are not used",
        "code": 1020,
    }
    unexpected = [warning for warning in report.get("warnings", []) if warning != allowed_warning]
    if unexpected:
        raise AssertionError(f"{label} ISA-JSON unexpected warnings: {unexpected}")


def hcmo_iri(comments) -> str | None:
    values = [comment.value for comment in comments if comment.name == "HCMO IRI"]
    if len(values) > 1:
        raise AssertionError(f"multiple HCMO IRI comments: {values}")
    return values[0] if values else None


def assert_returned_semantics(investigation) -> None:
    if len(investigation.studies) != 1:
        raise AssertionError("projection must contain exactly one Study")
    study = investigation.studies[0]
    if len(study.sources) != 1 or len(study.samples) != 1:
        raise AssertionError("projection must contain exactly one Source and one genuine Sample")
    source = study.sources[0]
    sample = study.samples[0]
    if source is sample:
        raise AssertionError("returned Source and Sample were conflated")
    if hcmo_iri(source.comments) != SOURCE_IRI:
        raise AssertionError("Source HCMO IRI did not survive the ISA-Tab round trip")
    if hcmo_iri(sample.comments) != SAMPLE_IRI:
        raise AssertionError("Sample HCMO IRI did not survive the ISA-Tab round trip")
    if len(sample.derives_from) != 1 or hcmo_iri(sample.derives_from[0].comments) != SOURCE_IRI:
        raise AssertionError("Sample-to-Source derivation did not survive")
    if len(study.process_sequence) != 1:
        raise AssertionError("projection must contain exactly one collection Process")
    if len(study.protocols) != 1:
        raise AssertionError("projection must contain exactly one collection Protocol")
    protocol = study.protocols[0]
    if protocol.name != "sample collection":
        raise AssertionError("sample-collection Protocol name did not survive")
    if protocol.protocol_type is None or protocol.protocol_type.term != "sample collection":
        raise AssertionError("sample-collection Protocol type did not survive")
    process = study.process_sequence[0]
    if process.executes_protocol is None or process.executes_protocol.name != protocol.name:
        raise AssertionError("collection Process no longer executes the collection Protocol")
    if len(process.inputs) != 1 or hcmo_iri(process.inputs[0].comments) != SOURCE_IRI:
        raise AssertionError("collection Process input is not the Source")
    if len(process.outputs) != 1 or hcmo_iri(process.outputs[0].comments) != SAMPLE_IRI:
        raise AssertionError("collection Process output is not the genuine Sample")


def main() -> int:
    try:
        installed = version("isatools")
    except PackageNotFoundError:
        print("[FAIL] isatools is not installed; install tooling/interoperability-requirements.txt")
        return 1
    if installed != EXPECTED_ISATOOLS:
        print(f"[FAIL] isatools {installed} installed; expected {EXPECTED_ISATOOLS}")
        return 1

    from isatools import isajson, isatab
    from isatools.convert import isatab2json, json2isatab
    from isatools.isajson import ISAJSONEncoder
    from isatools.model import (
        Comment,
        Investigation,
        OntologyAnnotation,
        Process,
        Protocol,
        Sample,
        Source,
        Study,
    )

    try:
        require_canonical_pattern()
        investigation = Investigation(
            identifier="HCMO-ISA-NATIVE-1",
            title="HCMO native ISA projection",
            description="Native ISA Source-to-Sample overlap only",
            submission_date="2026-07-31",
            public_release_date="2026-07-31",
        )
        study = Study(
            filename="s_hcmo.txt",
            identifier="HCMO-S1",
            title="HCMO specimen-collection projection",
            description="One genuine Source-to-Sample collection",
            submission_date="2026-07-31",
            public_release_date="2026-07-31",
        )
        investigation.studies.append(study)
        source = Source(
            name="animal-8",
            comments=[Comment(name="HCMO IRI", value=SOURCE_IRI)],
        )
        sample = Sample(
            name="tissue specimen animal 8",
            derives_from=[source],
            comments=[Comment(name="HCMO IRI", value=SAMPLE_IRI)],
        )
        study.sources.append(source)
        study.samples.append(sample)
        protocol = Protocol(
            name="sample collection",
            protocol_type=OntologyAnnotation(term="sample collection"),
        )
        study.protocols.append(protocol)
        study.process_sequence.append(
            Process(
                name="sample collection",
                executes_protocol=protocol,
                inputs=[source],
                outputs=[sample],
            )
        )

        with tempfile.TemporaryDirectory(prefix="hcmo-native-isa-") as tmp:
            root = Path(tmp)
            json_path = root / "isa.json"
            tab_dir = root / "isatab"
            tab_dir.mkdir()
            json_path.write_text(
                json.dumps(investigation, cls=ISAJSONEncoder, sort_keys=True, indent=2),
                encoding="utf-8",
            )
            with json_path.open(encoding="utf-8") as stream:
                validate_json(stream, "initial")
            with json_path.open(encoding="utf-8") as stream:
                json2isatab.convert(stream, str(tab_dir), validate_first=True)
            investigation_path = tab_dir / "i_investigation.txt"
            with investigation_path.open(encoding="utf-8") as stream:
                tab_report = isatab.validate(stream, log_level=logging.ERROR)
            if tab_report["errors"]:
                raise AssertionError(f"ISA-Tab errors: {tab_report['errors']}")
            returned_dict = isatab2json.convert(str(tab_dir), validate_first=True, use_new_parser=True)
            if returned_dict is None:
                raise AssertionError("ISA-Tab-to-ISA-JSON conversion returned no document")
            returned_json = json.dumps(returned_dict)
            validate_json(io.StringIO(returned_json), "returned")
            returned = isajson.load(io.StringIO(returned_json))
            assert_returned_semantics(returned)
    except Exception as exc:  # noqa: BLE001
        print(f"[FAIL] native ISA-JSON/ISA-Tab projection: {exc}")
        return 1

    print("[OK]   native ISA-JSON validation (pinned isatools 0.14.3)")
    print("[OK]   ISA-JSON -> ISA-Tab -> ISA-JSON Source/Sample projection")
    print("[OK]   stable HCMO identities preserved through explicit ISA comments")
    print("[INFO] housing, direct whole-animal assay, groups, and STATO extensions remain declared losses")
    return 0


if __name__ == "__main__":
    sys.exit(main())
