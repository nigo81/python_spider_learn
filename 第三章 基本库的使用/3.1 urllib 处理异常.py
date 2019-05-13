from urllib import request,error
try:
    response=request.urlopen('https://cuiqingcai.com/index.htm')
except error.HTTPError as e:
    print(e.reason,e.code,e.headers,sep='\n') #URLERROr的子类
except error.URLError as e:
    print(e.reason)
else:
    print('Request Successfully')

## 先捕获HTTPERROR，否则再捕获URLERROR，最后如果正常处理就执行到else。这是比较好的处理异常处理方法。