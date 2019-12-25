#该程序计算组合隔声量（墙体不完整，有门窗及开口时，根据声平均透射系数得到的隔声量）
import numpy as np

#设定部分
TL_blanket = np.array([40.0,41.2,39.0,34.0,44.7,41.2,40.0]) #由CAS-AP的隔声量测试数据得来
TL_22g_steel = np.array([8,14,20,23,26,27,35]) #22g钢板隔声量，出处：[Engineering Noise Control] 5th p399
TL_wall = np.zeros(7) #不设定墙体隔声量，通过墙体中各层材料隔声量计算墙体隔声量
# TL_wall = np.array([40.0,41.2,39.0,34.0,44.7,41.2,40.0]) #墙体隔声量也可在这里直接设定，设定时替换掉上一行
S_wall = 200 #隔声墙面积
TL_windows = np.array([25,30,33,35,34,34,35]) #窗隔声量
S_windows = 2 #窗面积
TL_door = np.array([26,26,28,32,32,40,40]) #门隔声量，出处：[Engineering Noise Control] 5th p403 “2-skin metal door”
S_door = 2 #门面积
TL_open = np.zeros(7) #开口隔声量，全零
S_open = 0.2 #开口面积

#计算部分
tau_blanket = 1/(10**(TL_blanket/10))
tau_22g_steel = 1/(10**(TL_22g_steel/10))
TL_wall = 10*np.log10(2*(1/tau_blanket+1/tau_22g_steel)) #计算“毡+钢板”墙体的隔声量，出处：声学技术《基于声电类比的多层结构隔声量算法》（若墙体隔声量是直接设定的，不需要该行）
tau_wall = 1/(10**(TL_wall/10))
tau_windows = 1/(10**(TL_windows/10))
tau_door = 1/(10**(TL_door/10))
tau_open =  1/(10**(TL_open/10))
tau_bar = (tau_wall*S_wall+tau_windows*S_windows+tau_door*S_door+tau_open*S_open)/(S_wall+S_windows+S_door+S_open)
TL_bar = 10*np.log10(1/tau_bar) #R即TL，组合隔声量，出处：[Engineering Noise Control] 5th p398

#输出
print("TL_wall : ",TL_wall,"dB")
print("TL_bar  : ",TL_bar,"dB")