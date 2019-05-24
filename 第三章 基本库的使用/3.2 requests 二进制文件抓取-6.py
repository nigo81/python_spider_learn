import requests
r= requests.get('https://github.com/favicon.ico')
with open('favicon.ico','wb') as f:
    f.write(r.content)     #运行结束后，会在文件夹中出现favicon.ico的图标