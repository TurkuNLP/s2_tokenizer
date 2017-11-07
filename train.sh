NMT=$HOME/OpenNMT-py
TBANK=$HOME/UD_Finnish

mkdir -p models
python3 $NMT/train.py -save_model models/$(basename $TBANK) -gpuid 0 -data data_pp/$(basename $TBANK) -epochs 200

