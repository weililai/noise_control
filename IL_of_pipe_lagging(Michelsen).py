# 吸声材料+隔声阻尼/质量壳层结构的管道隔声套，插入损失IL的估算，所有变量单位使用国际单位制SI
# 版本：20190827
# 作者：魏里来 weililai@foxmail.com

import numpy as np

# 输入公式变量 diameter  surface_densty  absorptive_materiial_thickness，并转化为浮点数值
structure_parameter = input("Please input  'diameter  surface_densty  absorptive_materiial_thickness' : (Separate the value entered with a space):")
structure_parameter = structure_parameter.split(" ")
structure_parameter = [float(structure_parameter[i]) for i in range(len(structure_parameter))]

# 输入公式变量 frequency，并转化为numpy向量
frequency = input("Please input 'frequency' :  (Separate the value entered with a space):")
frequency = frequency.split(" ")
frequency = [float(frequency[i]) for i in range(len(frequency))]
frequency = np.array(frequency)

# 打印经处理的输入变量
print(structure_parameter)
print(frequency)

# 把变量赋值到公式中的物理量上
D = structure_parameter[0]#diameter
f = frequency
m = structure_parameter[1]#surface_densty
l = structure_parameter[2]#absorptive_materiial_thickness

# 计算并显示插入损失 IL ，公式来源：[Engineering Nooise Control],4th,p431,(8.144)
IL = (40/(1+0.12/D))*np.log10((f*(m*l)**0.5)/132)
print(IL)
