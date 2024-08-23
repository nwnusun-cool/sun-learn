#! /bin/bash 
# x86架构、jdk1.8

cd /usr/local/src
yum -y install wget
wget https://repo.huaweicloud.com/java/jdk/8u181-b13/jdk-8u181-linux-x64.tar.gz

tar -xvf jdk-8u181-linux-x64.tar.gz

echo 'export JAVA_HOME=/usr/local/src/jdk1.8.0_181'  >>/etc/profile
echo 'export PATH=$PATH:$JAVA_HOME/bin'  >>/etc/profile 
echo 'export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar'  >>/etc/profile

source /etc/profile 
java -version

if [ $? = 0 ];then
   echo "ok"
fi
