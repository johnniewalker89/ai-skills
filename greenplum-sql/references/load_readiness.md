# Load Readiness

Read before designing, reviewing or handing off DDL, load, rebuild, staging or partition-replacement artifacts. Apply the common metadata/SELECT checks in `sql_readiness.md` and the selected workflow/access approvals. These procedures do not authorize writes.

## DDL/load syntax self-review

Before returning Greenplum DDL or load files:

- verify the complete final statement against the target Greenplum version and
  actual execution path; use a proven project form or version-matched syntax,
  not generic modern PostgreSQL. In CTAS, distribution follows the AS query;
  do not transpose clauses from typed CREATE TABLE
  ([Greenplum 6 syntax](https://docs-cn.greenplum.org/v6/ref_guide/sql_commands/CREATE_TABLE_AS.html));
- verify staging tables have a deliberate storage, distribution, and partition shape for the intended swap/delete/insert mechanics;
- classify `UNLOGGED` tables by owner SQL/job evidence, not by table name. Full-refresh staging may stay `UNLOGGED`; partial-window, incremental, append, or update owner tables should not be `UNLOGGED` unless a recovery contract proves it is safe;
- check that delete/truncate/exchange/swap keys match the declared rebuild grain and cannot leave stale rows;
- for table recreation/copy/rename rollouts, compare the complete before/after
  contract: columns/types/precision/nullability/defaults, owner, table/column
  comments, grants/grant options, distribution, storage and partition topology.
  Derive ACL from migrator output or `pg_class.relacl`, not only
  `information_schema.role_table_grants`; preserve privileges such as TRUNCATE
  and REFERENCES as well as SELECT/INSERT/UPDATE/DELETE. Merely printing catalog
  rows is not a comparison. Refresh saved migration files after a manual repair;
- mark post-load target checks separately from read-only source checks;
- if self-review finds invalid syntax or incompatible staging shape, fix the artifact before reporting engine-check passed. Sandbox validation should prove runtime/result behavior, not catch issues visible in the final SQL text.

## Partition maintenance and execution

Choose whether retention removes partition data or also changes the declared
partition topology. A schema checker may require empty partitions to remain;
in that contract use the appropriate truncate operation, not a drop that the
next schema check will undo or reject. Do not generalize this to all retention.

Check the exact legacy partition selector grammar and rerun behavior on the
target version. `IF EXISTS` is not proof that every `FOR (...)` form tolerates
an absent partition. Cover a populated partition, an empty/absent target, and
the same logical-date retry. Calendar guards alone do not make retries safe.

For templated/procedural SQL, inspect the rendered statements from the actual
runner splitter; internal semicolons and leading comments must survive intact.
If dynamic SQL is needed, keep its boundary minimal and quote identifiers/values
correctly. Verify transaction boundaries, including commit before maintenance
that cannot run inside a transaction. Parser-only proof does not prove DDL
execution, idempotency, or successful target replacement.
