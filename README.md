# Auto-3d-perception
Resource-aware 3D perception for automotive systems
# Auto 3D Perception (Resource-Aware)

## Quick Start
```bash
# 1) build
docker compose build
# 2) run container
docker compose up -d
# 3) attach shell
docker exec -it auto3d-dev bash
# 4) in container: sanity check
python scripts/sanity_check.py
# 5) start Jupyter Lab
bash scripts/run_jupyter.sh
# open http://localhost:8888
