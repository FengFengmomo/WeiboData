import re
def readCookie(file):
    f=open(file,encoding='utf-8')
    cookie={}
    for line in f.readlines():
        line=re.sub("\s|,","",line)
        items=line.split("=")
        cookie[items[0]]=items[1]
    return cookie
def getCookie(file):
    f=open(file,encoding='utf-8')
    cookie={}
    for line in f.readlines():
        kv=line.split(";")
        for var in kv:
            k,v=var.split("=")
            cookie[k]=v
    return cookie
