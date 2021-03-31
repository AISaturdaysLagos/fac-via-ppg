SRC_DIR=/home/ubuntu/fac-via-ppg
PPG2MEL_MODEL=$SRC_DIR/interspeech19-stage/ppg2speech-si-am-si-tacotron-bdl2ykwk-final/tacotron_checkpoint_11000
WAVEGLOW_MODEL=$SRC_DIR/interspeech19-stage/ppg2speech-si-am-si-tacotron-bdl2ykwk-final/waveglow_270000
UTTERANCE_FOLDER=$SRC_DIR/datasets/american_insurance_clip
output_dir=ame2zykwk

# conda activate ppg-speech

for i in {01..52};
do
    utterance_path=$UTTERANCE_FOLDER/american_$i.wav
    output_name=ame_ykwk_$i

    python src/script/generate_synthesis.py \
    --ppg2mel_model $PPG2MEL_MODEL \
    --waveglow_model  $WAVEGLOW_MODEL \
    --teacher_utterance_path $utterance_path \
    --output_dir $output_dir \
    --output_name $output_name

done