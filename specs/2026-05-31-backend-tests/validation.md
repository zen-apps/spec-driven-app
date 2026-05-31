# Validation — Backend tests (pytest) (Phase 3)

Detailed checklist to verify that backend behavior is fully locked in and validated before considering Phase 3 complete.

## Automated

### 1. Local Hermetic Test Suite
Verify that the test suite runs and passes cleanly in the local environment without requiring any network calls or credentials files.

- [ ] Execute `make test-local` (or `pytest backend/tests` directly).
- [ ] All written test cases pass (asserting status code, JSON response shapes, token calculations, and helper results).
- [ ] Pytest generates no warnings or deprecation errors that would fail a strict test run.

### 2. Containerized Test Suite
Verify that the test suite runs and passes inside the identical Docker container environment used for production.

- [ ] Rebuild the container stack using `docker-compose build`.
- [ ] Execute `make test-container` (or `docker-compose run --rm backend pytest` directly).
- [ ] All written test cases pass within the container context.

### 3. Isolation & Mocking Verification
Verify that the test suite is 100% hermetic (completely isolated from the live API).

- [ ] Temporarily remove or empty the `./credentials/` folder or unset any local environment variables.
- [ ] Execute `make test-local` or `make test-container`.
- [ ] The tests still pass, proving no live API setup/authentication is executed during the test run.

---

## Manual

Perform these manual verification tasks to confirm the robustness of the test suite and repository configurations:

### 1. Intentional Code Mutation / Verification Test
Ensure that our test assertions are active and robust.

- [ ] Open `backend/app/helpers.py` and temporarily modify one of the normalization functions (e.g., change `return ""` to `return "mutated"` in `normalize_content`).
- [ ] Run `make test-local`.
- [ ] Confirm that at least one test case fails as a result, showing that the assertions are valid.
- [ ] Revert the temporary change.

### 2. Output Schema Consistency Check
Confirm that the mocks align with actual JSON payloads returned by FastAPI.

- [ ] Check `test_main.py` success endpoint assertions.
- [ ] Verify that the mocked response matches the JSON schemas defined in `specs/2026-05-31-backend-agent/requirements.md` exactly.

---

## Definition of Done

- All automated test runs pass successfully locally and in the backend container.
- Verification checks for hermeticity (isolated mock behavior) are completed.
- Test assets are written cleanly inside standard `./backend/tests/` and `./backend/requirements.txt` is updated.
- The `specs/roadmap.md` Phase 3 entry remains untouched (it will be marked complete when this branch is implemented).
- The feature branch is clean, without uncommitted changes or extraneous temporary files.
