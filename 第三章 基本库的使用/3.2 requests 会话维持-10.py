import requests
s=requests.session()  #维持在一个会话中，而不是重新找开了一具浏览器
r=s.get('http://httpbin.org/cookies/set/number/123456789')
r=s.get('http://httpbin.org/cookies')
print(r.text)