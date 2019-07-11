import requests
import re
d={
    'phone_number':'18080072071',
    'category':'signin_or_signup'
}
r=requests.post('https://caibaoshuo.com/verification_codes',data=d)
print(r.text)
d={
    'utf8':'%E2%9C%93',
    'users_phone_signin_or_signup%5Bphone_number%5D':'18080072071',
    'users_phone_signin_or_signup%5Botp%5D':'729056',
    'commit':'%E7%99%BB%E5%BD%95'
}
r=requests.post('https://caibaoshuo.com/ajax_signin_or_signup',data=d)
#pattern=re.compile('explore-feed.*?question_link.*?>(.*?)</a>',re.S)
#titles=re.findall(pattern,r.text)
print(r.text)