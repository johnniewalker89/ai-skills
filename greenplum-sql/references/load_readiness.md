# Load Readiness

Read before designing, reviewing or handing off DDL, load, rebuild, staging or partition-replacement artifacts. Apply the common metadata/SELECT checks in `sql_readiness.md` and the selected workflow/access approvals. These procedures do not authorize writes.

## DDL/load syntax self-review

Before returning Greenplum DDL or load files:

- verify syntax against the expected Greenplum/PostgreSQL compatibility level, not generic modern PostgreSQL;
- verify staging tables have a deliberate storage, distribution, and partition shape for the intended swap/delete/insert mechanics;
- classify `UNLOGGED` tables by owner SQL/job evidence, not by table name. Full-refresh staging may stay `UNLOGGED`; partial-window, incremental, append, or update owner tables should not be `UNLOGGED` unless a recovery contract proves it is safe;
- check that delete/truncate/exchange/swap keys match the declared rebuild grain and cannot leave stale rows;
- for table recreation/copy/rename rollouts, restore owner, comments, and grants from migrator output or `pg_class.relacl`; do not rely only on `information_schema.role_table_grants`;
- mark post-load target checks separately from read-only source checks;
- if self-review finds invalid syntax or incompatible staging shape, fix the artifact before reporting engine-check passed. Sandbox validation should prove runtime/result behavior, not catch issues visible in the final SQL text.
