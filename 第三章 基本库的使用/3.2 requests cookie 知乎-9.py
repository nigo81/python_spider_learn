import requests
headers={
    'Cookie':'_zap=6c812c89-4708-4d87-a5da-4576c7291192; d_c0="AFDk6rLU5A6PTq0yVoi26iOBbNTYju2OWaU=|1548654747"; z_c0="2|1:0|10:1548725781|4:z_c0|92:Mi4xMHZPLUFBQUFBQUFBVU9UcXN0VGtEaVlBQUFCZ0FsVk5GZnc4WFFBRU5QQXpmbmZIaFg2d25SNDJkcHBDTktXVUF3|737bc118d998a0ec9f154a57e7bf531c867b8b1add4c10fe087e145956de23eb"; _xsrf=siGi6LdqJvRQFJZmwUDWusT7KlrxWVij; q_c1=40fe84aee8d8436a9d151ea36ad825c0|1557651897000|1548998942000; __utma=51854390.365212605.1557651901.1557651901.1557651901.1; __utmc=51854390; __utmz=51854390.1557651901.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.100--|2=registration_date=20150113=1^3=entry_date=20150113=1; tgw_l7_route=80f350dcd7c650b07bd7b485fcab5bf7; tst=r',
    'Host':'www.zhihu.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36',
}
r=requests.get('https://www.zhihu.com',headers=headers)
print(r.text)