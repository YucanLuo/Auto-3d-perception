#!/usr/bin/env bash
set -e
source /opt/conda/etc/profile.d/conda.sh
conda activate pt3d
python -m ipykernel install --user --name=pt3d
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token='' --NotebookApp.password=''
