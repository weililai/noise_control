# 计算管道隔声套在各频段中心频率的插入损失，并输出 插入损失-频率 折线图，为了与标准隔声等级比较，同时输出了标准隔声等级最小插入损失，最后判断该隔声套隔声级别。物理量使用国际SI国际单位制
'''
# 该程序的使用方法：在本文件的“# 常量及隔声套的几何参数、材料参数、声波频带中心频率”一段里设置需要的变量;
  在终端(Terminal)里输入“python<"IL_of_pipe_lagging(Hale+Michelsen).py" >level_report.txt”,回车
# 输出的文件有：①图片 IL of pipe lagging.png；②文本 level_report.txt
# 主要参考：①[Engineering Noise Control] 4th p429-431；②[GB/T 31013-2014 声学 管道、阀门和法兰的隔声] p19 附录A
# 版本：20191103
# 魏里来 weililai@foxmail.com
'''

import numpy as np
import matplotlib.pyplot as plt

# 常量及隔声套的几何参数、材料参数、声波频带中心频率、实测噪声
pi = 3.141592654  #圆周率
T = 20  #温度
c = 331 + 0.6*T  #空气声速
E = 69*10**9  #铝壳杨氏模量 69*10**9 #钢的杨氏模量 212*10**9
niu = 0.34  #铝的泊松比 0.34  #钢的泊松比0.31
rho = 2.7*10**3  #铝的密度2.7*10**3 #钢的密度7.85*10**3
D = 0.368  #裸管道直径
l = 0.06  #吸声层厚
h2 = 0.003  #隔声层厚  这里是隔声毡的阻尼层+防水涂料玻纤布
m2 = 4  #隔声层面密度  这里是隔声毡+防水涂料玻纤布
h3 = 1*10**(-3)  #铝壳或钢壳厚
f = np.array([125,250,500,1000,2000,4000,8000])  #声波频带中心频率
noise_before = np.array([71.1,67.3,73.9,84.1,91.5,93.2,88.4]) #实测噪声
# 设定内容到此为止

d = D+2*l+2*h2+2*h3  #隔声套外径
B = E*h3**3/(12*(1 - niu**2))  #弯曲刚度
m3 = rho*h3  #金属壳层面密度
m = m2+m3  #隔声毡+金属壳的总面密度
c_L = 12**0.5/h3*(B/m3)**0.5  #铝壳中纵波速度
f_r = c_L/pi/d  #铝壳环频率
f_c = c*c/2/pi*(m3/B)**0.5  #铝壳临界频率


# 下面计算隔声套在各频段中心频率的插入损失,公式来源：[[Engineering Noise Control] p429-413 8.6.2]
# IL = 10*np.log10(1-0.012*X_r*np.sin(2*C_r)+(0.012*X_r*np.sin(C_r))**2)  #300Hz以下插入损失IL公式，在使用时还增添了阻尼作用的附加插入损失
# IL = (40/(1+0.12/D))*np.log10((f*(m*l)**0.5)/132)  #300Hz以上IL公式，在使用时还增添了阻尼作用的附加插入损失
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
        IL[i] = 10*np.log10(1-0.012*X_r[i]*np.sin(2*C_r[i])+(0.012*X_r[i]*np.sin(C_r[i]))**2) +1*1000*h2
    else :  # 频率在300Hz以上
        IL[i] = (40/(1+0.12/D))*np.log10((f[i]*(m*l)**0.5)/132) +2*1000*h2
    i += 1

# 输出各设定的物理量及插入损失 IL
print("1. T , c , E , niu , rho , φ , l , h2 , h3 , Φ , m2 , m3 , m :")
print("  ",round(T,4),",",round(c,4),",",round(E,4),",",round(niu,4),",",round(rho,4),",",round(D,4),",",round(l,4),",",round(h2,4),",",round(h3,4),",",round(d,4),",",round(m2,4),",",round(m3,4),",",round(m,4))
print(" ")
#print(B,m,c_L,f_r,f_c,xi_r,X_r,)
#print(" ")
print("2. Insertion loss (IL) :")
np.set_printoptions(formatter={'float': '{: 0.1f}'.format})  #设定输出的数值保留一位小数
print("   f  = ",f,"Hz")
print("   IL = ",IL,"dB")

