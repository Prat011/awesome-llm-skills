# Queries and Results

## Inspect as Needed

Use schema for structure, targeted queries for specific facts, and profile for broader statistics. For example:

```sh
ava profile "$DATASET_ID" --metrics row_count,null_count,min,max,mean > profile.json
```

Each profile call recomputes statistics. `--metrics` replaces the defaults and applies to eligible columns across all tables; it cannot filter by table or column. Prefer targeted queries on large remote sources.

## Run a Query

`ava schema` discovers structure on demand and caches it. Use its `models`, `tableReference`, `columns`, and `language`. Write the query according to `language.name` and, when provided, `language.instructions`. Apply confirmed [business definitions](semantic.md) explicitly; `query` executes the supplied DSL without applying semantic filters or expressions for you. Save the query as UTF-8 and run it with `--dsl`:

```sh
ava query "$DATASET_ID" --dsl @query.sql > result.json
```

Python and JavaScript queries can be saved as `query.py` and `query.js` and run the same way. The file extension does not change the session engine. Read only the section for the active language and results below, and replace example names with actual table and column names.

## SQL

Write a single read-only `SELECT` statement in the session's dialect. Read-only CTEs are allowed. Access only loaded tables and columns.

```sql
SELECT region, SUM(amount) AS total
FROM sales
GROUP BY region
ORDER BY total DESC, region;
```

For ClickHouse, do not add `FORMAT`, `SETTINGS`, or `INTO OUTFILE`; AVA handles execution.

## Python / pandas

| Binding | Usage |
| --- | --- |
| `pd` | pandas, already imported |
| `tables` | A dictionary of DataFrames keyed by schema table name, such as `tables['Orders']` |
| `df` | Provided only when there is one table; for multiple tables, select one explicitly from `tables` |
| `result` | Must be assigned. Accepts a DataFrame, Series, list of records, a single record, or a JSON scalar. A scalar is returned at `data[0].value`. |

- Compute on the loaded DataFrames. Do not read or write other files, access the network, install packages, or print the answer.
- Each query reloads the source and does not preserve variables or changes from prior queries. Include all required transformations in the same query. The default execution timeout is 30 seconds; a timed-out local subprocess is terminated.
- DataFrame and Series indexes are not included in the result. Use `reset_index()` to preserve index values; for grouping, you can also use `as_index=False`.

For example, sum by region while preserving missing regions and groups with all-null amounts:

```python
result = (
    df.groupby('region', dropna=False, as_index=False)['amount']
      .sum(min_count=1)
      .rename(columns={'amount': 'total'})
)
```

## JavaScript

The input is a `data` array. A `stat` statistics object is provided. Assign the final output to `result` as an array of objects. The example below assumes all `amount` values are numeric:

```javascript
const result = [{ total: data.reduce((sum, row) => sum + row.amount, 0) }];
```

Each execution uses a copy of the input and does not preserve variables or changes from previous executions. Node.js file, network, and package-loading APIs are unavailable. Some numeric functions in `stat` treat values that cannot be converted to numbers as zero; handle them explicitly when nulls matter.

## Results and Post-Processing

After a command succeeds, read the returned JSON:

- `data` contains the answer data for responding, charting, or post-processing; `schema` describes the result columns.
- `truncated: true` means the result is incomplete; `truncatedBy` gives the reason. These fields may be omitted when the result is not truncated.
- `rowCount` is the number of rows in the current query result, not the source table. It is omitted when the result is truncated.

The default response limit is 200 rows or 1 MiB. Adjust it with `--max-rows` (up to 10000) and `--max-result-bytes`; individual fields are still limited to 1 MiB. These limits apply only to returned data. Perform aggregations and statistics in the execution engine; do not use truncated, limited, or sampled detail rows as a substitute for full-data statistics.

For cross-engine post-processing, first confirm that the result is complete, then save and load `data` as a JSON array rather than loading the entire result object. Keep the query and metric definitions used to generate intermediate data. An untruncated result does not necessarily mean the query covered all source data.
