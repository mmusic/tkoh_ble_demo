from socket import *
import time
import json
host  = '127.0.0.1' # 这是客户端的电脑的ip
# host  = '143.89.50.151' # 这是客户端的电脑的ip
port = 4000 #接口选择大于10000的，避免冲突
bufsize = 2048  #定义缓冲大小

addr = (host,port) # 元祖形式
udpClient = socket(AF_INET,SOCK_DGRAM) #创建客户端
count = -72
axis_x = 0
axis_y = 7
direction = 0
while True:
    count = count + 1
    data = str(count)
    data2 = {
                'type': '1',
                'device': '1002',
                'ts': int(time.time()),
                'loc_x': axis_x,
                'loc_y': axis_y,
                'val': 0.9,
                'status': 1,
            }
    if axis_x < 87 and direction == 0:
        print("1", axis_x)
        axis_x = axis_x + 1
    elif axis_x == 87:
        if axis_y < 15:
            axis_y = axis_y + 1
            direction = 1

    if axis_y == 15:
        axis_x = axis_x - 1
        print("2", axis_x)

    if axis_x < 1:
        axis_x = 0
        axis_y = 7
        direction = 0

    udpClient.sendto(json.dumps(data2).encode(), addr) # 发送数据
    time.sleep(4)

udpClient.close()