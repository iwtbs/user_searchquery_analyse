#coding:gbk
import sys
import traceback
import MySQLdb

conn = MySQLdb.connect(host="***", port=3306, user="***", passwd="***", db="***", charset='gbk')
cur = conn.cursor()

fw = open(sys.argv[1], 'w')
cur.execute('SELECT title, hot FROM `novel` ORDER BY hot DESC;')
rows = cur.fetchall()
ptr = 0
for i in rows:
    ptr += 1
    if ptr % 10000 == 0:
        print str(ptr/10000) + 'w'
    title = i[0].strip().encode('gbk', 'ignore').replace('\t', ' ')
    hot = i[1]
    fw.write(title + '\t' + str(hot) + '\n')
fw.close()

cur.close()
conn.close()
