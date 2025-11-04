# 用 Mambaforge 做基础（自带 conda/mamba，解析稳定）
FROM condaforge/mambaforge:24.3.0-0

# 基础工具
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    git nano ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# 更稳的解析设置
SHELL ["/bin/bash", "-lc"]
RUN conda config --set channel_priority flexible

WORKDIR /workspace
COPY env/environment.yml /workspace/env/environment.yml

# 用 mamba 一步创建 pt3d 环境（快、稳）
RUN mamba env create -f /workspace/env/environment.yml && \
    mamba clean -a -y && \
    echo "source /opt/conda/etc/profile.d/conda.sh && conda activate pt3d" >> /root/.bashrc

# 拷贝项目
COPY . /workspace

EXPOSE 8888
CMD [ "bash" ]
