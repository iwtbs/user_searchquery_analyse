#coding:gbk
import sys
import tqdm

searchquery_times_dict = {}

file_path = sys.argv[1]
line_num = len([ "" for line in open(file_path, "r")])

with tqdm.tqdm(total=line_num) as progress:
    for line in file(file_path):
        progress.update(1)
        items1 = line.strip().split('\t')
        if len(items1) != 2:
            continue
        mid = items1[0]
        items2 = items1[1].split('#@@#')
        for item2 in items2:
            items3 = item2.split('#@#')
            if len(items3) != 3:
                continue
            searchquery = items3[0]
            times = int(items3[2])
            searchquery_times_dict[searchquery] = searchquery_times_dict.get(searchquery, 0) + times
        #if len(searchquery_times_dict) >= 100000:
        #    break
print len(searchquery_times_dict)

searchquery_times_list = sorted(searchquery_times_dict.items(), cmp = lambda x, y: cmp(x[1], y[1]), reverse=True)

fw = open(sys.argv[2], 'w')
for searchquery, times in searchquery_times_list:
    fw.write(searchquery + '\t' + str(times) + '\n')
fw.close()
