# Python Samples: Project Structure and Automation

This document provides a summary of the project structure, testing conventions, and automation workflows for the Python samples.

## Analysis of `storage` and `storagecontrol` Directories

### 1. Testing Conventions
- **Framework:** `pytest`.
- **Environment:** `nox` for isolation.
- **Fixtures:** Shared fixtures in `conftest.py` for live resource management (GCS buckets/objects).
- **System Testing:** End-to-end tests requiring service accounts and real projects.

### 2. Placement of Tests
- **Co-located:** Tests are in the same folder as the samples (e.g., `storagecontrol/snippets_test.py`).

### 3. Dependency Management
- **No Manual Updates:** Do not modify `requirements.txt` or `requirements-test.txt` directly. An automated bot manages dependencies; you must not touch or make any changes to these files.

---

## Jules Instructions

Jules should use these commands to replicate CI workflows for a specific sample directory.

### 1. Prerequisites
Ensure the following environment variables are set:
- `GOOGLE_CLOUD_PROJECT` (or `GOOGLE_SAMPLES_PROJECT`)
- `GOOGLE_APPLICATION_CREDENTIALS` (path to a service account JSON key)

### 2. Linting (Kokoro CI - Lint)
Replicates the "Kokoro CI - Lint" build. This runs the linter (flake8) via `nox`:
```bash
make test dir=<sub-directory> RUN_TESTS_SESSION=lint
```

### 3. Testing (Kokoro CI - Python X.Y)
Replicates the various Python version builds (3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14):
```bash
make test dir=<sub-directory> py=<version>
```
Example for Python 3.10:
```bash
make test dir=<sub-directory> py=3.10
```

---

## Automation & Developer Workflows

### Makefile Commands

Developers use the following `make` commands:

- **Build:** `make build dir=<sub-directory>`
  - Runs: `pip install nox`
- **Test:** `make test dir=<sub-directory> [py=3.11]`
  - Runs: `nox -s py-$(py)` (or `$RUN_TESTS_SESSION` if defined)
- **Lint:** `make lint dir=<sub-directory>`
  - Runs:
    - `pip install nox black`
    - `nox -s blacken`
    - `nox -s lint`
- **Utility:**
  - `noxfile.py`: Copies `noxfile-template.py` to target directory if missing.
  - `check-env`: Verifies `GOOGLE_SAMPLES_PROJECT` or `GOOGLE_CLOUD_PROJECT` is set.
