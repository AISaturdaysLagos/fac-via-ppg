input_file=$1
output_file=$2
train_test_ratio=$3
output_folder=$4

mkdir -p $output_folder

train=$output_folder/$output_file.train
test=$output_folder/$output_file.test
valid=${5-false}

echo "$input_file; $output_file; $output_folder $train; $test; $train_test_ratio; $valid"

awk -v train=$train -v test=$test -v ratio=$train_test_ratio '{if(rand()<ratio) {print > train} else {print > test}}' $input_file

if [ $valid = true ]; then
training=$output_folder/${output_file}_train.txt
validation=$output_folder/${output_file}_valid.txt

awk -v train=$training -v test=$validation -v ratio=0.8 '{if(rand()<ratio) {print > train} else {print > test}}' $train

fi