# 计算各隔声等级要求的最小插入损失,来源：[[GB/T 31013-2014 声学 管道、阀门和法兰的隔声] 附录A]
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
print(" ")
print("3. Minimum insertion loss required for each class :")
print("   A1 = ",A1,"dB")
print("   A2 = ",A2,"dB")
print("   A3 = ",A3,"dB")
print("   B1 = ",B1,"dB")
print("   B2 = ",B2,"dB")
print("   B3 = ",B3,"dB")
print("   C1 = ",C1,"dB")
print("   C2 = ",C2,"dB")
print("   C3 = ",C3,"dB")


# 作管套隔声量与频率的关系图
fstr = [str(f[i]) for i in range(len(f))]  # 倍频程数值转字符串，方便在坐标轴上均匀排布（倍频程在普通线性递增坐标轴上刻度不均匀）
label_str = "IL (lagging Φ=" + str(round(d,4)) + "m ,φ=" + str(round(D,4)) + "m)"
plt.title("IL of pipe lagging")
level = "level(A/B/C)"
plt.plot(fstr, IL, label=label_str,marker='o') # 作出该隔声套的插入损失曲线
# 判断该管套所属的管径范围，作出管径对应的三个隔声等级标准曲线，并将管套隔声性能与标准曲线对比得出管套的隔声等级
if D <0.3 :
    plt.plot(fstr, A1, label='A1')
    plt.plot(fstr, B1, label='B1')
    plt.plot(fstr, C1, label='C1')
    if np.all(IL-A1 >0) :
        level = "A1"
    if np.all(IL-B1 >0) :
        level = "B1"
    if np.all(IL-C1 >0) :
        level = "C1"
if D >=0.3 and D <0.65 :
    plt.plot(fstr, A2, label='A2')
    plt.plot(fstr, B2, label='B2')
    plt.plot(fstr, C2, label='C2')
    if np.all(IL-A2 >0) :
        level = "A2"
    if np.all(IL-B2 >0) :
        level = "B2"
    if np.all(IL-C2 >0) :
        level = "C2"
if D >=0.65 and D <1 :
    plt.plot(fstr, A3, label='A3')
    plt.plot(fstr, B3, label='B3')
    plt.plot(fstr, C3, label='C3')
    if np.all(IL-A3 >0) :
        level = "A3"
    if np.all(IL-B3 >0) :
        level = "B3"
    if np.all(IL-C3 >0) :
        level = "C3"
print(" ")
print("4. Level of this lagging :")
print("  ",level)

plt.legend() # 给曲线添加图例
plt.xlabel('Frequency / Hz')
plt.ylabel('Insertion loss (IL) / dB')
#plt.show() #绘出的图用弹出窗口来显示
plt.savefig('IL of pipe lagging.png')  # 保存图片文件到当前文件夹

# 估算噪声降低值并输出（注：实测原噪声 noise_before 已经在开头设定）
noise_A_weighting_corrections = np.array([-16.1,-8.6,-3.2,0,1.2,1.0,-1.1]) # A计权修正谱
noise_before_dBA = noise_before + noise_A_weighting_corrections # 获得A计权原噪声
noise_before_dBA_total = 10*np.log10(np.sum(10**(noise_before_dBA/10) ) ) # 获得A计权原噪声总值
noise_after = noise_before - IL # 获得隔声后的噪声
noise_after_dBA = noise_after + noise_A_weighting_corrections # 获得隔声后的A计权噪声
noise_after_dBA_total = 10*np.log10(np.sum(10**(noise_after_dBA/10) ) ) # 获得隔声后的A计权噪声总值
noise_reduction_dBA_total = noise_before_dBA_total - noise_after_dBA_total # 获得A计权总降噪量
print(" ")
print("5. noise reduction estimate:")
print("   noise_before :    ",noise_before,"dB")
print("   noise_before_dBA :",noise_before_dBA,"dBA")
print("   IL :              ",IL,"dB")
print("   noise_after :     ",noise_after,"dB")
print("   noise_after_dBA : ",noise_after_dBA,"dBA")
print("   noise_before_dBA_total :   ",round(noise_before_dBA_total,1),"dBA")
print("   noise_after_dBA_total :    ",round(noise_after_dBA_total,1),"dBA")
print("   noise_reduction_dBA_total :",round(noise_reduction_dBA_total,1),"dBA")


exit(0)
