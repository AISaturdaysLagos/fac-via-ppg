output_folder=$1

male_train=$output_folder/$2
female_train=$output_folder/$3

female_valid=$output_folder/$4
male_valid=$output_folder/$5

echo "train: $male_train and $female_train; valid: $female_valid and $male_valid"

cat $male_train  > $output_folder/training_set.txt 
cat $female_train >> $output_folder/training_set.txt
cat $output_folder/training_set.txt  | shuf -o $output_folder/training_set.txt 


cat $female_valid > $output_folder/validation_set.txt
cat $male_valid >> $output_folder/validation_set.txt
cat $output_folder/validation_set.txt  | shuf -o $output_folder/validation_set.txt 
