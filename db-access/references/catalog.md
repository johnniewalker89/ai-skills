# Catalog Investigation

Read when catalog discovery or lineage is needed.

Use `bi_metadata` as the first catalog step when a task asks to find, understand, compare, explain, or debug tables, marts, dashboards, owners, tags, domains, columns, upstream/downstream dependencies, or data-quality impact.

- Start with `search_metadata` for exact names, FQNs, services, owners, tags, tiers, domains, known column names, or structured filters.
- Use `semantic_search` for vague business-language requests, unknown table names, or exploratory source discovery.
- Pass the returned `fullyQualifiedName` and `entityType` unchanged into `get_entity_details` or `get_entity_lineage`; do not construct or normalize FQNs manually.
- Use `get_entity_details` to inspect descriptions, columns, owners, tags, service/database/schema, domains, data products, and available table metadata before choosing or documenting a source.
- Use `get_entity_lineage` for normal upstream/downstream explanation and impact checks; use `root_cause_analysis` only when investigating data-quality failures or suspected upstream breakage.
- Keep catalog evidence separate from live DB proof: OpenMetadata can identify candidates, ownership, meaning, and lineage, but DDL, row counts, query behavior, freshness, and runtime proof still require the appropriate read-only database tools when needed.
- Page search results deliberately. Prefer a narrow query or small candidate set over dumping broad catalog results into chat.
- If OpenMetadata and live DB/repo evidence disagree, report the mismatch and do not silently treat catalog metadata as runtime truth.
