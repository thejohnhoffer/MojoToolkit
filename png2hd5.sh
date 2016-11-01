
mkdir /data/Red_Cylinder/$1-$2-$3
python png2hd5.py /data/x/$1/$2/$3/image /data/Red_Cylinder/$1-$2-$3/image.h5 -d 2
python png2hd5.py /data/x/$1/$2/$3/synapse-gt-segmentation /data/Red_Cylinder/$1-$2-$3/truth.h5 -d 2 -f bgr
python png2hd5.py /data/x/$1/$2/$3/synapse-segmentation /data/Red_Cylinder/$1-$2-$3/guess.h5 -d 2 -f bgr
python png2hd5.py /data/x/$1/$2/$3/mask /data/Red_Cylinder/$1-$2-$3/mask.h5 -d 2 -t uint8
