import paramiko
import time
import socket
from paramiko.py3compat import u
import select
# 创建SSH对象
ssh = paramiko.SSHClient()
# 允许连接不在known_hosts文件上的主机
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# 连接服务器
ssh.connect(hostname="127.0.0.1", port=22, username="lixm", password="lixm")
chan = ssh.invoke_shell(height=30,width=200)
chan.settimeout(0.0)
while True:
        time.sleep(2)
        chan.send("pwd")
        break
chan.close()
ssh.close()
