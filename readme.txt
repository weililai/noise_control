# 程序功能：计算管道隔声套在各频段中心频率的插入损失，并输出 插入损失-频率 折线图，为了与标准隔声等级比较，同时输出了标准隔声等级最小插入损失，最后判断该隔声套隔声级别。
# 使用步骤：①在文件“IL_of_pipe_lagging(Hale+Michelsen).py”的“# 常量及隔声套的几何参数、材料参数、声波频带中心频率”一段里设置需要的变量；
            ②在终端(Terminal)里输入“python<"IL_of_pipe_lagging(Hale+Michelsen).py" >level_report.txt”,回车；
            ③在终端(Terminal)里输入“python<"reporter.py"”,回车
# 输出的文件有：①图片 “IL of pipe lagging.png”；②文本 “level_report.txt”；③docx文档 “level_report.docx”
# 主要参考：[Engineering Noise Control] 4th p429-431,[GB/T 31013-2014 声学 管道、阀门和法兰的隔声] p19 附录A
# 版本：20190830
# 魏里来 weililai@foxmail.com