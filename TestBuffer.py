#!/usr/bin/env python
# -*- coding: euc-jp -*-



import OpenRTM_aist
from OpenRTM_aist import *

class TestBuffer(OpenRTM_aist.BufferBase):
  def __init__(self, length=1):
    self._buffer = None
    self._mutex = threading.RLock()
    self.reset()


  
  def init(self, prop):
    pass



  

  def reset(self):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    self._buffer = None
    return OpenRTM_aist.BufferStatus.BUFFER_OK


 
  def wptr(self, n = 0):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    return self._buffer

    

  def advanceWptr(self, n = 1):
    
    return OpenRTM_aist.BufferStatus.BUFFER_OK



  def put(self, value):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    self._buffer = value
    return OpenRTM_aist.BufferStatus.BUFFER_OK
    
  def write(self, value, sec = -1, nsec = 0):
    if self.full():
      return OpenRTM_aist.BufferStatus.BUFFER_FULL
    self.put(value)

    return OpenRTM_aist.BufferStatus.BUFFER_OK
    

  def writable(self):
    return 0
    

  def full(self):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    if self._buffer is None:
      return False
    else:
      return True
    

  def rptr(self, n = 0):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    return self._buffer

    
  def advanceRptr(self, n = 1):
    return OpenRTM_aist.BufferStatus.BUFFER_OK


    
  def get(self, value=None):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    if value is None:
      return self._buffer
    value[0] = self._buffer
    return OpenRTM_aist.BufferStatus.BUFFER_OK
    
    
  def read(self, value, sec = -1, nsec = 0):
    if self.empty():
      return OpenRTM_aist.BufferStatus.BUFFER_EMPTY
    val = self.get()
    if len(value) > 0:
      value[0] = val
    else:
      value.append(val)
    return OpenRTM_aist.BufferStatus.BUFFER_OK

    
  def readable(self):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    if self._buffer is None:
      return 0
    else:
      return 1
    

  def empty(self):
    guard = OpenRTM_aist.ScopedLock(self._mutex)
    if self._buffer is None:
      return True
    else:
      return False

    

def TestBufferInit(manager):
  OpenRTM_aist.CdrBufferFactory.instance().addFactory("test_buffer",
                                                      TestBuffer,
                                                      OpenRTM_aist.Delete)
