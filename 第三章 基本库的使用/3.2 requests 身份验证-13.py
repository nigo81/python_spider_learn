import requests
# from requests.auth import HTTPBasicAuth

# r=requests.get('http://localhost:5000',auth=HTTPBasicAuth)
#替代上两行的代码，简写为
r=requests.get('http://localhost:5000',auth=('username','passward'))