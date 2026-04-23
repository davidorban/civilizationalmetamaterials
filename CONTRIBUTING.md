# Contributing

Thank you for taking an interest in this work.

## How to contribute

### Errata

Found an error in the paper (wrong equation, incorrect value, typo)?
Open an **Errata** issue using the template in `.github/ISSUE_TEMPLATE/errata.md`.
Please include the location (section, equation number, or figure) and the correct version.

### Replication reports

Replicated the model, reproduced a figure, or piloted the trial protocol?
Open a **Replication** issue using the template in `.github/ISSUE_TEMPLATE/replication.md`.
All replication reports — successful or not — are welcome.

### Code fixes and figure scripts

1. Fork the repository and create a branch: `fix/issue-<number>/short-description`.
2. Follow the test-first workflow: write or update tests in `code/tests/` before changing `code/cm/`.
3. Run `pytest` and verify coverage ≥ 90% on `code/cm/`.
4. If you change a figure script, run `python code/figures/figXX_*.py --out figures/figXX-*.pdf`
   and commit the updated PDF alongside the script change.
5. Open a pull request using the template.

### Protocol and experiment scaffolding

Improvements to `experiments/` (protocol, SAP, instruments) are welcome as pull requests.
Keep the "proposed, not registered" framing intact until a partner institution files an IRB application.

## Collaboration on running the trial

If your institution is interested in piloting the stepped-wedge protocol with real grant review
panels, see `COLLABORATION.md` for the contact flow.

## Code of Conduct

This project follows the [Contributor Covenant v2.1](CODE_OF_CONDUCT.md).
