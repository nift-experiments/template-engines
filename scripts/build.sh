#!/bin/sh
set -eu
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
npm ci --ignore-scripts
revision=$(python3 -c 'import json;print(json.load(open("docs/VERSIONS.json"))["nift_source"])')
if [ ! -d work/nift-source/.git ]; then
 mkdir -p work
 git clone https://github.com/nift-dev/nift.git work/nift-source
fi
git -C work/nift-source checkout --detach "$revision"
make -C work/nift-source -j4 embed
g++ -std=c++17 -O2 -pthread -Iwork/nift-source/include adapters/nift.cpp work/nift-source/libnift_c.a -ldl -o work/nift-adapter
