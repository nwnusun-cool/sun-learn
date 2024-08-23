import argparse

import paramiko
import os
from stat import S_ISDIR as isdir

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='远程文件下载脚本')
    parser.add_argument('--host', type=str, required=True, help='远程服务器地址')
    parser.add_argument('--user', type=str, required=True, help='用户名')
    parser.add_argument('--password', type=str, required=True, help='密码')
    parser.add_argument('--port', type=int, default=22, help='远程服务器端口，默认为22')
    parser.add_argument('--remote_dir', type=str, required=True, help='远程文件目录')
    parser.add_argument('--local_dir', type=str, required=True, help='本地文件存放目录')
    return parser.parse_args()
def down_from_remote(sftp_obj, remote_dir_name, local_dir_name):
    """远程下载文件"""
    remote_file = sftp_obj.stat(remote_dir_name)
    if isdir(remote_file.st_mode):
        # 文件夹，不能直接下载，需要继续循环
        check_local_dir(local_dir_name)
        print('开始下载文件夹：' + remote_dir_name)
        for remote_file_name in sftp.listdir(remote_dir_name):
            sub_remote = os.path.join(remote_dir_name, remote_file_name)
            sub_remote = sub_remote.replace('\\', '/')
            sub_local = os.path.join(local_dir_name, remote_file_name)
            sub_local = sub_local.replace('\\', '/')
            down_from_remote(sftp_obj, sub_remote, sub_local)
    else:
        # 文件，直接下载
        print('开始下载文件：' + remote_dir_name)
        sftp.get(remote_dir_name, local_dir_name)


def check_local_dir(local_dir_name):
    """本地文件夹是否存在，不存在则创建"""
    if not os.path.exists(local_dir_name):
        os.makedirs(local_dir_name)


if __name__ == "__main__":
    """程序主入口"""
    args = parse_args()

    # 使用命令行参数替换硬编码的变量
    host_name = args.host
    user_name = args.user
    password = args.password
    port = args.port
    remote_dir = args.remote_dir
    local_dir = args.local_dir

    # 连接远程服务器
    t = paramiko.Transport((host_name, port))
    t.connect(username=user_name, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    # 远程文件开始下载
    down_from_remote(sftp, remote_dir, local_dir)
    # 关闭连接
    t.close()


