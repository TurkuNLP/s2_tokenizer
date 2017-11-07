NMT=$HOME/OpenNMT-py
TBANK=$HOME/UD_Finnish
CUTOFF=300

mkdir -p data data_pp

for s in train dev test
do
    cat $TBANK/*-$s.conllu | python3 create_data.py --max $CUTOFF data/$(basename $TBANK)-$s-src.txt data/$(basename $TBANK)-$s-trg.txt
done

python3 $NMT/preprocess.py -train_src data/$(basename $TBANK)-train-src.txt -train_tgt data/$(basename $TBANK)-train-trg.txt -valid_src data/$(basename $TBANK)-dev-src.txt -valid_tgt data/$(basename $TBANK)-dev-trg.txt -save_data data_pp/$(basename $TBANK) -src_seq_length 300 -tgt_seq_length 300 -dynamic_dict



