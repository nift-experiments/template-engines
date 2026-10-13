#!/bin/sh
set -eu
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
npm ci --ignore-scripts
revision=${NIFT_SOURCE_SHA:-$(python3 -c 'import json;print(json.load(open("docs/VERSIONS.json"))["nift_source"])')}
if [ ! -d work/nift-source/.git ]; then
 mkdir -p work
 git clone https://github.com/nift-dev/nift.git work/nift-source
fi
test "${#revision}" -eq 40
case "$revision" in *[!0-9a-f]*) echo "NIFT_SOURCE_SHA must be a full SHA" >&2; exit 1;; esac
git -C work/nift-source checkout --detach "$revision"
test "$(git -C work/nift-source rev-parse HEAD)" = "$revision"
test -z "$(git -C work/nift-source status --porcelain)"
make -C work/nift-source -j4 embed
g++ -std=c++17 -O2 -pthread -Iwork/nift-source/include adapters/nift.cpp work/nift-source/libnift_c.a -ldl -o work/nift-adapter
