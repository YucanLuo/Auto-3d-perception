FROM nvidia/cuda:12.1.1-cudnn9-devel-ubuntu22.04

# 基础工具
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    wget git nano build-essential curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 安装 Miniconda（也可换 mambaforge）
ENV CONDA_DIR=/opt/conda
RUN wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/mc.sh && \
    bash /tmp/mc.sh -b -p $CONDA_DIR && \
    rm /tmp/mc.sh
ENV PATH=$CONDA_DIR/bin:$PATH

# 设置工作目录并复制环境文件
WORKDIR /workspace
COPY env/environment.yml /workspace/env/environment.yml

# 创建 conda 环境并清理
RUN conda env create -f /workspace/env/environment.yml && conda clean -afy
# 激活默认环境
SHELL ["bash", "-lc"]
RUN echo "conda activate pt3d" >> ~/.bashrc
ENV CONDA_DEFAULT_ENV=pt3d
ENV PATH=$CONDA_DIR/envs/pt3d/bin:$PATH

# Jupyter 端口
EXPOSE 8888

# 默认进入 bash
CMD [ "bash" ]
