# **Logalyzer v1.0**

A simple, fast, memory-efficient command-line log analysis tool.

Logalyzer parses web server logs (Apache Combined Log Format), computes useful statistics, and outputs them in a clean, structured way. It is designed for correctness, clarity, and extensibility, allowing additional log formats and output styles to be added later.

This version focuses on:

* **Sequential log parsing**
* **Customizable log format selection**
* **Statistics aggregation**
* **Human-readable CLI output**
* **Dockerized execution**

Multiprocessing is intentionally not included in v1.0.

## **Features**

### ✔ Log Parsing

Supports the **Apache Combined Log Format** out of the box, with infrastructure for adding more formats:

* IP address
* Ident/user
* Timestamp
* HTTP method
* Request path
* Status code
* Byte size
* User Agent
* Referrer

Parsed lines are represented using a typed `LogRecord` dataclass.

### ✔ Statistics Computed

Using `compute_stats()`, Logalyzer extracts:

* **Total requests**
* **First and last timestamps**
* **Total bytes sent**
* **Requests by status code (e.g., 200, 404, 500)**
* **Requests by status class** (Success, Redirect, Client Error, Server Error)
* **Requests by HTTP method** (GET, POST, PUT, etc.)
* **Top N most requested paths**
* **Top N error paths**

### ✔ CLI Tooling

Logalyzer exposes a structured command-line interface using `argparse`.

#### Commands

#### `stats`

Analyze one or more log files.
python -m logalyzer stats <paths...> [options]


Options:

| Argument        | Description                                        |
| --------------- | -------------------------------------------------- |
| `--format`      | Log format (default: `apache_combined`)            |
| `--strict`      | Raise an error instead of skipping malformed lines |
| `--top-paths N` | Show top N visited paths (default: 3)              |

#### `parse`

Print parsed records from a log file.
python -m logalyzer parse <path> [--format FORMAT]

## **Project Structure**
logcli/
│
├── logalyzer/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── reader.py
│   ├── parser.py
│   ├── models.py
│   ├── stats.py
│   ├── output_helpers.py
│   └── parser_formats.py
│
├── log_files/
│   └── … (sample log files)
│
├── tests/
│   └── … (unit tests)
│
├── Dockerfile
├── requirements.txt
└── README.md

## **Installation**

### Local execution

1. Create a virtual environment:
python -m venv .venv

2. Activate it:
# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate


3. Install requirements:
pip install -r requirements.txt


4. Run Logalyzer:
python -m logalyzer stats ./log_files/apache_combined_1


## **Docker Usage**
Logalyzer ships with a Dockerfile for isolated execution.

### Build the image:
docker build -t logalyzer:1.0 .


### Running in Docker

Mount your log directory into the container and run:
docker run --rm -v C:\YOUR_PATH\logcli\log_files:/logs logalyzer:1.0 stats /logs/apache_combined_1 --top-paths 10


Linux/macOS version:
docker run --rm -v $(pwd)/log_files:/logs logalyzer:1.0 stats /logs/apache_combined_1 --top-paths 10

## **Extending Logalyzer**

### Adding a new log format

1. Create a new class implementing `LogFormat` in `parser_formats.py`
2. Define:

   * `name`
   * `pattern`
   * `parse_line()`
3. Register the format in the registry dict

Logalyzer will automatically pick it up via the `--format` flag.

---

## **Testing**

Unit tests cover:

* `LogRecord` model behavior
* Parsing functions
* Reader functions
* Stats aggregation

Run tests with:
pytest


## **Known Limitations in v1.0**

* No multiprocessing (planned for v2.0)
* No streaming output formatter
* Only Apache Combined logs supported
* No JSON/YAML output option


## **Roadmap**

### v2.0 (planned)

* Multiprocessing for parallel parsing
* Streamed inter-process record handling
* Rich CLI output (colorized tables)

## **License**

MIT License (or whatever license you want; add it here).

