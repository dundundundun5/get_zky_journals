# for i in {2019..2023}
# do

# python get_n_save_jsons.py --year $i


# done

# for i in {2019..2023}
# do

# python get_zky_journals.py --year $i


# done

# for i in {2019..2023}
# do

# python merge.py --year $i

# done
  
# for i in {2018..2021}
# do

# python old_get_n_save_csvs.py --year $i --subject 地学 

# python old_get_n_save_csvs.py --year $i --subject 地学天文

# python old_get_n_save_csvs.py --year $i --subject 工程技术 

# python old_get_n_save_csvs.py --year $i --subject 管理科学 

# python old_get_n_save_csvs.py --year $i --subject 化学 

# python old_get_n_save_csvs.py --year $i --subject 环境科学与生态学 

# python old_get_n_save_csvs.py --year $i --subject 农林科学 

# python old_get_n_save_csvs.py --year $i --subject 社会科学

# python old_get_n_save_csvs.py --year $i --subject 生物

# python old_get_n_save_csvs.py --year $i --subject 数学 

# python old_get_n_save_csvs.py --year $i --subject 物理 

# python old_get_n_save_csvs.py --year $i --subject 医学 

# python old_get_n_save_csvs.py --year $i --subject 综合性期刊

# done

for i in {2018..2021}
do

python old_get_zky_journals.py --year $i
done