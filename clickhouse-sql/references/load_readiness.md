# Load Readiness

Read before designing, reviewing or handing off DDL, load, rebuild, staging or partition-replacement artifacts. Apply the common metadata/SELECT checks in `sql_readiness.md` and the selected workflow/access approvals. These procedures do not authorize writes.

## Partition replacement safety

For any build that writes a temp/staging table and swaps data with `REPLACE PARTITION`:

- write staging DDL with an explicit MergeTree-compatible engine, `PARTITION BY`, and `ORDER BY`, or prove that `CREATE TABLE ... AS target` inherits an exactly compatible physical shape on the target ClickHouse version;
- inspect the target table `PARTITION BY` expression before finalizing the load SQL;
- compare the partition expression with the rows materialized into the temp table;
- ensure the temp table contains the full target partition being replaced, not only the current logical refresh slice;
- a daily build must not run `REPLACE PARTITION toYYYYMM(report_dt)` against a monthly-partitioned target unless it materializes the full month;
- if the intended refresh grain is daily, prefer a daily target partition such as `event_dt`/`toYYYYMMDD(event_dt)`, or change the build to reconstruct the full monthly partition;
- record the decision in the validation notes when designing a new mart or changing a partitioned load.


## DDL/load syntax self-review

Before returning ClickHouse DDL or load files:

- verify all DDL syntax is ClickHouse-native for the expected version, including table comments, column comments, codecs, TTL, settings, temporary table syntax, and `CREATE TABLE ... AS ...` behavior;
- do not use nonstandard quoting forms such as dollar-quoted comments unless the target ClickHouse version is proven to accept them;
- if `db-access` can safely run a parse-only or bounded DDL/load check in an approved sandbox, use it when the workflow layer has approved that validation; otherwise mark syntax/runtime proof as unproven and report the engine-check blocker;
- if a self-review finds invalid DDL/load syntax, fix the artifact before reporting engine-check passed. Sandbox validation is not a place to discover mistakes the agent can catch by reading the final code.
