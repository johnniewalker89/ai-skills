# Data Artifact Decisions

Read for new production-like marts/models when material source, grain, refresh,
attribution or proof choices remain unresolved. Use bounded supplied/repo/catalog
evidence to make a concrete proposal before asking a business question or requesting
a required operation. Preserve already accepted decisions and authorization.

Record, proportionally in the requested artifact or active task context:
- selected sources and material rejected alternatives;
- driving/output grain, join semantics and ownership of independent facts;
- refresh/reprocessing and attribution/window semantics, including mutable sources;
- unresolved business decisions with recommended defaults and their consequence;
- expected SQL/DDL/build artifacts and their requested destination;
- existing proof, planned checks, comparison surface/window and acceptance criteria;
- what read-only proves, what remains unproven and the trigger for sandbox proof;
- exact operational stop-points, targets and cleanup/rollback when relevant.

Do not create context files solely because this checklist exists. A supplied-evidence
review can record needed conclusions in its answer. For large artifacts, retain
detailed evidence in an agreed report and summarize decisions/limits in chat.

Concrete live sandbox approval follows the selected operational owner: contour,
action, target set and cleanup/rollback scope. Test schemas and temporary objects
are still writes. Safe read-only discovery or an already authorized source change
does not need another approval because the task is called a project.

Source/DDL/query creation does not prove live result correctness. Use
data_artifact_proof.md for exact comparison scope, applicability and final SQL claims.
