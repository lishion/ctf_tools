import gmpy2
from rsa import transform
from rsa import common
from rsa import decrypt
# 对rsa的共模攻击
# 构造函数:
# c1,c2 : 密文1,2
# e1,e2 : 指数1,2
# N     : 共同模数
# 方法:
# attack() : 返回十进制明文
# stringify() : 返回明明文字符串
# 使用依赖:
# 需要安装rsa,gmpy2
# rsa : pip install rsa
# gmpy2 : https://www.cnblogs.com/pcat/p/5746821.html
class common_mode_attack:

  def __init__(self,c1,c2,e1,e2,N):
    self._c1 = c1
    self._c2 = c2
    self._e1 = e1
    self._e2 = e2
    self._N = N
    self._modinv = lambda x,y : gmpy2.invert(x,y)
    self._m = None

  def __egcd(self,a, b):
      if a == 0:
        return (b, 0, 1)
      else:
        g, y, x = self.__egcd(b % a, a)
        return (g, x - (b // a) * y, y)

  def attack(self):
      s = self.__egcd(self._e1, self._e2)
      s1 = s[1]
      s2 = s[2]
      if s1<0:
          s1 = - s1
          c1 = self._modinv(self._c1, self._N)
          c2 = self._c2
      elif s2<0:
          s2 = - s2
          c1 = self._c1
          c2 = self._modinv(self._c2, self._N)
      self._m =  pow(c1,s1,self._N)*pow(c2,s2,self._N) % self._N
      return self._m
  
  def stringify(self):
      return transform.int2bytes(self._m)