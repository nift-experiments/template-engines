#!/bin/sh
set -eu
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq build-essential git python3-venv curl xz-utils ca-certificates autoconf automake libtool pkg-config
mkdir -p /opt/node
cd /opt/node
curl -fsSLO https://nodejs.org/dist/v22.22.1/node-v22.22.1-linux-x64.tar.xz
curl -fsSLO https://nodejs.org/dist/v22.22.1/SHASUMS256.txt
rgpattern='node-v22.22.1-linux-x64.tar.xz'
grep " $rgpattern\$" SHASUMS256.txt | sha256sum -c -
tar -xf node-v22.22.1-linux-x64.tar.xz --strip-components=1
ln -sf /opt/node/bin/node /usr/local/bin/node
ln -sf /opt/node/bin/npm /usr/local/bin/npm
cd /opt/template-engines
./scripts/build.sh
uname -a > work/kernel.txt
df -T . > work/filesystem.txt
dpkg-query -W > work/packages.txt
python3 scripts/certify.py > work/cloud-certification.log 2>&1
