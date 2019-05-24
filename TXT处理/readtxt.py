import os
import re
import xlwt
from tkinter import *
from tkinter.filedialog import askdirectory
from xlwt import Workbook
def select_path():
    path_=askdirectory()
    path.set(path_)
root=Tk()
root.withdraw()
#path='f:/Excel资料/黑科技开发/TXT读取/txt'
path=askdirectory()
#root.mainloop()
print(path)
file_names=os.listdir(str(path))
name_lists=[]
output=[]
for file in file_names:
    file_path=path + '/' + file
    f=open(file_path,'r',encoding='utf-8',errors='ignore')
    data=f.read()
    data=data.strip()
    mhs=re.search(r'Summary((.|\s)*)',data)
    if mhs:
        data=mhs.group(1)
        rows=data.split('\n')
        for row in rows:
            if row.strip() and row.strip()!='|':
                mhs=re.search(r'(([a-zA-Z]+\s)+)\s+.*?(\d+\.\d+)',row)
                if mhs:
                    output.append([file,mhs.group(1),mhs.group(3)])
    else:
        output.append([file,'N/A','N/A'])
book=Workbook(encoding='utf-8')
sht1=book.add_sheet('sheet1')
for i in range(len(output)):
    for j in range(len(output[1])):
        sht1.write(i,j,output[i][j])
book.save('./output_data.xls')
print("over")

