# 基于官方 PyTorch 镜像（已包含 PyTorch + CUDA 12.1 + cuDNN 8）
FROM pytorch/pytorch:2.3.1-cuda12.1-cudnn8-devel

# 基础工具
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    git nano curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 工作目录
WORKDIR /workspace
COPY . /workspace

# Python 依赖（用 pip，避免 conda 解析失败）
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
        numpy scipy scikit-learn matplotlib pandas pyyaml tqdm ipykernel open3d

# Jupyter 端口
EXPOSE 8888

# 默认进入 bash
CMD ["bash"]

