# Data Sources

## Choose an Engine

| Data source | Engine | Query language |
| --- | --- | --- |
| CSV/JSON/Parquet/Excel files | DuckDB by default; Python is optional | DuckDB SQL / Python (pandas) |
| Inline CSV/JSON | DuckDB by default; Python or JavaScript is optional | SQL / Python / JavaScript |
| Unstructured text | DuckDB by default; JavaScript is optional; requires a model | SQL / JavaScript |
| MySQL, PostgreSQL, SQLite, MongoDB | DuckDB only | DuckDB SQL |
| ClickHouse | ClickHouse only, selected automatically | ClickHouse SQL |
| Supabase | Supabase only, selected automatically | PostgreSQL SQL |
| Feishu Bitable | DuckDB only | DuckDB SQL |

To use Python or JavaScript, add `--engine python` or `--engine javascript` to the `source` command. Python does not connect directly to databases. To post-process database results with pandas, query the database first, then export the complete result as described in [Results and Post-Processing](queries.md#results-and-post-processing).

## Files and Configuration

**Load a regular file or URL directly:**

```sh
ava source /data/sales.csv > session.json
```

The CLI identifies CSV, JSON, Parquet, XLSX, and SQLite (`.sqlite`, `.sqlite3`, `.db`) files by extension. If the extension is not recognized, use `--type` with `csv-file`, `json-file`, `parquet`, `excel`, or `sqlite`. SQLite supports local files only; other file sources support HTTP(S). Each Excel sheet becomes a table; use the schema to find its actual table name.

**Use configuration for inline data, authentication, or custom read options:**

Configuration includes `type` and `options`. `type` specifies the data format or database type, not the engine. For example, to read a semicolon-delimited CSV while preserving text types, save the following as `source.json`:

```json
{
  "type": "csv-file",
  "options": {
    "path": "/data/sales.csv",
    "options": { "delim": ";", "all_varchar": true }
  }
}
```

```sh
ava source @source.json > session.json
```

A regular `.json` file is read as data rows. Only `@file` or stdin `-` reads JSON as configuration; configuration input cannot be combined with `--type`. Relative paths are resolved from the command's working directory.

For other common configurations, set `type` and `options` as shown:

| Use case | `type` | Example `options` |
| --- | --- | --- |
| JSON rows | `json` | `{"data":[{"region":"East","sales":10}]}` |
| Inline CSV | `csv` | `{"csv":"region,sales\nEast,10"}` |
| Unstructured text | `text` | `{"text":"East region sales were 10."}` |
| Parquet file | `parquet` | `{"path":"/data/sales.parquet"}` |
| Excel workbook | `excel` | `{"path":"/data/sales.xlsx","sheets":[{"sheet":"Orders","range":"B3:F100","header":true}]}` |
| Authenticated URL | `json-file` | `{"path":"https://example.com/data.json","headers":{"Authorization":"******"}}` |

File sources except SQLite accept `headers` for HTTP(S) authentication. `csv-file` and `json-file` accept nested `options` for reader settings; `parquet` does not.

For Excel, omitting `sheets` loads every sheet. Otherwise use a nonempty array of unique sheet names, each with `sheet`, optional inclusive A1 `range`, and `header` (default `true`). DuckDB expects `.xlsx` and also accepts per-sheet booleans `all_varchar`, `ignore_errors`, `stop_at_empty`, and `empty_as_varchar`. Python supports `sheet`, `range`, and `header` only.

Python CSV reader options are limited to `header`, `names`, `delim`, `quote`, `escape`, `comment`, `skip`, `nullstr`, `all_varchar`, `decimal_separator`, `thousands`, `encoding`, and `compression`. Python JSON sources do not accept reader `options`. Do not assume DuckDB reader settings work in Python.

The native `text` source extracts rows using an AVA model and requires model credentials (see [Setup](setup.md)). Alternatively, extract JSON rows yourself, keeping only information supported by the source text, then load `json`.

## Databases

Use the configuration format and load command shown above:

| `type` | Example `options` |
| --- | --- |
| `mysql` | `{"host":"localhost","database":"sales","user":"reader","password":"REPLACE"}` |
| `postgresql` | `{"host":"localhost","database":"sales","user":"reader","password":"REPLACE","schema":"public"}` |
| `sqlite` | `{"path":"/data/sales.sqlite"}` |
| `mongodb` | `{"connection":"mongodb://localhost:27017","database":"sales"}` |
| `clickhouse` | `{"url":"http://localhost:8123","database":"sales","username":"reader","password":"REPLACE"}` |
| `supabase` | `{"accessToken":"REPLACE","projectRef":"REPLACE"}` |

Use authorized read-only credentials. Restrict temporary credential files to the current user and delete them after loading. Do not put credentials in deliverables or logs.

- MySQL, PostgreSQL, SQLite, and MongoDB require the corresponding DuckDB extensions. MongoDB uses the `mongo` community extension. Each collection becomes a table, and its schema is inferred from samples, so rare fields may be missed.
- MySQL/PostgreSQL accept `port` and `ssh: {"host":"bastion","user":"reader","port":22,"password":"REPLACE"}`. PostgreSQL defaults to schema `public`.
- MongoDB accepts `connection` or structured `host`, `port`, `user`, `password`, `authSource`, `srv`, `tls`, `ssl`, `tlsCAFile`, and `tlsAllowInvalidCertificates`; `database` is required in either form. `connection` takes precedence; keep its database consistent with `database`.
- ClickHouse connects over HTTP(S) and requires version 23.10 or later.
- ClickHouse requires `database` and either `host` or `url`. It accepts `port`, `user`/`username`, `password`, `access_token`, `pathname`, `application`, `session_id`, `role` (string or string array), `http_headers`, `request_timeout`, and other ClickHouse client options.
- Supabase uses the Management API; `accessToken` must be a token authorized for that API.

## Feishu Bitable

`feishu-bitable` is read-only and uses DuckDB; the Python and JavaScript engines cannot load it. Rows are exposed as one view named `data`. The `view` parameter in the URL is ignored and the whole table is loaded, not one view.

The CLI detects Bitable links on `feishu.cn` and `larksuite.com` automatically (Node.js 22.13+), including tables that live inside a wiki:

```sh
ava source "https://<tenant>.feishu.cn/base/<app_token>?table=<table_id>" > session.json
ava source "https://<tenant>.feishu.cn/wiki/<node_token>?table=<table_id>" > session.json
```

A `/wiki/` URL carries a node token, so AVA calls the wiki `get_node` API and uses the hosted object's `obj_token` as the Bitable app token. The node must host a Bitable (`obj_type=bitable`); the app also needs `wiki:wiki:readonly` and membership of the wiki space, which is separate from the document grant on the table. Docx and Sheets nodes are rejected with an explicit error.

When `?table=` is missing, AVA uses the only table of the Bitable and, when there are several, stops with the table list so you can pick one. For non-URL configs, pass `feishu-bitable` through an `@file` or stdin config; `--type` cannot supply it.

`appId` and `appSecret` are required. They are the internal app credentials used to request a tenant access token, and the app must be added as a collaborator on the table. A `bitable:app:readonly` scope is enough unless the table enables advanced permissions, which require manage rights. Credentials are resolved from the source config first, then `AVA_FEISHU_APP_ID` / `AVA_FEISHU_APP_SECRET`, then `~/.ava/feishu.json`. In a terminal, AVA prompts for the pair, verifies it, and saves it to `~/.ava/feishu.json`.

The app must belong to an account allowed to call the Open Platform. Apps created by signing in to `open.feishu.cn` with a personal account such as a Doubao account are rejected with `Feishu Error 21001` (access denied due to platform policy) when requesting the tenant access token; create the app with a Feishu account bound to a phone number instead.


```json
{
  "type": "feishu-bitable",
  "options": {
    "url": "https://<tenant>.feishu.cn/base/<app_token>?table=<table_id>",
    "appId": "<app-id>",
    "appSecret": "<app-secret>"
  }
}
```

```sh
ava source @feishu.json > session.json
```

Provide `url`, or both `appToken` and `tableId`; when both are set they must name the same table. The path segment after `base` is `appToken`, and the `table` query parameter is `tableId`. For a `/wiki/` URL the segment after `wiki` is a node token that AVA resolves to the app token, so `appToken` alone is not enough to describe a wiki table. Never commit `appSecret` or put it in deliverables, logs, or screenshots; rotate it if it leaks.

Supported field types become columns. Other types are omitted. Complex cells are flattened to text; list values are joined with a comma.

| type | Field | Cell value |
| --- | --- | --- |
|1| Text | string, or null when empty |
|2| Number | number, or null when empty |
|3| Single select | option name, or null |
|4| Multi select | option names joined by comma, or null |
|5| Date | ISO string, or null |
|7| Checkbox | boolean |
|11| User | names joined by comma (name → en_name → email → id) |
|13| Phone | string, or null |
|15| URL | link text, or the URL, or null |
|17| Attachment | file names joined by comma |
|18| Single link | record IDs joined by comma |
|19| Lookup | converted from the wrapped result type |
|20| Formula | converted from the wrapped result type |
|21| Duplex link | record IDs joined by comma |
|22| Location | full address, falling back to name, address, or coordinates |
|23| Group chat | group names joined by comma |
|1001| Created time | ISO string |
|1002| Last modified time | ISO string |
|1003| Created user | names joined by comma |
|1004| Modified user | names joined by comma |
|1005| Auto number | string, or null |

Stage (24) and button (3001) fields are read-only and skipped. A formula or
lookup whose result type is unsupported becomes null.
