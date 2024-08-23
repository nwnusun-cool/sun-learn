#! /bin/bash

set -e
cd /opt/
wget https://mirrors.aliyun.com/golang/go1.20.linux-amd64.tar.gz
tar zxvf go1.20.linux-amd64.tar.gz
mkdir -p /opt/gopath/{bin,src}
cat >>/etc/profile<<EOF
export GOROOT=/opt/go
export GOPATH=/opt/gopath
export PATH=\$PATH:/opt/gopath/bin:/opt/go/bin
EOF
source  /etc/profile
go version