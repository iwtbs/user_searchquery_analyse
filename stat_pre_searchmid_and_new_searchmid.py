pre_searchmid_list = []
for line in file('../data/search_mid'):
    pre_searchmid_list.append(line.strip())

new_searchmid_list = []
for line in file('./data/mid_searchquerys_20190331_31'):
    items1 = line.strip().split('\t')
    if len(items1) == 2:
        new_searchmid_list.append(items1[0])

pre_searchmid_set = set(pre_searchmid_list)
new_searchmid_set = set(new_searchmid_list)
set1 = pre_searchmid_set | new_searchmid_set
set2 = pre_searchmid_set & new_searchmid_set

print len(pre_searchmid_set), len(new_searchmid_set)
print len(set1)
print len(set2)
