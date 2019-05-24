import requests
r=requests.get('http://www.baidu.com')
print(r.cookies)
for key,value in r.cookies.items():
    print(key + "=" + value)