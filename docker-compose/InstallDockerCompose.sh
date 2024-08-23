#! /bin/bash
# Compose目前已经完全支持Linux、Mac OS和Windows，在我们安装Compose之前，需要先安装Docker。下面我 们以编译好的二进制包方式安装在Linux系统中。 
# curl -L https://github.com/docker/compose/releases/download/v$1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
 
curl -L https://nwnusun.oss-cn-beijing.aliyuncs.com/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
# 查看版本信息 
docker-compose version
echo "ok"
