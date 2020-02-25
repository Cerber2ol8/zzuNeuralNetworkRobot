# zzuNeuralNetworkRobot

基于卷积神经网络的巡线机器人，使用的框架 Tensorflow Keras tf版本1.12.0  
使用了 hamuchiwa/AutoRCCar 的部分代码  

# 项目介绍
代码自从去年参加完比赛就没怎么看过了，描述可能不怎么清晰  
其中包含最初的巡线arduino小车和后来的机器人  
主要都用的是树莓派，摄像头到的图片，处理后用神经网络模型识别，返回 0. 1. 2. 代表 前进和左右转向  
然后树莓派发送串口消息给arduino或舵机控制板执行事先预设的动作或动作组  
其中PC文件夹存放的是   树莓派arduino小车使用的代码，在hamuchiwa/AutoRCCar基础上做了改动  
RaspberryPi\Robot文件夹存放的是  机器人项目所使用的代码。重写了收集数据的代码，根据舵机串口通信协议写了调用的库。  
根据机器人的运动情况写了一部分运动逻辑，以及一些调试工具  

#  RaspberryPi\Robot\ 里需要注意的文件
 CommandDriver_udp.py  用于树莓派接收PC指令，串流或者远程调试运动的时候必要  
 config.py     全局设置  
 img_augment.py    用于预处理数据集  
 model.py    定义卷积神经网络模型  
 my_collect_data.py    用于收集数据，需在PC端运行，在收集串流图像的同时保存标签信息到/images/imgs_xxx_xxx/label_arrary_xxx.npz  
 nn_training_conv.py 用于训练cnn模型，前提是预处理数据完成  
 PyServo.py  用于支持与舵机控制板通信的库  
 Readkey.py  用于PC远程测试运动的工具  
 run.py      机器人执行的主程序  
 Servo_Test.py   用于树莓派机器人测试串口连接  
	

# 项目结构
		PC────树莓派─────舵机控制板────舵机控制

#  大致工作流
   # 图像收集
      TBD
   # 数据处理
      TBD
   # 模型加载
      TBD
   # 运行
      TBD
    

	



			by lcy
