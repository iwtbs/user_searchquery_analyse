#coding:gbk
import sys
import traceback
import MySQLdb

conn = MySQLdb.connect(host="***", port=3306, user="***", passwd="***", db="***", charset='gbk')
cur = conn.cursor()

fw = open(sys.argv[1], 'w')
cur.execute('SELECT dockey,doctype,hit_count,`name`,alais_name,serial,alais_serial FROM entity_main WHERE version_id=(SELECT MAX(version_id) FROM entity_main) ORDER BY hit_count DESC;')
rows = cur.fetchall()
ptr = 0
for i in rows:
    ptr += 1
    if ptr % 10000 == 0:
        print str(ptr/10000) + 'w'
    dockey = i[0].encode('gbk', 'ignore')
    doctype = i[1]
    hit_count = i[2]
    name = i[3].strip().encode('gbk', 'ignore').replace('\t', ' ')
    alias_name = i[4].strip().encode('gbk', 'ignore').replace('\t', ' ')
    serial = i[5].strip().encode('gbk', 'ignore').replace('\t', ' ')
    alais_serial = i[6].strip().encode('gbk', 'ignore').replace('\t', ' ')
    fw.write(dockey + '\t' + str(doctype) + '\t' + str(hit_count) + '\t' + name + '\t' + alias_name + '\t' + serial + '\t' + alais_serial + '\n')
fw.close()

cur.close()
conn.close()
