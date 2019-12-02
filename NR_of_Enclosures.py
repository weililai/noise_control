# NR_of_Enclosures, 可以计算厂房内的隔声罩在各频段的降噪量；已知设备声功率级可以计算罩内外声压级。（物理量使用SI国际单位制）
'''
# 该程序的使用方法：在本文件的设置段落里设置需要的变量;
  在终端(Terminal)里输入“python<"NR_of_Enclosures.py" >NR_report.txt”,回车
# 输出的文件：文本 NR_report.txt
# 主要参考：[Engineering Noise Control] 5th p407-410
# 版本：20191118
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
S_E = 200 #隔声罩外表面积
S_i = 200 #隔声罩内表面积（包括设备表面）
S = 10000 #厂房内表面积
D_Theta = 2 #声指向系数
alpha_bar_i = np.array([0.1,0.2,0.25,0.3,0.35,0.4,0.4]) #罩内平均吸声系数
alpha_bar = np.array([0.01,0.01,0.01,0.02,0.02,0.02,0.03]) #厂房平均吸声系数，参考[Engineering Noise Control] 5th p411 calculations for example7.4
TL = np.array([11,12,15,18,23,25,30]) #墙体传输损失
L_W = np.array([93,96,99,102,105,102,99]) #设备声功率级
NR = np.zeros(7)
#设置段落完毕

#计算段落
R = S_i*alpha_bar_i/(1-alpha_bar_i) #enclosures room constant
R_room = S*alpha_bar/(1-alpha_bar) #room constant
C = 10*np.log10(0.3+S_E*(1-alpha_bar_i)/(S_i*alpha_bar_i)) #coefficient,C
L_p = L_W + 10*np.log10(D_Theta/(4*pi*r*r + 4/R)) + 10*np.log10(Rho_multiply_c/400) #罩内距声源r处的声压级
L_p1 = L_W - TL -10*np.log10(S_E)  + 10*np.log10(Rho_multiply_c/400) + C #罩外近点声压级(不考虑厂房回声时)
L_Wt = L_p1 + 10*np.log10(S_E) - 10*np.log10(Rho_multiply_c/400) #从罩面向外辐射的声功率级
L_p2 = L_Wt + 10*np.log10(D_Theta/(4*pi*r2*r2) + 4/R_room) + 10*np.log10(Rho_multiply_c/400) #对于厂房内的隔声罩，罩外距声源r2处的声压级（考虑了厂房回声）
L_p2_without_room = L_p1 + 10*np.log10(S_E) + 10*np.log10(D_Theta/(4*pi*r2*r2)) #对于室外隔声罩，罩外距声源r2处的声压级
NR = TL - C #降噪量（各频带）
L_p2_prime = NR + L_p2 #未做隔声处理时，距声源r2处的声压级
NR_total = 10*np.log10(np.sum(10**(NR/10) ) ) #总降噪量
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
print("   NR_total      :    ",round(NR_total,1),"dB")
#输出段落完毕

exit(0)