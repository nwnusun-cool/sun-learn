#!/bin/bash
# 安装必要软件包
yum install -y wget gcc zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel libffi-devel

# 指定Python版本号
PYTHON_VERSION=$1

# 下载并安装指定版本的Python
cd /usr/local/src
wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz
tar -xvJf Python-$PYTHON_VERSION.tar.xz
mkdir -p /usr/local/python$PYTHON_VERSION
cd Python-$PYTHON_VERSION
./configure --prefix=/usr/local/python$PYTHON_VERSION
make && make install

# 设置软连接
ln -s /usr/local/python$PYTHON_VERSION/bin/python3 /usr/local/bin/python3
ln -s /usr/local/python$PYTHON_VERSION/bin/pip3 /usr/local/bin/pip3

# 显示Python和pip版本
python3 -V
pip3 -V
