Plan: Add backend FastAPI tests

Goal
- Add a test suite under `tests/` to cover the FastAPI backend (`src.app`). Ensure tests run in isolation and reset the in-memory `activities` between tests.

Steps
1. Create a `tests/` directory (if missing).
2. Add `tests/test_backend.py` with the following responsibilities:
   - Use `fastapi.testclient.TestClient` to exercise the API.
   - Provide an autouse fixture that deep-copies the original `activities` data and restores it after each test (so tests are isolated).
  - Tests to implement (follow AAA -- Arrange, Act, Assert):
    - Arrange: set up fixtures, restore in-memory data, and prepare inputs.
    - Act: call the endpoint under test (GET, POST, DELETE).
    - Assert: verify response status, body, and side effects on `activities`.
  - Example test cases to implement:
     - `test_get_activities`: GET `/activities` returns 200 and includes `Chess Club`.
     - `test_signup_for_activity_success`: POST signup for a new email increases participant count and returns 200.
     - `test_signup_for_activity_duplicate`: Attempting to signup the same email twice returns 400.
     - `test_unregister_from_activity_success`: DELETE removes an existing participant and returns 200.
     - Additional negative cases: signup for missing activity (404), delete missing participant (404).
3. Ensure `pytest.ini` includes `pythonpath = .` (already present) so `src` imports work.
4. (Optional) Add `pytest` to `requirements.txt` or install in dev environment.
5. Run the tests locally with `pytest -q` and iterate on failures.

Notes / Implementation hints
- Use `copy.deepcopy()` to snapshot `activities` and restore it after each test.
- Use `urllib.parse.quote` when building URLs that contain activity names with spaces.
- Keep tests deterministic by always restoring the original `activities` state.
- Place the test file at `tests/test_backend.py` and prefer pytest fixtures for setup/teardown.

Commands to run locally
```
pip install -r requirements.txt
pip install pytest
pytest -q
```

Deliverable
- `tests/test_backend.py` created under `tests/` with the tests described above, ready for refinement and expansion.