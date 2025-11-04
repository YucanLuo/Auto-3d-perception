#!/usr/bin/env bash
set -e
python -m ipykernel install --user --name=pt3d || true
exec jupyter lab \
  --ip=0.0.0.0 --port=8888 --no-browser \
  --ServerApp.token='' --ServerApp.password='' \
  --allow-root
