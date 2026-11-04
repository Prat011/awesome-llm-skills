# Visualization

Build charts from user-provided data or the `data` in query results. All engines use the same charting workflow. Follow the steps in order; at each `IF`, take the first branch that matches.

## Workflow

```
Step 1 Get data → Step 2 Pick intent → Step 3 Check data shape → Step 4 Choose chart → Step 5 Map fields & build Spec → Step 6 Render & inspect
```

### Step 1: Get usable data

- IF the user supplied a chart type: use it, and go to Step 3 only to verify the data fits. If it does not fit, say why and use the Step 4 alternative.
- ELSE IF there is no data yet: run a query first (see queries.md) and come back with the result.
- ELSE IF the data has many rows (more than can be read in a chart, roughly 50+) and the chart is not `scatter`, `histogram`, `boxplot`, `violin` or `table`: aggregate (`GROUP BY`) or take Top N (usually 10) sorted by value first, and label this in the chart.
- ELSE: continue.

### Step 2: Identify the intent

- IF the question is about change over time (trend, growth, by month/year): intent = **trend**.
- ELSE IF it is about comparing or ranking categories (which is highest, top N): intent = **comparison**.
- ELSE IF it is about share or composition (proportion, breakdown): intent = **part-to-whole**.
- ELSE IF it is about correlation or the effect of one variable on another: intent = **relationship**.
- ELSE IF it is about spread, shape, or outliers: intent = **distribution**.
- ELSE IF it is about stage conversion or drop-off: intent = **funnel**.
- ELSE IF it is about what increases or decreases a total: intent = **change breakdown**.
- ELSE IF it is about flow between nodes: intent = **flow**.
- ELSE IF it is about overlap between sets: intent = **intersection**.
- ELSE IF it is about exact values or details: intent = **lookup** (use `table`).
- ELSE: intent unclear; infer from the data shape in Step 3, or ask the user.

### Step 3: Check the data shape

Classify each field as time, category, numeric measure, or text. Numeric IDs and year-like numbers are not measures. Note row count, distinct categories, series count, negatives, nulls, and ordering.

- IF a field that must be numeric is a string (for example `"12%"`, `"1,200"`): convert it to a plain number first.
- IF the time field is unsorted: sort it ascending.
- IF there is only one row and the intent is trend, comparison or distribution: stop and use `table`, or ask for more data.

### Step 4: Choose the chart

Use the branch for the intent from Step 2.

**Trend**
- IF there are two measures on very different scales: `dual-axes`.
- ELSE IF the total matters and the series add up: `area` with `stack true`.
- ELSE: `line` (use `group` for multiple series).
- Never use `line` for unordered categories; use Comparison instead.

**Comparison**
- IF labels are long or there are more than about 8 categories: `bar`.
- ELSE: `column`.
- IF there is a second dimension: add `group` (`stack` or `group true` for `column`/`bar`).
- IF there are many categories: sort by value and keep Top N.

**Part-to-whole**
- IF the data is a single percentage or progress: `liquid`, with `percent` from 0 to 1; otherwise use `bar` or `table`.
- ELSE IF any value is negative: `bar`.
- ELSE IF the total is zero: `table`.
- ELSE IF the data is hierarchical (parent/child): `treemap`.
- ELSE IF there are 5 or fewer categories: `pie` (`innerRadius 0.6` for a donut). Values must be plain numbers, not percentages, with a positive total.
- ELSE IF there are more than 5 categories: merge the tail into "Other" and use `pie`, or use `bar`.

**Relationship**
- IF both fields are numeric: `scatter` (`group` for a third categorical dimension).
- ELSE: use Comparison.

**Distribution**
- IF one numeric field of raw observations: `histogram`.
- ELSE IF comparing distributions across categories and each category has many observations: `boxplot` (outliers, quartiles) or `violin` (density).
- ELSE IF each category has only one value: `column`.

**Funnel**
- IF ordered stages with decreasing values: `funnel`. ELSE: `column`.

**Change breakdown**
- IF signed changes that sum to a total: `waterfall` (mark the total with `isTotal true`). ELSE: `column`.

**Flow**
- IF `source`/`target`/`value` pairs form an acyclic flow: `sankey`. ELSE: `table`.

**Intersection**
- IF set sizes and overlaps: `venn`. ELSE: `table`.

**Other**
- IF the text data is about word frequency: `word-cloud`.
- IF comparing a few entities across several dimensions: `radar` (add `align true` only to compare absolute values on a shared scale).
- IF the request needs a type not supported by `ava viz` (flow diagram, mind map, tree, network graph, org chart, fishbone, text summary): do not invent a `chartType`; use `table` or the closest supported chart and say why.
- IF none of the above fits, there are more than two measures with no clear intent, or the user wants exact values: `table`.

### Step 5: Map fields and build the Spec

Map actual fields to the fields below. Unless noted otherwise, fields belong to each item in the `data` array; `value`, `x`, and `y` are numeric. When there are two dimensions, put the axis dimension in `time`/`category` and the other in `group`.

These are all 19 chart types registered by the CLI. `summary` is not registered and cannot be passed to `ava viz`.

