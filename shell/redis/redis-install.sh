#! /bin/bash 


check_port() {
    local port=$1  # 获取传入的端口号参数

    if ss -tln | grep -q ":$port "; then  # 判断端口是否被占用
        echo "Port $port is already in use, exiting..."
        exit 1  # 如果端口已被占用则退出脚本
    else
        echo "Port $port is available"
    fi
}

port=6379
check_port $port
 
yum install -y wget nmap unzip wget lsof xz net-tools gcc make gcc-c++

cd /usr/local/src
rm -rf redis-$1
wget http://download.redis.io/releases/redis-$1.tar.gz
tar zxvf redis-$1.tar.gz
cd redis-$1
make -j 4 
make install PREFIX=/usr/local/redis-$1

cat >/usr/local/redis-$1/redis.conf<<EOF
daemonize yes
bind 0.0.0.0
requirepass password
port 6379
timeout 60
loglevel warning
databases 16
EOF

echo vm.overcommit_memory=1 >> /etc/sysctl.conf
sysctl -p

/usr/local/redis-$1/bin/redis-server /usr/local/redis-$1/redis.conf

if ! ss -lntp | grep 6379 | grep -v grep > /dev/null; then
    echo "Install failed"
else
    echo "Install successfully"
fi
