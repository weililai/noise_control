#该程序将1/3倍频程噪声级转倍频程噪声级，也可通过1/3倍频程隔声量估算倍频程隔声量
import numpy as np
f = np.array([100,125,160,200,250,315,400,500,630,800,1000,1250,1600,2000,2500,3150,4000,5000,6300,8000,10000])
a_one_third_octave = np.array([40.0,40.0,40.0,42.0,41.5,39.7,37.5,40.8,38.1,32.8,34.9,34.3,33.7,48.2,43.0,31.7,37.8,45.1,40,40,40])
a_octave_TL = np.zeros(7)
a_octave = np.zeros(7)
i=0
while i <21 :
    a_octave[int(i/3)] = 10*np.log10((10**(a_one_third_octave[i]/10)+10**(a_one_third_octave[i+1]/10)+10**(a_one_third_octave[i+2]/10) ) ) #1/3倍频程噪声转倍频程噪声
    a_octave_TL[int(i/3)] = 10*np.log10((10**(a_one_third_octave[i]/10)+10**(a_one_third_octave[i+1]/10)+10**(a_one_third_octave[i+2]/10) )/3 ) #1/3倍频程隔声量转倍频程隔声量
    i = i+3
print("octavea",a_octave,"dB")
print("octave_TL",a_octave_TL,"dB")
