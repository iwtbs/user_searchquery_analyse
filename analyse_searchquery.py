#coding:gbk
import sys
import tqdm
import esm

debug = False

max_len_threshold = 60

def prepare_str(string, new_part):
    string = string.replace('：', new_part)
    string = string.replace('，', new_part)
    string = string.replace('！', new_part)
    string = string.replace('!', new_part)
    string = string.replace('*', new_part)
    string = string.replace('-', new_part)
    string = string.replace(',', new_part)
    return string.strip()


def prepare_str_for_more(string_list, strings_list):
    string_set = set()
    for string in string_list:
        string_set |= set([string])
    for strings in strings_list:
        string_set |= set(map(lambda x: prepare_str(x, ''), strings.split(';')))
    return string_set


def gen_novel_index(file_path):
    novel_index = esm.Index()
    line_num = len([ "" for line in open(file_path, "r")])
    with tqdm.tqdm(total=line_num) as progress:
        valid_num = 0
        for line in file(file_path):
            progress.update(1)
            items1 = line.strip().split('\t')
            if len(items1) != 2:
                continue
            novel1 = items1[0]
            novel2 = prepare_str(novel1, '')
            times = int(items1[1])
            len_threshold = 4
            if times < 1000 and times >= 100:
                len_threshold = 6
            elif times < 100:
                len_threshold = 8
            if len(novel1) >= len_threshold and len(novel1) <= max_len_threshold:
                novel_index.enter(novel1)
                valid_num += 1
            if novel1 != novel2 and len(novel2) >= len_threshold and len(novel2) <= max_len_threshold:
                novel_index.enter(novel2)
                valid_num += 1
            if debug == True:
                if valid_num >= 100000:
                    break
    print valid_num
    novel_index.fix()
    return novel_index


def gen_video_index(file_path):
    video_index = esm.Index()
    line_num = len([ "" for line in open(file_path, "r")])
    with tqdm.tqdm(total=line_num) as progress:
        valid_num = 0
        for line in file(file_path):
            progress.update(1)
            items1 = line.split('\t')
            if len(items1) != 7:
                continue
            hit_count = int(items1[2])
            name = items1[3]
            alias_name = items1[4]
            serial = items1[5]
            alais_serial = items1[6]
            name_set = prepare_str_for_more([name, serial], [alias_name, alais_serial])
            len_threshold = 4
            if hit_count < 100:
                len_threshold = 6
            for name in name_set:
                if len(name) >= len_threshold and len(name) <= max_len_threshold:
                    video_index.enter(name)
                    valid_num += 1
            if debug == True:
                if valid_num >= 100000:
                    break
    print valid_num
    video_index.fix()
    return video_index


def gen_game_index(file_path):
    game_index = esm.Index()
    line_num = len([ "" for line in open(file_path, "r")])
    with tqdm.tqdm(total=line_num) as progress:
        valid_num = 0
        for line in file(file_path):
            progress.update(1)
            items1 = line.split('#@#')
            if len(items1) != 2:
                continue
            game_list = items1[1].split('@')
            for game in game_list:
                game2 = prepare_str(game, '')
                len_threshold = 6
                if len(game) >= len_threshold:
                    game_index.enter(game)
                    valid_num += 1
                if game2 != game and len(game2) >= len_threshold and len(game2) <= max_len_threshold:
                    game_index.enter(game2)
                    valid_num += 1
            if debug == True:
                if valid_num >= 100000:
                    break
    print valid_num
    game_index.fix()
    return game_index


def gen_qingse_index(file_path):
    qingse_index = esm.Index()
    line_num = len([ "" for line in open(file_path, "r")])
    with tqdm.tqdm(total=line_num) as progress:
        valid_num = 0
        for line in file(file_path):
            progress.update(1)
            qingse_index.enter(line.strip())
            valid_num += 1
    print valid_num
    qingse_index.fix()
    return qingse_index


novel_index = gen_novel_index(sys.argv[1])
video_index = gen_video_index(sys.argv[2])
game_index = gen_game_index(sys.argv[3])
qingse_index = gen_qingse_index(sys.argv[4])

def get_match_entity(index, searchquery):
    index_result = index.query(searchquery)
    match_entity_dict = {}
    for (st_end, match_entity) in index_result:
        if st_end[0] % 2 == 0:
            match_entity_dict[match_entity] = True
    ret = ''
    if len(match_entity_dict) > 0:
        ret = ','.join(match_entity_dict.keys())
    return ret


fw = open(sys.argv[6], 'w')

file_path = sys.argv[5]
line_num = len([ "" for line in open(file_path, "r")])
with tqdm.tqdm(total=line_num) as progress:
    for line in file(file_path):
        progress.update(1)
        items1 = line.split('\t')
        if len(items1) != 2:
            continue
        searchquery = items1[0]
        times = int(items1[1])
        
        novel_result = get_match_entity(novel_index, searchquery)
        video_result = get_match_entity(video_index, searchquery)
        game_result = get_match_entity(game_index, searchquery)
        qingse_result = get_match_entity(qingse_index, searchquery)

        output = ''
        if len(novel_result) > 0:
            output += 'novel:' + novel_result + '; '
        if len(video_result) > 0:
            output += 'video:' + video_result + '; '
        if len(game_result) > 0:
            output += 'game:' + game_result + '; '
        if len(qingse_result) > 0:
            output += 'qingse'

        fw.write(searchquery + '\t' + str(times) + '\t' + output + '\n')

fw.close()


