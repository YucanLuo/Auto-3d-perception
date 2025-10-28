#!/usr/bin/env bash
set -e

# 可选：注册内核名称
python -m ipykernel install --user --name=pt3d || true

# 启动 JupyterLab（允许 root，禁用鉴权，监听 0.0.0.0:8888）
exec jupyter lab \
  --ip=0.0.0.0 \
  --port=8888 \
  --no-browser \
  --ServerApp.token='' \
  --ServerApp.password='' \
  --allow-root
