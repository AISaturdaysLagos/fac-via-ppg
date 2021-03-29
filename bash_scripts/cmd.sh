PROJECT_ROOT_DIR=~/fac-via-ppg/
export PYTHONPATH=/home/tejumade/fac-via-ppg//src:/home/tejumade/fac-via-ppg//src:

ls en_ng_male/*.wav | awk '{print "/home/ubuntu/fac-via-ppg/datasets/"$0}' > en_ng_male.csv
ls en_ng_female/*.wav | awk '{print "/home/ubuntu/fac-via-ppg/datasets/"$0}' > en_ng_female.csv
. split_train_test.sh en_ng_male.csv male 0.95 filepaths true
. split_train_test.sh en_ng_female.csv female 0.95 filepaths true
. split2.sh  filepaths male_train.txt female_train.txt female_valid.txt male_valid.txt
export PYTHONPATH=$PROJECT_ROOT_DIR/src:$PYTHONPATH

cat male_train_500.txt | xargs -I{} soxi -D {} | awk '{SUM +=} END { printf %d:%d:%dn,SUM/3600,SUM%3600/60,SUM%60}'
