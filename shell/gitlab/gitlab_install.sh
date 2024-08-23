#! /bin/bash 
# 系统:centos
# 作者：nwnusun
# 时间：2024年2月23日10:45:01

port=8888
version=$1
yum install -y wget curl policycoreutils-python openssh-server
systemctl enable sshd
systemctl start sshd

yum install -y postfix
sed -i 's/^inet_interfaces = .*/inet_interfaces = all/' /etc/postfix/main.cf
systemctl enable postfix
systemctl start postfix

cd /usr/local/src
wget https://mirrors.tuna.tsinghua.edu.cn/gitlab-ce/yum/el7/gitlab-ce-${version}-ce.0.el7.x86_64.rpm

rpm -ivh gitlab-ce-${version}-ce.0.el7.x86_64.rpm

# external_url 'http://192.168.100.17'
sed -i "s/^external_url.*/external_url 'http://0.0.0.0'/"  /etc/gitlab/gitlab.rb 
gitlab-ctl reconfigure
sed -i  "s/*:80;/*:$port;/" /var/opt/gitlab/nginx/conf/gitlab-http.conf 
gitlab-ctl restart

# 检查端口是否处于监听状态
netstat -tuln | grep ":$port " > /dev/null
if [ $? -eq 0 ]; then
    echo "端口 $port 已经启动，安装成功。"
else
    echo "端口 $port 未启动，安装可能出现问题。"
fi
