项目结构
		PC────TCP/IP────树莓派─────Serial────Arduino────舵机控制
host		192.168.1.4	192.168.1.12	
tcp(stream)	server:8000	client
udp(cmd)		client		server:8001

PC监听按键	
	stream.py────────readkey.py
host	127.0.0.1		127.0.0.1
udp	server:9870	client	
	


my_collect_data.py
主线程 监听键盘消息
	子线程1 收集串流
	子线程2 upd发送command


			by lcy