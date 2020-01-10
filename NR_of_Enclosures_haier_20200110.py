# NR_of_Enclosures, 可以计算厂房内的隔声罩在各频段的降噪量；已知设备声功率级可以计算罩内外声压级。（物理量使用SI国际单位制）
'''
# 该程序的使用方法：在本文件的设置段落里设置需要的变量;
  在终端(Terminal)里输入“python<"NR_of_Enclosures_haier_20200110.py" >NR_report.txt”,回车
# 输出的文件：文本 NR_report.txt
# 方法主要参考：[Engineering Noise Control] 5th p407-410；声学技术《基于声电类比的多层结构隔声量算法》
# 版本：20191226
# 作者：魏里来 weililai@foxmail.com
'''

import numpy as np
import matplotlib.pyplot as plt

#设置段落
pi = 3.141592654  #圆周率
Rho_multiply_c = 414  #20摄氏度下，空气密度乘以空气声速的近似结果
f = np.array([125,250,500,1000,2000,4000,8000])  #倍频带中心频率
r = 2  #罩内测点与声源的距离
r2 = 6  #罩外测点与声源的距离
S_E = 100 #隔声罩外表面积
S_i = 100 #隔声罩内表面积（包括设备表面）
S = 10000 #厂房内表面积
D_Theta = 2 #声指向系数
alpha_bar_i = np.array([0.1,0.2,0.25,0.3,0.35,0.4,0.4]) #罩内平均吸声系数
alpha_bar = np.array([0.01,0.01,0.01,0.02,0.02,0.02,0.03]) #普通硬壁厂房平均吸声系数，参考[Engineering Noise Control] 5th p411 calculations for example7.4
#墙体材料隔声性能及门窗开口组合设定
TL_blanket = np.array([40.0,41.2,39.0,34.0,44.7,41.2,40.0]) #由CAS-AP的隔声量测试数据得来
TL_22g_steel = np.array([8,14,20,23,26,27,35]) #22g钢板隔声量，出处：[Engineering Noise Control] 5th p399
TL_wall = np.zeros(7) #不直接设定墙体隔声量，通过墙体中各层材料隔声量计算墙体隔声量，墙体隔声量也可用下一行直接设定
# TL_wall = np.array([40.0,41.2,39.0,34.0,44.7,41.2,40.0]) #墙体隔声量也可在这里直接设定，设定时替换掉上一行
S_wall = 100 #隔声墙面积
TL_windows = np.array([25,30,33,35,34,34,35]) #窗隔声量
S_windows = 2 #窗面积
TL_door = np.array([26,26,28,32,32,40,40]) #“2-skin metal door”门隔声量，出处：[Engineering Noise Control] 5th p403 “2-skin metal door”
S_door = 2 #门面积
TL_open = np.zeros(7) #开口隔声量，自然是全零
S_open = 0.1 #开口面积
#TL = np.array([11,12,15,18,23,25,30]) #组合传输损失,可直接由该行设置，默认是通过计算获得
L_W = np.array([93,96,99,102,105,102,99]) #设备声功率级
TL_porous = np.array([0,0,0,0.5,1.5,4,12]) #吸声材料附加隔声量
#设置段落完毕

