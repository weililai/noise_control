# 计算管道隔声套在各频段中心频率的插入损失，并输出 插入损失-频率 折线图，为了与标准隔声等级比较，同时输出了标准隔声等级最小插入损失。
# 该程序的使用方法：在本文件的“# 常量及隔声套的几何参数、材料参数、声波频带中心频率”一段里设置需要的变量，在终端(Terminal)里输入“python<"IL_of_pipe_lagging(Hale+Michelsen).py" > printout.txt”即可
# 输出的文件有：①图片 IL.png；②文本 printout.txt
# 主要参考：[Engineering Noise Control] 4th p429-431,[GB/T 31013-2014 声学 管道、阀门和法兰的隔声] p19 附录A
# 版本：20190829
# 魏里来 weililai@foxmail.com

import numpy as np
import matplotlib.pyplot as plt

# 常量及隔声套的几何参数、材料参数、声波频带中心频率
pi = 3.141592654  #圆周率
T = 20  #温度
c = 331 + 0.6*T  #空气声速
E = 69*10**9  #铝壳杨氏模量
niu = 0.34  #铝的泊松比
rho = 2.7*10**3  #铝的密度
D = 0.3  #裸管道直径
l = 0.1  #吸声层厚
h2 = 0.01  #隔声毡层厚
m2 = 2  #隔声毡层面密度
f = np.array([125,250,500,1000,2000,4000,8000])  #声波频带中心频率

h3 = 0.3*10**(-3)  #铝壳厚
d = D+2*l+2*h2+2*h3  #隔声套外径
B = E*h3**3/(12*(1 - niu**2))  #弯曲刚度
m3 = rho*h3  #铝壳层面密度
m = m2+m3  #隔声毡+铝壳的总面密度
c_L = 12**0.5/h3*(B/m3)**0.5  #铝壳中纵波速度
f_r = c_L/pi/d  #铝壳环频率
f_c = c*c/2/pi*(m3/B)**0.5  #铝壳临界频率


# 下面计算隔声套在各频段中心频率的插入损失,公式来源：[[Engineering Noise Control] p429-413 8.6.2]
# IL = 10*np.log10(1-0.012*X_r*np.sin(2*C_r)+(0.012*X_r*np.sin(C_r))**2)  #300Hz以下插入损失IL公式
# IL = (40/(1+0.12/D))*np.log10((f*(m*l)**0.5)/132)  #300Hz以上IL公式

IL = np.zeros(7)
xi_r = np.zeros(7)
X_r = np.zeros(7)
C_r = np.zeros(7)
i = 0
while i <7 :
    if f[i] <300 :  # 频率在300Hz以下
        xi_r[i] = f[i]/f_r  #IL公式所需局部量
        X_r[i] = (1000*(m/d)**0.5*(xi_r[i] - xi_r[i]**2)**0.5) - (2*d/(l*xi_r[i]))  #IL公式所需局部量
        C_r[i] = 30*xi_r[i]*l/d  #IL公式所需局部量
        IL[i] = 10*np.log10(1-0.012*X_r[i]*np.sin(2*C_r[i])+(0.012*X_r[i]*np.sin(C_r[i]))**2)
    else :  # 频率在300Hz以上
        IL[i] = (40/(1+0.12/D))*np.log10((f[i]*(m*l)**0.5)/132)
    i += 1

# 输出各物理量及插入损失 IL
print("T , c , E , niu , rho , D , l , h2 , h3 , d , m2 , m3 , m :")
print(round(T,4),round(c,4),round(E,4),round(niu,4),round(rho,4),round(D,4),round(l,4),round(h2,4),round(h3,4),round(d,4),round(m2,4),round(m3,4),round(m,4))
print("            ")
#print(B,m,c_L,f_r,f_c,xi_r,X_r,)
#print("            ")
print("Insertion loss (IL):")
np.set_printoptions(formatter={'float': '{: 0.1f}'.format})  #设定输出的数值保留一位小数
print("f  = ",f,"Hz")
print("IL = ",IL,"dB")

