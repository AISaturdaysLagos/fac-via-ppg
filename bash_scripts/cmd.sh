ls en_ng_male/*.wav | awk '{print /home/ubuntu/fac-via-ppg/datasets/}' > en_ng_male.csv
ls en_ng_female/*.wav | awk '{print /home/ubuntu/fac-via-ppg/datasets/}' > en_ng_female.csv
. split_train_test.sh en_ng_male.csv male 0.95 filepaths true
. split_train_test.sh en_ng_female.csv female 0.95 filepaths true
. split2.sh  filepaths male_train.txt female_train.txt female_valid.txt male_valid.txt
