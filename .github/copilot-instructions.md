## Quick orientation

This repository implements resource-aware 3D perception experiments for automotive systems.
Keep in mind these concrete locations and conventions when editing code or adding features:

- Primary code lives under `src/` with logical subpackages:
  - `src/data/` — data loaders and dataset helpers (contains `__init__.py`).
  - `src/models/` — model architectures and training code.
  - `src/utils/` — reusable utilities and helpers.
- Runtime/workflow artifacts:
  - `env/environment.yml` — (conda) environment spec kept here.
  - `Dockerfile` and `docker-compose.yml` — containerized development and run setups.
  - `scripts/` — lightweight runner scripts (e.g. `run_jupyter.sh`, `sanity_check.py`).
  - `experiments/` — experiment definitions/configs (store configs here).
  - `results/` — experiment outputs, metrics, and artifacts go here.

## How to run locally (discoverable patterns)

1. Environment
   - Preferred environment spec is `env/environment.yml` (Conda). Create with:
     - On Windows PowerShell: `$env:CONDA_DEFAULT_ENV; conda env create -f env/environment.yml` (or `conda env update -f env/environment.yml`).
   - If not using Conda, set `PYTHONPATH` to include the `src` directory so modules import as `src.*`:
     - PowerShell example: `$env:PYTHONPATH = 'src' ; python -c "import src; print('src on path')"`

2. Containers
   - A `Dockerfile` and `docker-compose.yml` are present; use these to reproduce env in CI or on a dev machine:
     - Build: `docker build -t auto3d .`
     - Compose: `docker-compose up --build`

3. Jupyter / interactive
   - A `scripts/run_jupyter.sh` exists as the canonical launcher for notebooks. If it's empty, prefer using the container or manual invocation (with `PYTHONPATH=src`) to ensure import paths work.

## Code and contribution patterns agents should follow

- Prefer small, focused edits under `src/`. New modules belong in the appropriate package (data, models, utils).
- When adding runnable scripts, place them under `scripts/` and keep them idempotent and parameterized (use CLI args or environment variables).
- Experiments: register experiment configs under `experiments/` and write outputs to `results/` to keep runs reproducible.

## Import / module-resolution details

- The repository uses a `src/`-centric layout. When running modules or tests locally, ensure `src` is on `PYTHONPATH` (or install the package into the environment).
- Examples of safe invocations (PowerShell):
  - `$env:PYTHONPATH='src'; python -m src.models.train --config experiments/my_exp.yaml`

## Things NOT to assume

- There are minimal/empty helper scripts and config files (e.g. `scripts/run_jupyter.sh`, `env/environment.yml`, `Dockerfile`, `docker-compose.yml`) — they are place-holders; verify with the repo owner before changing CI-critical flows.
- No tests or CI configs were found; do not presume a test harness exists.

## Quick heuristics for edits

- If changing model or dataset code, also update an example experiment under `experiments/` to demonstrate usage and add a short note in `README.md` describing the change.
- Store large datasets outside the repository and reference them via a config in `experiments/` (do not add data to `src/` or commit large binary files to `results/`).

## Files to inspect for deeper context

- `src/` (all subpackages)
- `scripts/` (runner scripts)
- `env/environment.yml` (environment spec)
- `Dockerfile`, `docker-compose.yml`
- `experiments/` and `results/`

If anything above is unclear or you want the agent to edit/complete placeholder scripts (e.g. populate `scripts/run_jupyter.sh` or `env/environment.yml`), tell me which workflow you want implemented and I will update files and run quick verification steps.
