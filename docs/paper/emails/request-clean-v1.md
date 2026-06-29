# Email — request the clean V1 artifact from co-authors

**To:** Cyril Gilbert (primary); cc Konstantin Todorov, Pierre Larmande,
Gaoussou Sanou, Serge Sonfack Sounchio, Antoine Toffano
**From:** Damien Huzard
**Subject:** HCMO resource paper — need the clean V1 ontology (source + Turtle) to unblock writing

---

Dear all,

We're preparing an HCMO **Resources Track** paper for **ESWC 2027**, and the
artifact-independent sections are drafted (intro, related work, requirements,
engineering/availability, impact, conclusion, abstract). To finish the two
remaining sections — the **resource description** and the **evaluation** — we need
the **clean version of the ontology** that matches Cyril's report
(modules *bio / housing / env / tech*, ~45 classes / ~46 properties, clean
diagrams).

Important: the version currently committed to the GitHub repo is an **older, raw
Chowlk export** — 143 terms, **no definitions**, and 43 placeholder/erroneous
terms (`UNKNOWN:*`, `ns:Class2`, `xsd:boolean`/`xsd:integer` typed as properties).
It does **not** reflect the model in the report and cannot go in the paper as-is.

**Cyril — could you send the authoritative source behind the report's figures?**
Specifically:

1. The **diagrams.net (.drawio) file(s)** used with Chowlk, and the **exported
   OWL/Turtle** generated from them.
2. Confirmation of the **module structure** (bio / housing / env / tech) and the
   namespaces used.

For the version to be "paper-ready", it should ideally include (or we plan time
to finish together):

- [ ] **No placeholders** — every `UNKNOWN:*` / `ns:Class2` resolved or removed;
      no datatype values mis-typed as properties.
- [ ] **A label + a definition (`rdfs:comment`)** for every class and property.
- [ ] **Reused vocabularies wired in**: SOSA/SSN, OWL-Time, UO, PROV, BFO
      (+ schema.org, semts) with the alignment axioms (subclass/subproperty).
- [ ] The **sensor ≠ observation ≠ result** separation preserved (as in Fig. 11).
- [ ] **Competency-question SPARQL** re-authored against the V1 terms so the six
      questions actually return results (CQ1–CQ6 in the report).
- [ ] **SHACL shapes** and **example data** (one valid, one intentionally invalid)
      updated to the V1 terms.
- [ ] **Confirmed counts** (classes, object/datatype properties, reused terms,
      prefixes) so the paper's numbers are exact.

A few non-artifact items we also need to finalise the submission:

- **Affiliations** for all co-authors, and the **ORCID** confirmations (thanks to
  those who already sent theirs).
- Confirmation of **author order** (Cyril first; Konstantin and Damien as the two
  co-corresponding/contact authors) and **both corresponding-author emails**.
- **Gaoussou** — OK to cite/redraw your KG-querying pipeline figure as *outlook*?
- **Antoine** — same for the ontology-structured-ML figure, if we reference it.

If it's easier, we can do a short call to walk through the model together and lock
the V1. Could you aim to send what you have **by [DATE]**? That keeps us on track
well ahead of the ESWC deadline.

Thanks a lot,
Damien

---

> _Internal note (not for the email): once the V1 lands, it unblocks §4 (Resource
> description), §6 (Evaluation), and the parked questions Q9–Q11 (CQ results,
> OOPS!/FOOPS!/reasoner/SHACL reports, term counts). See `AUDIT.md` and `TODO.md`
> (T0). Fill in [DATE] before sending._
