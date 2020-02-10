import sys
import traceback
import MySQLdb

conn = MySQLdb.connect(host="***", port=3306, user="***", passwd="***", db="***", charset='gbk')
cur = conn.cursor()

fw = open(sys.argv[1], 'w')
cur.execute('SELECT id,`name`,alias,hit_count FROM `star` WHERE total_number>=3 AND hit_count>=10 ORDER BY hit_count DESC;')
rows = cur.fetchall()
ptr = 0
for i in rows:
    ptr += 1
    if ptr % 10000 == 0:
        print str(ptr/10000) + 'w'
    star_id = i[0]
    name = i[1].strip().encode('gbk', 'ignore').replace('\t', ' ')
    alias_name = i[2].strip().encode('gbk', 'ignore').replace('\t', ' ')
    hit_count = i[3]
    fw.write(str(star_id) + '\t' + name + '\t' + alias_name + '\t' + str(hit_count) + '\n')
fw.close()

cur.close()
conn.close()


