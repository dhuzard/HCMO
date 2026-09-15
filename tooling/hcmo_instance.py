#!/usr/bin/env python3
"""Shared helpers for generating HCMO instance graphs from HCM-system exports.

Every per-system generator under ``docs/hcm-systems/systems/<slug>/`` builds
its ABox through this module so that all evaluation graphs follow the same
modelling conventions (named QUDT quantity values, OWL-Time intervals with
named instants, time-bounded housing assignments, SOSA observations) and the
same deterministic serialization as ``tooling/build.py``.

The helpers never invent HCMO terms: only IRIs declared in
``ontology/modules/`` or pinned external vocabularies are emitted.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

from rdflib import RDF, RDFS, XSD, Graph, Literal, Namespace, URIRef
from rdflib.compare import to_canonical_graph

ROOT = Path(__file__).resolve().parent.parent

HCM = Namespace("https://w3id.org/hcmo/ontology/hcm#")
HCM_BIO = Namespace("https://w3id.org/hcmo/ontology/hcm/bio#")
HCM_ENV = Namespace("https://w3id.org/hcmo/ontology/hcm/env#")
HCM_OBS = Namespace("https://w3id.org/hcmo/ontology/hcm/obs#")
HCM_TECH = Namespace("https://w3id.org/hcmo/ontology/hcm/tech#")
SOSA = Namespace("http://www.w3.org/ns/sosa/")
TIME = Namespace("http://www.w3.org/2006/time#")
PROV = Namespace("http://www.w3.org/ns/prov#")
QUDT = Namespace("http://qudt.org/schema/qudt/")
UNIT = Namespace("http://qudt.org/vocab/unit/")
SCHEMA = Namespace("https://schema.org/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
SEMTS = Namespace("https://w3id.org/semts/ontology#")

PREFIXES = {
    "hcm": HCM,
    "hcm-bio": HCM_BIO,
    "hcm-env": HCM_ENV,
    "hcm-obs": HCM_OBS,
    "hcm-tech": HCM_TECH,
    "sosa": SOSA,
    "time": TIME,
    "prov": PROV,
    "qudt": QUDT,
    "unit": UNIT,
    "schema": SCHEMA,
    "dcterms": DCTERMS,
    "semts": SEMTS,
    "rdfs": RDFS,
    "xsd": XSD,
}


def xsd_datetime(value: datetime) -> Literal:
    """Serialize an aware datetime as xsd:dateTime keeping its UTC offset."""
    if value.tzinfo is None:
        raise ValueError("datetimes must be timezone-aware")
    return Literal(value.isoformat(), datatype=XSD.dateTime)


def decimal_literal(value) -> Literal:
    """Serialize a number as xsd:decimal without floating-point noise."""
    if isinstance(value, Decimal):
        text = format(value.normalize(), "f")
    else:
        text = format(Decimal(str(value)).normalize(), "f")
    if "." not in text:
        text += ".0"
    return Literal(text, datatype=XSD.decimal)


class InstanceGraph:
    """A small builder around :class:`rdflib.Graph` for HCMO ABoxes."""

    def __init__(self, base: str, prefix: str) -> None:
        self.base = Namespace(base)
        self.prefix = prefix
        self.g = Graph()
        for name, namespace in PREFIXES.items():
            self.g.bind(name, namespace, replace=True)
        self.g.bind(prefix, self.base, replace=True)

    # ---------------------------------------------------------------- basics
    def iri(self, local: str) -> URIRef:
        return self.base[local]

    def add(self, s, p, o) -> None:
        self.g.add((s, p, o))

    def typed(self, local: str, *classes: URIRef, label: str | None = None, comment: str | None = None) -> URIRef:
        node = self.iri(local)
        for cls in classes:
            self.add(node, RDF.type, cls)
        if label is not None:
            self.add(node, RDFS.label, Literal(label))
        if comment is not None:
            self.add(node, RDFS.comment, Literal(comment))
        return node

    # ------------------------------------------------------------- quantities
    def quantity(self, local: str, value, unit: URIRef, *extra_types: URIRef) -> URIRef:
        """A named ``qudt:QuantityValue`` (optionally also an HCMO result class)."""
        node = self.typed(local, QUDT.QuantityValue, *extra_types)
        self.add(node, QUDT.numericValue, decimal_literal(value))
        self.add(node, QUDT.hasUnit, unit)
        return node

    def result_quantity(self, local: str, value, unit: URIRef) -> URIRef:
        """An observation result typed ``hcm-obs:QuantityValue``."""
        return self.quantity(local, value, unit, HCM_OBS.QuantityValue)

    # --------------------------------------------------------------- temporal
    def instant(self, local: str, when: datetime) -> URIRef:
        node = self.typed(local, TIME.Instant)
        self.add(node, TIME.inXSDDateTime, xsd_datetime(when))
        return node

    def interval(
        self,
        local: str,
        start: datetime,
        end: datetime,
        *,
        duration_unit: URIRef | None = None,
    ) -> URIRef:
        """A bounded ``time:Interval`` with named beginning/end instants.

        When ``duration_unit`` is ``time:unitHour`` or ``time:unitMinute`` the
        ``time:numericDuration``/``time:unitType`` pair is asserted as well.
        """
        if end <= start:
            raise ValueError(f"interval {local} must end after it starts")
        node = self.typed(local, TIME.Interval)
        self.add(node, TIME.hasBeginning, self.instant(f"{local}-begin", start))
        self.add(node, TIME.hasEnd, self.instant(f"{local}-end", end))
        if duration_unit is not None:
            seconds = (end - start).total_seconds()
            divisor = {TIME.unitHour: 3600, TIME.unitMinute: 60, TIME.unitSecond: 1, TIME.unitDay: 86400}[duration_unit]
            self.add(node, TIME.numericDuration, decimal_literal(Decimal(seconds) / Decimal(divisor)))
            self.add(node, TIME.unitType, duration_unit)
        return node

    # -------------------------------------------------------------- enclosure
    def dimensions(self, local: str, width_cm, length_cm, height_cm) -> URIRef:
        node = self.typed(local, HCM.EnclosureDimensions)
        self.add(node, HCM.hasWidthQuantity, self.quantity(f"{local}-width", width_cm, UNIT.CentiM))
        self.add(node, HCM.hasLengthQuantity, self.quantity(f"{local}-length", length_cm, UNIT.CentiM))
        self.add(node, HCM.hasHeightQuantity, self.quantity(f"{local}-height", height_cm, UNIT.CentiM))
        return node

    def enclosure(
        self,
        local: str,
        *,
        label: str,
        identifier: str,
        dimensions: URIRef,
        manufacturer: str | None = None,
        comment: str | None = None,
    ) -> URIRef:
        node = self.typed(local, HCM.MonitoredEnclosure, label=label, comment=comment)
        self.add(node, HCM.hasEnclosureIdentifier, Literal(identifier))
        self.add(node, HCM.hasDimensions, dimensions)
        if manufacturer:
            self.add(node, HCM.hasManufacturer, Literal(manufacturer))
        return node

    def enrichment(self, local: str, enrichment_type: str, label: str) -> URIRef:
        node = self.typed(local, HCM.Enrichment, label=label)
        self.add(node, HCM.hasEnrichmentType, Literal(enrichment_type))
        return node

    def light_cycle(
        self,
        local: str,
        *,
        dark_start: str,
        dark_hours: int,
        light_hours: int,
        label: str,
    ) -> URIRef:
        node = self.typed(local, HCM_ENV.LightCycle, label=label)
        self.add(node, HCM_ENV.hasDarkPhaseStart, Literal(dark_start, datatype=XSD.time))
        self.add(node, HCM_ENV.hasDarkPhaseDuration, Literal(f"PT{dark_hours}H", datatype=XSD.duration))
        self.add(node, HCM_ENV.hasLightPhaseDuration, Literal(f"PT{light_hours}H", datatype=XSD.duration))
        return node

    def environmental_property(self, local: str, label: str) -> URIRef:
        return self.typed(local, HCM_ENV.EnvironmentalProperty, label=label)

    def observable_property(self, local: str, label: str) -> URIRef:
        return self.typed(local, SOSA.ObservableProperty, label=label)

    def measurement_spec(self, local: str, prop: URIRef, value, unit: URIRef, label: str) -> URIRef:
        node = self.typed(local, HCM_ENV.MeasurementSpecification, label=label)
        self.add(node, HCM_ENV.specifiesProperty, prop)
        self.add(node, HCM_ENV.hasSpecifiedValue, self.quantity(f"{local}-value", value, unit))
        return node

    def environment_profile(self, local: str, *, label: str, light_cycle: URIRef | None = None, specs: list[URIRef] = ()) -> URIRef:
        node = self.typed(local, HCM_ENV.EnvironmentProfile, label=label)
        if light_cycle is not None:
            self.add(node, HCM_ENV.hasLightCycle, light_cycle)
        for spec in specs:
            self.add(node, HCM_ENV.hasMeasurementSpec, spec)
        return node

    # ---------------------------------------------------------------- biology
    def subject(
        self,
        local: str,
        *,
        label: str,
        species: str,
        strain: str | None = None,
        sex: str | None = None,
        date_of_birth: str | None = None,
        group: URIRef | None = None,
    ) -> URIRef:
        node = self.typed(local, HCM_BIO.Subject, label=label)
        self.add(node, HCM_BIO.hasSpecies, Literal(species))
        if strain:
            self.add(node, HCM_BIO.hasStrain, Literal(strain))
        if sex:
            self.add(node, HCM_BIO.hasBiologicalSex, Literal(sex))
        if date_of_birth:
            self.add(node, HCM_BIO.hasDateOfBirth, Literal(date_of_birth, datatype=XSD.date))
        if group is not None:
            self.add(node, HCM_BIO.belongsToGroup, group)
            self.add(group, HCM_BIO.hasMember, node)
        return node

    def group(self, local: str, *, label: str, comment: str | None = None) -> URIRef:
        return self.typed(local, HCM_BIO.ExperimentalGroup, label=label, comment=comment)

    def housing(self, local: str, *, holder: URIRef, enclosure: URIRef, start: datetime, end: datetime) -> URIRef:
        """A time-bounded ``hcm-bio:HousingAssignment`` for a subject or group."""
        node = self.typed(local, HCM_BIO.HousingAssignment)
        self.add(holder, HCM_BIO.hasHousingAssignment, node)
        self.add(node, HCM_BIO.assignedToEnclosure, enclosure)
        self.add(node, TIME.hasTime, self.interval(f"{local}-validity", start, end))
        return node

    # -------------------------------------------------------------- technical
    def sensor(
        self,
        local: str,
        *,
        label: str,
        identifier: str,
        technology: str | None = None,
        sensor_type: str | None = None,
        model_number: str | None = None,
        sampling_rate_hz=None,
        installed_in: URIRef | None = None,
        captures: list[URIRef] = (),
    ) -> URIRef:
        node = self.typed(local, HCM_TECH.Sensor, label=label)
        self.add(node, HCM_TECH.hasSensorIdentifier, Literal(identifier))
        if technology:
            self.add(node, HCM_TECH.hasSensorTechnology, Literal(technology))
        if sensor_type:
            self.add(node, HCM_TECH.hasSensorType, Literal(sensor_type))
        if model_number:
            self.add(node, HCM_TECH.hasModelNumber, Literal(model_number))
        if sampling_rate_hz is not None:
            self.add(node, HCM_TECH.hasSamplingRateQuantity, self.quantity(f"{local}-sampling-rate", sampling_rate_hz, UNIT.HZ))
        if installed_in is not None:
            self.add(node, HCM_TECH.installedIn, installed_in)
            self.add(installed_in, HCM_TECH.monitoredBy, node)
        for prop in captures:
            self.add(node, HCM_TECH.captures, prop)
        return node

    def actuator(self, local: str, *, label: str, enclosure: URIRef, model_number: str | None = None) -> URIRef:
        node = self.typed(local, HCM_TECH.Actuator, label=label)
        self.add(enclosure, HCM_TECH.hasActuator, node)
        if model_number:
            self.add(node, HCM_TECH.hasModelNumber, Literal(model_number))
        return node

    def hardware(self, local: str, *, label: str, model_number: str | None = None, firmware: str | None = None) -> URIRef:
        node = self.typed(local, HCM_TECH.Hardware, label=label)
        if model_number:
            self.add(node, HCM_TECH.hasModelNumber, Literal(model_number))
        if firmware:
            self.add(node, HCM_TECH.hasFirmware, Literal(firmware))
        return node

    def software(self, local: str, *, label: str, version: str | None = None, runs_on: URIRef | None = None) -> URIRef:
        node = self.typed(local, HCM_TECH.Software, label=label)
        if version:
            self.add(node, HCM_TECH.hasVersion, Literal(version))
        if runs_on is not None:
            self.add(node, HCM_TECH.runsOn, runs_on)
        return node

    def time_series(
        self,
        local: str,
        *,
        label: str,
        file_format: str,
        storage_path: str,
        sampling_rate_hz=None,
        generated_by: URIRef | None = None,
        comment: str | None = None,
    ) -> URIRef:
        node = self.typed(local, HCM_TECH.TimeSeries, label=label, comment=comment)
        self.add(node, HCM_TECH.hasFileFormat, Literal(file_format))
        self.add(node, HCM_TECH.hasStoragePath, Literal(storage_path))
        if sampling_rate_hz is not None:
            self.add(node, HCM_TECH.hasSamplingRateQuantity, self.quantity(f"{local}-sampling-rate", sampling_rate_hz, UNIT.HZ))
        if generated_by is not None:
            self.add(node, PROV.wasGeneratedBy, generated_by)
        return node

    # ------------------------------------------------------------ observation
    def observation(
        self,
        local: str,
        *,
        cls: URIRef,
        feature: URIRef,
        sensor: URIRef,
        prop: URIRef,
        result: URIRef,
        phenomenon_time: URIRef,
        occurs_in: URIRef | None = None,
        condition: URIRef | None = None,
        procedure: URIRef | None = None,
    ) -> URIRef:
        """A SOSA observation; ``cls`` is ``sosa:Observation`` or an HCMO subtype."""
        node = self.typed(local, cls)
        self.add(node, SOSA.hasFeatureOfInterest, feature)
        self.add(node, SOSA.madeBySensor, sensor)
        self.add(node, SOSA.observedProperty, prop)
        self.add(node, SOSA.hasResult, result)
        self.add(node, SOSA.phenomenonTime, phenomenon_time)
        if occurs_in is not None:
            self.add(node, HCM_OBS.occursIn, occurs_in)
        if condition is not None:
            self.add(node, HCM_OBS.hasCondition, condition)
        if procedure is not None:
            self.add(node, SOSA.usedProcedure, procedure)
        return node

    def behavior_result(self, local: str, behavior_type: str, confidence=None) -> URIRef:
        node = self.typed(local, HCM_OBS.BehaviorResult)
        self.add(node, HCM_OBS.hasBehaviorType, Literal(behavior_type))
        if confidence is not None:
            self.add(node, HCM_OBS.hasConfidenceScore, decimal_literal(confidence))
        return node

    def categorical_result(self, local: str, category: str) -> URIRef:
        node = self.typed(local, HCM_OBS.CategoricalResult)
        self.add(node, HCM_OBS.hasCategory, Literal(category))
        return node

    # ------------------------------------------------------------ provenance
    def dataset_note(
        self,
        local: str,
        *,
        label: str,
        description: str,
        source: str,
        real_data: bool,
    ) -> URIRef:
        """A ``schema:Dataset`` node stating where the instance data came from.

        ``real_data`` distinguishes a graph derived from a genuine vendor export
        from one derived from a schema-faithful synthetic export.
        """
        node = self.typed(local, SCHEMA.Dataset, PROV.Entity, label=label)
        self.add(node, SCHEMA.description, Literal(description))
        self.add(node, DCTERMS.source, Literal(source))
        self.add(node, DCTERMS.type, Literal("real export" if real_data else "synthetic schema-faithful export"))
        return node

    # ---------------------------------------------------------- serialization
    def serialize(self, path: Path, header: str) -> None:
        canon = Graph()
        for triple in sorted(to_canonical_graph(self.g), key=lambda t: (str(t[0]), str(t[1]), str(t[2]))):
            canon.add(triple)
        for name, namespace in PREFIXES.items():
            canon.bind(name, namespace, replace=True)
        canon.bind(self.prefix, self.base, replace=True)
        text = header + canon.serialize(format="turtle")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")


def minutes(start: datetime, count: int, step: int = 1):
    """Yield ``count`` consecutive bin start times ``step`` minutes apart."""
    for index in range(count):
        yield start + timedelta(minutes=index * step)
