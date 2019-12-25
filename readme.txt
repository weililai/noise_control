# IL_of_pipe_lagging(Hale+Michelsen),可以计算管道隔声套在各频段中心频率的插入损失，并输出 插入损失-频率 折线图，为了与标准隔声等级比较，同时输出了标准隔声等级最小插入损失，最后判断该隔声套隔声级别。物理量使用国际SI国际单位制
'''
# 该程序的使用方法：在本文件的“# 常量及隔声套的几何参数、材料参数、声波频带中心频率”一段里设置需要的变量;
  在终端(Terminal)里输入“python<"IL_of_pipe_lagging(Hale+Michelsen).py" >level_report.txt”,回车
# 输出的文件有：①图片 IL of pipe lagging.png；②文本 level_report.txt
# 主要参考：①[Engineering Noise Control] 4th p429-431；②[GB/T 31013-2014 声学 管道、阀门和法兰的隔声] p19 附录A
# 版本：20191103
# 作者：魏里来 weililai@foxmail.com
'''

# NR_of_Enclosures, 可以计算厂房内的隔声罩在各频段的降噪量；已知设备声功率级可以计算罩内外声压级。（物理量使用SI国际单位制）
'''
# 该程序的使用方法：在本文件的设置段落里设置需要的变量;
  在终端(Terminal)里输入“python<"NR_of_Enclosures.py" >NR_report.txt”,回车
# 输出的文件：文本 NR_report.txt
# 主要参考：[Engineering Noise Control] 5th p407-410
# 版本：20191118
# 作者：魏里来 weililai@foxmail.com
'''
