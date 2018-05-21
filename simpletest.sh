DATANAME="wikisql"
GPU_ID=0

PWD_DIR=$(pwd)
WORK_DIR=$(dirname "$(readlink -f $0)")
cd $WORK_DIR
DATA_DIR=$WORK_DIR/data_model/$DATANAME
MODEL_PATH=$DATA_DIR/pretrain.pt

cd $DATANAME
CUDA_VISIBLE_DEVICES=$GPU_ID python predict.py -split test -output pred.txt -data_path "$DATA_DIR" -model_path "$MODEL_PATH"

cd $PWD_DIR