# 各隔声等级要求的最小插入损失,来源：[GB/T 31013-2014 声学 管道、阀门和法兰的隔声] 附录A
j =0
f0 =1
A1 = np.zeros(7)
A2 = np.zeros(7)
A3 = np.zeros(7)
B1 = np.zeros(7)
B2 = np.zeros(7)
B3 = np.zeros(7)
C1 = np.zeros(7)
C2 = np.zeros(7)
C3 = np.zeros(7)
while j < 7 :
    if f[j] <=250 and f[j] >=125 :
        A1[j] = -4
        A2[j] = -4
        A3[j] = 19*np.log10(f[j]/f0)-44
        B1[j] = 20*np.log10(f[j]/f0)-51
        B2[j] = 20*np.log10(f[j]/f0)-51
        B3[j] = 30*np.log10(f[j]/f0)-70
        C1[j] = 13*np.log10(f[j]/f0)-32
        C2[j] = 34*np.log10(f[j]/f0)-78
        C3[j] = 27*np.log10(f[j]/f0)-55.5
    elif f[j] <=500 and f[j] >250 :
        A1[j] = 22*np.log10(f[j]/f0)-57
        A2[j] = 22*np.log10(f[j]/f0)-57
        A3[j] = 19*np.log10(f[j]/f0)-44
        B1[j] = 20*np.log10(f[j]/f0)-51
        B2[j] = 30*np.log10(f[j]/f0)-75
        B3[j] = 30*np.log10(f[j]/f0)-70
        C1[j] = 39*np.log10(f[j]/f0)-94.5
        C2[j] = 34*np.log10(f[j]/f0)-78
        C3[j] = 27*np.log10(f[j]/f0)-55.5
    elif f[j] <=2000 and f[j] >500 :
        A1[j] = 22*np.log10(f[j]/f0)-57
        A2[j] = 22*np.log10(f[j]/f0)-57
        A3[j] = 19*np.log10(f[j]/f0)-44
        B1[j] = 27*np.log10(f[j]/f0)-70
        B2[j] = 30*np.log10(f[j]/f0)-75
        B3[j] = 30*np.log10(f[j]/f0)-70
        C1[j] = 39*np.log10(f[j]/f0)-94.5
        C2[j] = 34*np.log10(f[j]/f0)-78
        C3[j] = 27*np.log10(f[j]/f0)-55.5
    else :
        A1[j] = 22*np.log10(f[j]/f0)-57
        A2[j] = 22*np.log10(f[j]/f0)-57
        A3[j] = 19*np.log10(f[j]/f0)-44
        B1[j] = 27*np.log10(f[j]/f0)-70
        B2[j] = 30*np.log10(f[j]/f0)-75
        B3[j] = 22*np.log10(f[j]/f0)-43.5
        C1[j] = 13.5*np.log10(f[j]/f0)-10.5
        C2[j] = 13.5*np.log10(f[j]/f0)-10.5
        C3[j] = 13.5*np.log10(f[j]/f0)-10.5
    j += 1
# 输出各隔声等级要求的最小插入损失
print("A1 = ",A1,"dB")
print("A2 = ",A2,"dB")
print("A3 = ",A3,"dB")
print("B1 = ",B1,"dB")
print("B2 = ",B2,"dB")
print("B3 = ",B3,"dB")
print("C1 = ",C1,"dB")
print("C2 = ",C2,"dB")
print("C3 = ",C3,"dB")


# 作隔声量与频率的关系图
fstr = [str(f[i]) for i in range(len(f))]  #倍频程数值转字符串，方便在坐标轴上均匀排布（倍频程在普通线性递增坐标轴上刻度不均匀）
label_str = "IL (lagging Φ=" + str(round(d,4)) + "m ,φ=" + str(round(D,1)) + "m)"
plt.title("IL of pipe lagging")
plt.plot(fstr, IL, label=label_str,marker='o')
if D <0.3 :
    plt.plot(fstr, A1, label='A1')
    plt.plot(fstr, B1, label='B1')
    plt.plot(fstr, C1, label='C1')
if D >=0.3 and D <0.65 :
    plt.plot(fstr, A2, label='A2')
    plt.plot(fstr, B2, label='B2')
    plt.plot(fstr, C2, label='C2')
if D >=0.65 and D <1 :
    plt.plot(fstr, A3, label='A3')
    plt.plot(fstr, B3, label='B3')
    plt.plot(fstr, C3, label='C3')
plt.legend() # 给曲线添加图例
plt.xlabel('Frequency / Hz')
plt.ylabel('Insertion loss (IL) / dB')
#plt.show()
plt.savefig('IL.png')

exit(0)
