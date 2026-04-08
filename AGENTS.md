# Python Samples: Project Structure and Automation

This document provides a summary of the project structure, testing conventions, and all automation commands used in Kokoro CI, GitHub Actions, and developer workflows.

## Analysis of `storage` and `storagecontrol` Directories

### 1. Testing Conventions
- **Framework:** `pytest`.
- **Environment:** `nox` for isolation.
- **Fixtures:** Shared fixtures in `conftest.py` for live resource management (GCS buckets/objects).
- **System Testing:** End-to-end tests requiring service accounts and real projects.

### 2. Placement of Tests
- **Co-located:** Tests are in the same folder as the samples (e.g., `storagecontrol/snippets_test.py`).

---

## Automation Commands

### Kokoro CI (`.kokoro/`)

The following commands are extracted from the main test runner (`.kokoro/tests/run_tests.sh`) and individual task scripts:

**1. Environment Setup:**
```bash
pip install --upgrade pip
pip install --user -q nox
# For Python 2.7 legacy support (if applicable)
pip install --user -q virtualenv==20.21
```

**2. Authentication & Secrets:**
```bash
gcloud auth activate-service-account --key-file="${KOKORO_GFILE_DIR}/secrets_viewer_service_account.json" --project="cloud-devrel-kokoro-resources"
./scripts/decrypt-secrets.sh
export GOOGLE_APPLICATION_CREDENTIALS=$(pwd)/testing/service-account.json
gcloud auth activate-service-account --key-file "${GOOGLE_APPLICATION_CREDENTIALS}"
```

**3. Database Proxies (for SQL samples):**
```bash
wget --quiet https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O ${HOME}/cloud_sql_proxy
chmod +x ${HOME}/cloud_sql_proxy
${HOME}/cloud_sql_proxy -instances="${MYSQL_INSTANCE}"=tcp:3306,"${MYSQL_INSTANCE}" -dir "${HOME}" &>> ${HOME}/cloud_sql_proxy.log &
${HOME}/cloud_sql_proxy -instances="${POSTGRES_INSTANCE}"=tcp:5432,"${POSTGRES_INSTANCE}" -dir "${HOME}" &>> ${HOME}/cloud_sql_proxy-postgres.log &
${HOME}/cloud_sql_proxy -instances="${SQLSERVER_INSTANCE}"=tcp:1433 &>> ${HOME}/cloud_sql_proxy-sqlserver.log &
```

**4. Test Execution (btlr):**
```bash
# Kokoro uses btlr to orchestrate concurrent tests across all changed directories
btlr run --max-cmd-duration=60m "**/requirements.txt" --max-concurrency ${NUM_TEST_WORKERS} --git-diff ${DIFF_FROM} . -- .kokoro/tests/run_single_test.sh
```

**5. Single Directory Test (`run_single_test.sh`):**
```bash
# If no noxfile exists, copy template
cp "$PARENT_DIR/noxfile-template.py" "./noxfile.py"
# Execute using Makefile
make test dir=${test_subdir}
```

### Makefile Commands

Developers use the following `make` commands:

- **Build:** `make build dir=<sub-directory>`
  - Runs: `pip install nox`
- **Test:** `make test dir=<sub-directory> [py=3.11]`
  - Runs: `nox -s py-$(py)` (or `$RUN_TESTS_SESSION` in CI)
- **Lint:** `make lint dir=<sub-directory>`
  - Runs:
    - `pip install nox black`
    - `nox -s blacken`
    - `nox -s lint`
- **Utility:**
  - `noxfile.py`: Copies `noxfile-template.py` to target directory if missing.
  - `check-env`: Verifies `GOOGLE_SAMPLES_PROJECT` or `GOOGLE_CLOUD_PROJECT` is set.
