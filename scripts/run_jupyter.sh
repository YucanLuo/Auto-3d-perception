#!/bin/bash
# ==========================================
# 自动启动 Jupyter Lab (for Auto3D / pt3d)
# ==========================================

# 默认端口
PORT=8888

# 检查端口是否被占用
if lsof -i:$PORT >/dev/null 2>&1; then
    echo "⚠️  Port $PORT is already in use. Switching to 8889..."
    PORT=8889
fi

# 激活 conda 环境
source /opt/conda/etc/profile.d/conda.sh
conda activate pt3d

# 显示当前环境信息
echo "✅ Activated conda environment: $(conda info --envs | grep '*' | awk '{print $1}')"
echo "📂 Working directory: $(pwd)"
echo "🌐 Launching JupyterLab on port: $PORT"

# 启动 Jupyter Lab
jupyter lab \
    --ip=0.0.0.0 \
    --port=$PORT \
    --allow-root \
    --no-browser \
    --NotebookApp.token='' \
    --NotebookApp.password='' \
    --notebook-dir=/workspace
