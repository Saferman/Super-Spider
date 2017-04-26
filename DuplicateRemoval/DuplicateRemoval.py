#encoding=utf-8
import hashlib

def MD5(s):
    m = hashlib.md5() 
    m.update(s)
    return m.hexdigest()

def Duplicate(conn, ID, u):
    #print "D:" + u
    md5_u = MD5(u)
    sql = "select ID from URLS where MD5=" + "'" + md5_u + "';"
    if len(conn.execute(sql).fetchall()) > 0 :
        #print "True"
        return True
    else:
        #print "False"
        ID[0] += 1
        sql = "INSERT INTO URLS (ID,URL,MD5) VALUES (" + str(ID[0]) + ", '" + u + "', '" + md5_u + "');"
        conn.execute(sql)
        conn.commit()
        return False

if __name__ == '__main__':
    pass
