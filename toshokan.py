import os
import math
import numpy as np
from numpy import arange
import scipy.io.wavfile as wavfile

class File:  
  def __init__(self, file):    
    self.__file_name = file    
    self.__fs, self.__data = wavfile.read(self.__file_name)
    # self.__data = self.__data / 2**15
  def sample_rate(self):
    return self.__fs

  def length(self):
    return len(self.__data) 

  def data(self):
    return self.__data

  def time(self):    
    return len(self.__data)/self.__fs

  def frames(self, frame_length):
    try:      
      return self.__frames
    except AttributeError:            
      self.__frames = []
      for i in range(0, len(self.__data), frame_length >> 1): 
        self.__frames.append(Frame(self.__data, i, frame_length))
      return self.__frames

  def file_name(self):
    return self.__file_name
    
  def play(self):    
    os.system("aplay {0}".format(self.__file_name))

  def show(self, axes):    
    axes.plot(arange(len(self.__data)) / self.__fs, self.__data)      
    axes.set_xlabel('Time(s)')
    axes.set_ylabel('Amplitude') 

class Tieng:  
  def __init__(self, data):
    self.dulieu = data
class Frame:
  def __init__(self, data, toa_do, frame_length):
    if (toa_do + frame_length >> 1) >= len(data):
      self.__data = data[toa_do: len(data)]  
    else:
      self.__data = data[toa_do: toa_do + frame_length]    
    self.__toa_do = toa_do

  def data(self):
    return self.__data

  def toa_do(self):
    return self.__toa_do

  def nang_luong(self):
    try:      
      return self.__nang_luong
    except AttributeError:            
      self.__nang_luong = math.sqrt(sum(np.power(self.__data.astype('int32'), 2)))
      return self.__nang_luong

  def ham_ttq(self): # ham tu tuong quan
    try:
      return self.__ham_ttq      
    except AttributeError:
      N = len(self.__data)
      K = (int)(4*N/5)
      self.__ham_ttq = []
      x = self.__data / (1 << 15)      
      for k in range(K):
        sum = 0
        for n in range(N - k):
          sum += x[n] * x[n + k]
        self.__ham_ttq.append(sum)      
      return self.__ham_ttq

  def tan_so_co_ban(self, sample_rate):
    try:
      return self.__tan_so_co_ban
    except AttributeError:
      self.__tan_so_co_ban = sample_rate / self.chu_ky()
      return self.__tan_so_co_ban

  def chu_ky(self):
    try:
      return self.__chu_ky
    except AttributeError:
      a = self.ham_ttq()  
      cuc_tieu_dau_tien = a.index(min(a))
      self.__chu_ky = a.index(max(a[cuc_tieu_dau_tien: len(a)])) 
      return self.__chu_ky
class Kame:
  dulieu = None
  def __init__(self, data):
    self.dulieu = data  
    
class KameJoko:
  dulieu = None
  def __init__(self, data):
    self.dulieu = data