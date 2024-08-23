#! /bin/bash 

# 问题：采用yum安装mysql，重装的时候需要卸载干净，不然在脚本修改密码的时候会报错
# rm -rf /etc/my.cnf /usr/share/mysql /var/lib/mysql 

check_port() {
    local port=$1  # 获取传入的端口号参数

    if ss -tln | grep -q ":$port "; then  # 判断端口是否被占用
        echo "Port $port is already in use, exiting..."
        exit 1  # 如果端口已被占用则退出脚本
    else
        echo "Port $port is available"
    fi
}

check_port 3306

if type mysql >/dev/null 2>&1;then
   echo "mysql exists!"
   exit 1
fi

rm -rf /etc/my.cnf /usr/share/mysql /var/lib/mysql

EL_VERSION=$(rpm -E %rhel)
MYSQL_REPO_URL="https://repo.mysql.com/mysql80-community-release-el$EL_VERSION-1.noarch.rpm"
yum -y install $MYSQL_REPO_URL
yum -y install mysql-community-server  --nogpgcheck 
systemctl start mysqld

if [ $? != 0 ];then
    exit 1
fi

pwd=`grep 'temporary password' /var/log/mysqld.log | tail -n 1 | awk '{print$NF}'`

echo "密码：$pwd"
#cat >/tmp/mysql_sql<<EOF
#alter user 'root'@'localhost'  identified by  'Mypwd@123';
# use mysql;
# update user set host = '%' where user ='root';
#EOF


mysql -uroot -h 127.0.0.1 -P 3306 -p$pwd --connect-expired-password <<EOF
 alter user 'root'@'localhost'  identified by  'Mypwd@123';
 use mysql;
 update user set host = '%' where user ='root';
 exit
EOF

if ! ss -lntp | grep 3306 | grep -v grep >/dev/null;then
  echo "Install failed"
fi
echo "Install successfully"

echo "默认端口：3306  密码：Mypwd@123"
