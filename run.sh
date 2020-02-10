#python get_novel_info_from_feed_monitor.py ./data/novel_info.txt
#python get_video_info_from_video_film.py ./data/video_info.txt
#python get_star_info_from_video_film.py ./data/star_info.txt

#python stat_searchquery_times.py ./data/mid_searchquerys_20190331_31 ./data/searchquery_times
#cat searchquery_times | tail -n +10000000 | head -n 100


##############
#python analyse_searchquery.py ./data/novel_info.txt ./data/video_info.txt ./data/game_info.txt ./data/qingse_keyword.txt ./data/searchquery_times ./data/searchquery_times_analyse

#split -l 3000000 -a 2 -d ./data/searchquery_times ./data/searchquery_times_dir/searchquery_times.

#split_file_num=`ls -l ./data/searchquery_times_dir |grep "^-"|wc -l`
#echo ${split_file_num}

#for((i=0;i<${split_file_num};i++))
#do
#    {    
#        suffix=`printf "%02d\n" ${i}`
#        echo ${suffix}
#        python analyse_searchquery.py ./data/novel_info.txt ./data/video_info.txt ./data/game_info.txt ./data/qingse_keyword.txt ./data/searchquery_times_dir/searchquery_times.${suffix} ./data/searchquery_times_analyse_dir/searchquery_times_analyse.${suffix}
#    }&
#done
#wait
############

#split -l 1000000 -a 2 -d ./data/searchquery_times ./data/searchquery_times_dir/searchquery_times.

#sh sub_run.sh

#cat ./data/searchquery_times_analyse_dir/* > ./data/searchquery_times_analyse

#python stat_entity_searchquerynumber_searchquerytimes.py ./data/searchquery_times_analyse ./data/entity_searchquerynumber_searchquerytimes

#python cal_mid_entity_info.py ./data/searchquery_times_analyse ./data/mid_searchquerys_20190331_31 ./data/mid_searchquerys_entitys