| `chartType` | Data fields or structure |
| --- | --- |
| `column`, `bar` | `category`, `value`, optional `group`; `stack` or `group true` |
| `line` | `time`, `value`, optional `group` |
| `area` | `time`, `value`, optional `group`; `config.stack: true` for stacked area |
| `pie` | `category`, `value`; `innerRadius` 0.6 creates a donut chart |
| `scatter` | `x`, `y`, optional `group` |
| `histogram` | Array of raw numeric observations |
| `boxplot`, `violin` | `category`, `value`; multiple observations per category |
| `radar` | `name`, `value`, optional `group` |
| `funnel` | `category`, `value`, ordered by stage |
| `waterfall` | `category`, `value`; mark the total item with `"isTotal": true` |
| `liquid` | Top-level `percent`, from 0 to 1; no `data` array |
| `word-cloud` | `text`, `value` |
| `venn` | `sets`, `value`; `sets` is an array; write intersections as `["A", "B"]` |
| `treemap` | `name`, `value`, optionally nested in a `children` array |
| `sankey` | `source`, `target`, `value` |
| `table` | Fields from the original rows |
| `dual-axes` | Top-level `categories` and `series` arrays; each series has `type` (`column` or `line`), `axisYTitle`, and numeric `data` aligned with `categories` |

Config properties used by AVA's chart generator:

| Property | Applies to |
| --- | --- |
| `title`, `theme` (`default`, `light`, `dark`, `academy`), `style` (`backgroundColor`, `palette` array) | All charts |
| `axisXTitle`, `axisYTitle` | `line`, `area`, `column`, `bar`, `scatter`, `histogram`, `boxplot`, `violin`, `waterfall` |
| `axisXTitle`, `series[].axisYTitle` | `dual-axes` |
| `binNumber` | `histogram` |
| `align` | `radar` |
| `shape` (`rect`, `circle`, `pin`, `triangle`) | `liquid` |
| `label` on a set | `venn` |
| `nodeAlign` (`left`, `center`, `right`, `justify`) | `sankey` |

JSON config fragments for the less obvious structures (wrap each in `{ "chartType": "…", "config": … }` for `--spec`):

```json
{ "type": "histogram", "data": [68, 72, 85], "binNumber": 10 }
```

```json
{
  "type": "dual-axes",
  "categories": ["Jan", "Feb"],
  "series": [
    { "type": "column", "axisYTitle": "Sales", "data": [820, 650] },
    { "type": "line", "axisYTitle": "Profit", "data": [12, 10] }
  ]
}
```

```json
{ "type": "table", "data": [{ "Product": "Laptop", "Region": "East China", "Sales Amount": 3200 }] }
```

For `table`, every row is one `data` item and each original column is a key. For `waterfall`, the total item has `category` and `isTotal` but no `value`. For `treemap`, put nested items under `children` with the same `name`/`value` fields.

Then build the Spec:

A Spec is a JSON object with exactly two keys: `chartType`, the chart type string, and `config`, the GPT-Vis JSON config object.

- Set `config.type` to `chartType` for consistency; the CLI fills or overrides it with `chartType` before rendering.
- Put the fields from the table above directly in `config`. Use plain numbers for numeric values; put units in the title or axis title.
- The chart size adapts to its container, so do not set `width` or `height`.

For example, given regional totals `[{"region":"East","total":25},{"region":"West","total":20}]`, map `region → category` and `total → value`, then save as `chart.json`:

```json
{
  "chartType": "column",
  "config": {
    "type": "column",
    "data": [
      { "category": "East", "value": 25 },
      { "category": "West", "value": 20 }
    ],
    "title": "Total by region",
    "axisXTitle": "Region",
    "axisYTitle": "Total"
  }
}
```

### Step 6: Render and inspect

```sh
ava viz --spec @chart.json --output chart.html
```

The returned `output` is the absolute path to the HTML file. Existing files are not overwritten. The HTML requires an internet connection to load GPT-Vis.

The CLI validates only the Spec structure and chart type; it does not verify that the config renders correctly. If a browser is available, preview the chart and check the field mappings, ordering, title, units, and data range. If you do not preview it, say so. Label Top N selections and aggregated categories in the chart.

If rendering fails, fix the error and retry up to two times. If it still fails, provide the results table and explain why the chart could not be rendered.

## CLI Entry Points

| Command | Input | Result | Model required |
| --- | --- | --- | --- |
| `viz --spec @chart.json --output chart.html` | Complete Spec; inline JSON, `@file`, or stdin `-` | Absolute `output` path | No |
| `recommend --query "…" --data @rows.json` | Question and array of row objects | Spec, or `null` when no chart fits | Yes |
| `visualize --query "…" --data @rows.json --output chart.html` | Question and array of row objects | Spec and HTML, plus `output` when requested; or `null` | Yes |

None requires a dataset ID. For `recommend`/`visualize`, `--data` accepts inline JSON, `@file`, or stdin `-`; even histogram input must be row objects. A manual histogram Spec instead uses numeric observations in `config.data`. Model setup is described in [Setup](setup.md).
