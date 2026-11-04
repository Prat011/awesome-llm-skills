# Environment Setup

## CLI

Requires AVA CLI **4.x**, Node.js ≥22.13, and macOS or Linux. The runtime must support long-lived background processes and Unix sockets. Calls must share the same user, runtime environment, and temporary directory.

Check the Node.js version and confirm that the CLI is available:

```sh
node --version
ava source --help
```

Prefer an existing installation or project build of this version. Otherwise, install:

```sh
npm install -g @antv/ava@4
```

## Model-Backed Commands

`source` with type `text`, `analyze`, `translate`, `suggest`, `recommend`, and `visualize` use AVA's model integration. Set `OPENAI_API_KEY`; optionally set `OPENAI_MODEL` (default `gpt-4o-mini`) and `OPENAI_BASE_URL`. For session commands, set these before creating the session; later environment changes do not update its model configuration. Loading structured data, running `query`, managing semantic, and rendering a supplied Spec with `viz` do not require a model API key.

## Python

When using `--engine python`, select an existing virtual environment or a Python environment for the current task, and put its `python3` on `PATH`.

Check the dependencies in that environment. pandas is required; Parquet also requires a supported reader (such as `pyarrow`), and XLSX requires `openpyxl`. For example:

```sh
python3 -c 'import pandas; print(pandas.__version__)'
```

Install any missing packages in the same environment, then create the session. Switching Python environments requires a new session.

By default, execution runs in a local subprocess with the current user's file and network permissions; it is not a security sandbox. For isolation, run the entire CLI inside a sandbox provided by the host.

## Sessions

Save session IDs and query outputs in a task-specific directory. For example:

```sh
ava source /absolute/path/sales.csv > session.json
DATASET_ID=$(node -p 'JSON.parse(require("fs").readFileSync("session.json", "utf8")).datasetId')
ava schema "$DATASET_ID" > schema.json
```

Across terminals, recover the ID from the file instead of relying on another process's environment variables.

Sessions expire after 30 idle minutes or disposal. If access remains authorized, reload the same source and engine, refresh schema, and reapply compatible saved semantic. Recompute statistics only as needed.

When finished or after failure, close task-created sessions that are no longer needed with `ava dispose "$DATASET_ID"`. Keep a session if analysis will continue. Close a user-provided session only when explicitly asked.
