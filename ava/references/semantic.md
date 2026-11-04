# Semantic

Semantic stores reusable business meaning: metric formulas, eligible records, units, time conventions, and join rules.

## File

| Item | Rule |
| --- | --- |
| Location | Use the user's location or project convention; otherwise `.ava/semantics/<source-key>.json`. |
| Identity | Use a stable source/reporting-scope key, not the temporary session ID. |
| Contents | Reusable definitions with their source, scope, and provenance. |
| Exclude | Temporary filters, guesses, answers, profile statistics, credentials, and personal records. |

Keep the file outside disposable outputs and the installed skill. Start with plain language:

```json
{
  "description": "Revenue is paid amount minus cumulative refunds. Null refunds mean zero.",
  "properties": {
    "source": "data/orders.csv",
    "scope": "Sales operations order reporting",
    "confirmedBy": "user",
    "confirmedAt": "2026-11-02"
  }
}
```

Adapt the example to the actual evidence. Attribute documented rules to their source instead of labeling them user-confirmed. The `properties` keys above are conventions for the agent, not fields with special CLI behavior.

## Structured Format

All six top-level keys are optional: `description` (string), `properties` (JSON object), and the arrays `models`, `relationships`, `views`, `cubes`. Add structured definitions only when useful. Names, types, `refSql`, `baseObject`, `condition`, `statement`, and measure expressions must be nonempty strings. Column `expression` may also be empty or null.

| Object | Required fields | Optional fields |
| --- | --- | --- |
| Model | `name`; exactly one of `tableReference`, `refSql`, `baseObject` | `columns`, `primaryKey`, `uniqueKeys`, `dialect`, `properties` |
| Table reference | `table` | `catalog`, `schema` |
| Column | `name`, `type` | `relationship`, `isCalculated`, `isPrimaryKey`, `notNull`, `expression`, `properties` |
| Relationship | `name`, `models` (exactly two model names), `joinType`, `condition` (SQL) | `properties` |
| View | `name`, `statement` (SQL) | `dialect`, `properties` |
| Cube | `name`, `baseObject`, nonempty `measures` | `dimensions`, `timeDimensions`, `hierarchies`, `properties` |
| Measure, dimension, time dimension | `name`, `expression`, `type` | `description`, `properties` |

`primaryKey` is a string or nonempty string array; `uniqueKeys` is an array of the same key shape. Column flags are booleans; `relationship` names a relationship. Relationship `joinType` is cardinality: `ONE_TO_ONE`, `ONE_TO_MANY`, `MANY_TO_ONE`, or `MANY_TO_MANY`. Cube `hierarchies` maps names to nonempty string arrays ordered from coarse to fine.

Use an existing schema model name to enrich that model; additional names can define logical models. `tableReference` maps a physical table, `refSql` defines a SQL source, and `baseObject` refers to another object. Keep names unique and references consistent. Put measure eligibility rules in the measure expression or its base.

For example, for a DuckDB session whose table `data` has `paid_amount`, `refund_amount`, `status`, and `region`:

```json
{
  "models": [{
    "name": "paid_orders",
    "refSql": "SELECT *, paid_amount - COALESCE(refund_amount, 0) AS net_revenue FROM data WHERE status = 'paid'",
    "columns": [{
      "name": "net_revenue",
      "type": "DOUBLE",
      "properties": {"description": "Paid amount minus cumulative refunds"}
    }]
  }],
  "views": [{
    "name": "regional_revenue",
    "statement": "SELECT region, SUM(net_revenue) AS revenue FROM paid_orders GROUP BY region",
    "dialect": "duckdb"
  }],
  "cubes": [{
    "name": "sales",
    "baseObject": "paid_orders",
    "measures": [{"name": "revenue", "expression": "SUM(net_revenue)", "type": "DOUBLE"}],
    "dimensions": [{"name": "region", "expression": "region", "type": "VARCHAR"}]
  }]
}
```

Loading metadata does not create physical tables, views, or calculated columns. A query using the example must supply the `paid_orders` CTE explicitly. Store custom annotations in `properties`; unknown keys are rejected except JSON extensions on table references, relationships, and views. Profiling `metrics` are not accepted on semantic models or columns.

## Incremental Maintenance

| Step | Operation |
| --- | --- |
| Read | Read the local file and `ava semantic "$DATASET_ID"`. Check source identity, scope, effective period, and required fields; matching field names alone are insufficient. |
| Merge | Add new rules or revise affected ones. Preserve unrelated definitions and provenance. Clarify material conflicts; temporary report overrides stay in task context. Preserve history for lasting corrections. |
| Load | Write a complete temporary candidate; run `ava semantic "$DATASET_ID" --file semantic-candidate.json`. Pass a plain path without `@`. |
| Save | Check the returned definition before replacing the local file. On load/save failure, retain the previous durable file and report what succeeded. |

When several files apply, combine their rules into one candidate; keep each durable file within its source/scope.

## Runtime Behavior

| Operation | Behavior |
| --- | --- |
| Read | Returns the current definition, initially `{}`. |
| Invalid write | Preserves the previous session value. |
| Load `{}` | Clears session semantic. |
| Update schema/profile | Retains semantic. |
| New session | Starts empty; reload compatible local definitions. |
| `analyze`, `translate`, `suggest` | Receive loaded semantic as model context. |
| `query` | Executes supplied code; the agent must implement the business rules explicitly. |

Structure validation does not verify business meaning or SQL correctness. Check new expressions with targeted queries and relevant edge cases. If the CLI lacks `semantic`, use an updated build; do not substitute `schema --file`.
