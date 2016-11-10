mkdir /data/Red_Cylinder/$1-$2-$3/mask
python hd5mask.py truth.h5 -d /data/Red_Cylinder/$1-$2-$3
python hd5mask.py guess.h5 -d /data/Red_Cylinder/$1-$2-$3
