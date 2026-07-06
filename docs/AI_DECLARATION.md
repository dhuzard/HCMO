> Status: AI-assisted draft generated from repository structure and metadata. Requires human review before being treated as authoritative.

# AI Declaration

AI-assistance declaration for **dhuzard/HCMO**.

## Scope

This declaration covers the use of AI/LLM tools in producing the code,
documentation, tests, analyses, and generated artefacts in this repository. It
states what was AI-assisted, who is responsible, and what risks apply.

## AI tools used

<!-- Be specific: tool, version/model, and where it was applied. -->
- Tool / model — used for (code / docs / tests / data wrangling / review)
- (If none: "No AI tools were used in this project.")

## Type of AI assistance

- [ ] Code generation / autocompletion
- [ ] Refactoring / code review suggestions
- [ ] Documentation drafting
- [ ] Test generation
- [ ] Data cleaning / transformation
- [ ] Literature / background summarisation
- [ ] Other: <describe>

## Human responsibility

A named human is responsible for every AI-assisted output. AI output was
reviewed by a human before being committed and is not treated as authoritative
on its own.

- Responsible reviewer(s): <name / ORCID>
- Review method: <PR review / test execution / manual verification>

## Non-delegated decisions

The following decisions were **not** delegated to AI and were made by humans:

- Scientific assumptions and study design
- Interpretation of results and conclusions
- Choice of statistical methods and their validity
- Handling of sensitive / personal data
- Licensing and attribution decisions

## Known AI-related risks

We explicitly acknowledge the following risks of AI-assisted work and how we
mitigate them:

- **Hallucinated dependencies** — imports/packages that do not exist or are
  wrong (mitigation: dependency pinning + install/test in CI).
- **Incorrect scientific assumptions** — plausible-sounding but wrong domain
  logic (mitigation: human domain review).
- **Silent changes to analysis logic** — subtle behavioural changes during
  refactors (mitigation: tests + diff review).
- **Overconfident documentation** — docs that overstate validation or maturity
  (mitigation: `TRUST.md` + `LIMITATIONS.md`).
- **Security/privacy leakage** — secrets or personal data exposed in prompts or
  outputs (mitigation: secret scanning, no secrets in prompts).
- **Unverified generated tests** — tests that pass but assert the wrong thing
  (mitigation: review tests as carefully as code).

## Review checklist

- [ ] Every AI-assisted change has a human reviewer of record
- [ ] Dependencies verified to exist and resolve
- [ ] Analysis/logic changes covered by tests
- [ ] No secrets or personal data were shared with AI tools
- [ ] Documentation claims match actual validation status
- [ ] Generated tests independently reviewed
- Last human review: <date> by <name>
