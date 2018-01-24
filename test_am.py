#!/usr/bin/python3
import scipy
import scipy.io
import scipy.io.wavfile as wavfile
from toshokan import File, Tieng, Frame, Kame, KameJoko
# a = [1,3,4,5,6,7,8,9]
# print(a)
# b = Kame(a)
# print(a, b.dulieu)
# a[5] = 1000
# print(a, b.dulieu)


# m = 5
# c = KameJoko(m)
# print(m, c.dulieu)
# m = 1000
# print(m, c.dulieu)
import numpy as np
import sounddevice as sd
import os
import time
n = File('khoosoothunhus.wav')
print(n.sample_rate(), n.time(), n.data())
n.play()
f =Frame(n.data(), 0, 640, 16000)
print(f.chu_ky())
# print(f.nang_luong())
# print(f.ham_ttq())
# print(n.data())
# print(f.nang_luong(), f.chu_ky(), f.tan_so_co_ban())
# # time.sleep(3)
# p = File('/home/hero/Downloads/khoosoothunhus.wav')
# p.play()
# fs, data = wavfile.read("khoosoothunhus.wav")
# os.system("aplay khoosoothunhus.wav")

# print(fs, len(data), type(data))
# wavfile.write('chim.wav',fs,data)
# os.system("aplay chim.wav")