#计算段落
#计算平均传输损失TL
tau_blanket = 1/(10**(TL_blanket/10))
tau_22g_steel = 1/(10**(TL_22g_steel/10))
TL_wall = 10*np.log10(2*(1/tau_blanket+1/tau_22g_steel))+TL_porous #计算“毡+钢板”墙体的传输损失，出处：声学技术《基于声电类比的多层结构隔声量算法》，这里还擅自增加了吸声材料的附加隔声量TL_porous。（若墙体隔声量是直接设定的，不需要该行）
tau_wall = 1/(10**(TL_wall/10))
tau_windows = 1/(10**(TL_windows/10))
tau_door = 1/(10**(TL_door/10))
tau_open =  1/(10**(TL_open/10))
tau_bar = (tau_wall*S_wall+tau_windows*S_windows+tau_door*S_door+tau_open*S_open)/(S_wall+S_windows+S_door+S_open)
TL_bar = 10*np.log10(1/tau_bar) #组合隔声量（组合传输损失或平均传输损失），出处：[Engineering Noise Control] 5th p398
TL = TL_bar #用于计算隔声罩降噪量所需的平均传输损失，若TL在设定段落已经设置，就应去掉该行
#计算各位置声压级及隔声罩的降噪量
R = S_i*alpha_bar_i/(1-alpha_bar_i) #enclosures room constant
R_room = S*alpha_bar/(1-alpha_bar) #room constant
C = 10*np.log10(0.3+S_E*(1-alpha_bar_i)/(S_i*alpha_bar_i)) #coefficient,C
L_p = L_W + 10*np.log10(D_Theta/(4*pi*r*r + 4/R)) + 10*np.log10(Rho_multiply_c/400) #罩内距声源r处的声压级
L_p1 = L_W - TL -10*np.log10(S_E)  + 10*np.log10(Rho_multiply_c/400) + C #罩外近点声压级(不考虑厂房回声时)
L_Wt = L_p1 + 10*np.log10(S_E) - 10*np.log10(Rho_multiply_c/400) #从罩面向外辐射的声功率级
noise_A_weighting_corrections = np.array([-16.1,-8.6,-3.2,0,1.2,1.0,-1.1]) # A计权修正谱
L_p2 = L_Wt + 10*np.log10(D_Theta/(4*pi*r2*r2) + 4/R_room) + 10*np.log10(Rho_multiply_c/400) #对于厂房内的隔声罩，罩外距声源r2处的声压级（考虑了厂房回声）
L_p2_dBA = L_p2 + noise_A_weighting_corrections # 获得隔声处理后距声源r2处的A计权噪声级
L_p2_dBA_total = 10*np.log10(np.sum(10**(L_p2_dBA/10) ) ) # 获得隔声处理后距声源r2处的A计权噪声总值
L_p2_without_room = L_p1 + 10*np.log10(S_E) + 10*np.log10(D_Theta/(4*pi*r2*r2)) #对于室外隔声罩，罩外距声源r2处的声压级
NR = np.zeros(7)
NR = TL - C #降噪量（各频带）
L_p2_prime = NR + L_p2 #未做隔声处理时，距声源r2处的声压级
L_p2_prime_dBA = L_p2_prime + noise_A_weighting_corrections # 获得隔声处理前距声源r2处的A计权噪声级
L_p2_prime_dBA_total = 10*np.log10(np.sum(10**(L_p2_prime_dBA/10) ) ) # 获得隔声处理前距声源r2处的A计权噪声总值
NR_dBA_total = L_p2_prime_dBA_total - L_p2_dBA_total #总降噪量(隔声前后A计权噪声总值的差值)
#计算段落完毕

#输出段落
print("   r             :    ",r,"m")
print("   r2            :    ",r2,"m")
print("   S_E           :    ",S_E,"m2")
print("   S_i           :    ",S_i,"m2")
print("   S             :    ",S,"m2")
print("   D_Theta       :    ",D_Theta)
print("   alpha_bar_i   :    ",alpha_bar_i)
print("   alpha_bar     :    ",alpha_bar)
print("   TL            :    ",TL,"dB")
print("   L_W           :    ",L_W,"dB")
np.set_printoptions(formatter={'float': '{: 0.1f}'.format})  #设定输出的数值保留一位小数
print("NR_of_Enclosures :")
print("   f             :    ",f,"/s")
print("   L_p           :    ",L_p,"dB")
print("   L_p1          :    ",L_p1,"dB")
print("   L_p2_prime    :    ",L_p2_prime,"dB")
print("   L_p2          :    ",L_p2,"dB")
print("   L_p2_without_room: ",L_p2_without_room,"dB")
print("   C             :    ",C,"dB")
print("   NR            :    ",NR,"dB")
print("   NR_dBA_total  :    ",round(NR_dBA_total,1),"dB")
#输出段落完毕

exit(0)