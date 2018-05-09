进行rsa共模攻击

## 用法

```python
attacker = common_mode_attack(c1,c2,e1,e2,N)
message_decimal = attacker.attack()
message = attacker.stringify()
print(message) 
```

## 依赖

依赖于`rsa`以及`gmpy2`,`gmpy2`安装可以参考:

https://www.cnblogs.com/pcat/p/5746821.html

## 版本

只支持python2