#coding:gbk
import sys
import tqdm

searchquery_entitys_dict = {}

file_path = sys.argv[1]
line_num = len([ "" for line in open(file_path, "r")])

ptr = 0
with tqdm.tqdm(total=line_num) as progress:
    for line in file(file_path):
	progress.update(1)
	ptr += 1
	#if ptr % 100000 == 0:
	#    break
        items1 = line.strip().split('\t')
        if len(items1) < 3:
            continue
	searchquery = items1[0]
        entity_info = items1[2]
        entity_type_list = []
        label_list = ['novel:', 'video:', 'game:', 'qingse']
        for label in label_list:
            if entity_info.find(label) != -1: 
                entity_type_list.append(label)
        if len(entity_type_list) > 0:
	    searchquery_entitys_dict[searchquery] = ':'.join(entity_type_list)

print len(searchquery_entitys_dict)


def convert_searchquerys_to_list(searchquerys_info):
    searchquery_times_dict = {}
    items1 = searchquerys_info.split('#@@#')
    for item1 in items1:
	items2 = item1.split('#@#')
	if len(items2) != 3:
	    continue
	searchquery = items2[0]
	times = int(items2[2])
	searchquery_times_dict[searchquery] = searchquery_times_dict.get(searchquery, 0) + times
    searchquery_times_list = sorted(searchquery_times_dict.items(), cmp = lambda x, y: cmp(x[1], y[1]), reverse=True)
    return searchquery_times_list



file_path = sys.argv[2]
line_num = len([ "" for line in open(file_path, "r")])

fw = open(sys.argv[3], 'w')
ptr = 0
with tqdm.tqdm(total=line_num) as progress:
    for line in file(file_path):
        progress.update(1)
	ptr += 1
	#if ptr % 100000 == 0:
	#    break
        items1 = line.strip().split('\t')
        if len(items1) != 2:
            continue
        mid = items1[0]
	searchquery_times_list = convert_searchquerys_to_list(items1[1])
	new_searchquerys_info = ''
	entity_set = set()
	for searchquery, times in searchquery_times_list:
	    new_searchquerys_info += searchquery + '#@#' + str(times) + '#@@#'
            entity_set |= set(searchquery_entitys_dict.get(searchquery, '').split(':'))
        entity_info = '' if len(entity_set) == 0 else ':'.join(filter(lambda x: True if len(x) != 0 else False, entity_set))
        fw.write(mid + '\t' + new_searchquerys_info + '\t' + entity_info + '\n')

fw.close()
