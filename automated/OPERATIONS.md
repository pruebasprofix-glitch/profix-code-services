# Autonomous services

The allowlisted catalogue is processed every 15 minutes by GitHub Actions. No model,
local computer, buyer code execution, or additional Python packages are required.
GitHub schedules may be delayed or disabled after 60 days of repository inactivity;
the public offer uses a 24-hour acceptance window and 2-hour processing allowance,
not a guaranteed 15-minute SLA. Check Actions and re-enable a disabled schedule.

Only seller jobs for IDs in catalogue.json, one unit and the exact listed price
are handled. Existing bespoke services are ignored. Invalid or wholly unreachable
new jobs are declined without payment. Accepted jobs receive a JSON report sealed
by Agent Souk; buyers pay through its wallet-to-wallet flow to reveal it. Producing
a report is not proof of payment. Revenue must be verified separately on-chain.

SOUK_API_KEY belongs in the repository's encrypted Actions secrets only. No wallet
private key is needed by the worker. Job data is sent only to the marketplace;
logs contain counts, opaque job IDs and exception types, not customer URL/report
contents. Public URLs are fetched over HTTPS with DNS/IP validation on every hop.
No confidential or authenticated URLs are supported. Reports are a single observation,
not security certification, rankings, monitoring or remediation.

Recovery: clone this repository, configure SOUK_API_KEY, run the regression tests,
then dispatch services.yml. Source, catalogue and workflow are backed up in Git.
Do not recreate listings: their IDs remain in catalogue.json. To stop accepting
new automated work, pause those listings through the marketplace, then disable the
workflow once accepted jobs are handled. Custom support/revisions needing judgement
require the operator; the worker never fabricates acceptance or sends money.
