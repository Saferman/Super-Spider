#encoding=utf-8
import hashlib
import re

def MD5(s):
    m = hashlib.md5() 
    m.update(s)
    return m.hexdigest()


def caculatemode(u):
    # Hash tag不同的链接是一样的页面
    if u.rfind("#")!=-1:
        u = u[0:u.rfind("#")]

    # 去除末尾的?,&
    u = u.rstrip('&')
    u = u.rstrip('?')

    # 数字替换，对于同一类的页面尽可能少的重复提取
    number_pattern = re.compile("\d+")
    u = re.sub(number_pattern, 'd+', u)
    return u


def Duplicate(conn, ID, url):
    mode_md5 = MD5(caculatemode(url))
    sql = "select ID from URLS where MD5=" + "'" + mode_md5 + "';"
    if len(conn.execute(sql).fetchall()) > 0 :
        #print "True"
        return True
    else:
        #print "False"
        ID[0] += 1
        sql = "INSERT INTO URLS (ID,URL,MD5) VALUES (" + str(ID[0]) + ", '" + url + "', '" + mode_md5 + "');"
        conn.execute(sql)
        conn.commit()
        return False

if __name__ == '__main__':
    pass
