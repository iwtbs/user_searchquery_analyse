#coding:gbk
import sys
import tqdm
from itertools import combinations

entity_searchquerynumber_searchquerytimes_dict = {}
total_searchquerynumber = 0
total_searchquerytimes = 0
total_entity_searchquerynumber = 0
total_entity_searchquerytimes = 0

file_path = sys.argv[1]
line_num = len([ "" for line in open(file_path, "r")])

ptr = 0
with tqdm.tqdm(total=line_num) as progress:
    for line in file(file_path):
        ptr += 1
        if ptr % 2000000 == 0:
            print entity_searchquerynumber_searchquerytimes_dict
            #break
        progress.update(1)
        items1 = line.strip().split('\t')
        if len(items1) < 2:
            continue
        times = int(items1[1])
        total_searchquerynumber += 1
        total_searchquerytimes += times
        if len(items1) < 3:
            continue
        entity_info = items1[2]
        entity_type_list = []
        label_list = ['novel:', 'video:', 'game:', 'qingse']
        for label in label_list:
            if entity_info.find(label) != -1:
                entity_type_list.append(label)
        if len(entity_type_list) > 0:
            total_entity_searchquerynumber += 1
            total_entity_searchquerytimes += times
            for i in range(len(entity_type_list)):
                for comb in combinations(entity_type_list, i+1):
                    comb_str = ':'.join(comb)
                    entity_searchquerynumber_searchquerytimes_dict[comb_str] = (entity_searchquerynumber_searchquerytimes_dict.get(comb_str, (0, 0))[0] + 1, entity_searchquerynumber_searchquerytimes_dict.get(comb_str, (0, 0))[1] + times)

fw = open(sys.argv[2], 'w')

fw.write(str(total_searchquerynumber) + '\t' + str(total_searchquerytimes) + '\t' + str(total_entity_searchquerynumber) + '\t' + str(total_entity_searchquerytimes) + '\t' + str(total_entity_searchquerynumber*1.0/total_searchquerynumber) + '\t' + str(total_entity_searchquerytimes*1.0/total_searchquerytimes) + '\n')

for entity, (searchquerynumber, searchquerytimes) in entity_searchquerynumber_searchquerytimes_dict.items():
    fw.write(entity + '\t' + str(searchquerynumber) + '\t' + str(searchquerytimes) + '\t' + str(searchquerynumber*1.0/total_searchquerynumber) + '\t' + str(searchquerytimes*1.0/total_searchquerytimes) + '\n')

fw.close()
