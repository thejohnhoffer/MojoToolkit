## The Mojo Conversion Toolkit

If you want to use RhoANA's proofreading tool Dojo, you'll need data arranged in a standardized way. The Mojo Conversion Toolkit comes with three python scripts that allow you to readily convert data to the mojo folder layout. Here you can see the scripts you need to make specific conversions:

   | mojo out | hd5 out
   --- | --- | ---
**pngs in** | png2mojo.py | png2hd.py
**hd5 in** | hd2mojo.py | ...

## Installing dependencies

Assuming you have python and pip installed:

```
https://github.com/thejohnhoffer/tools.git
sudo ./tools/install
cd tools
```

If you don't have python or pip installed,
First [get and install python.](https://wiki.python.org/moin/BeginnersGuide/Download)
Then run:

```
https://github.com/thejohnhoffer/tools.git
sudo ./tools/setup/get-pip.py
sudo ./tools/install
cd tools
```

You can then run all three python scripts from the tools directory.

## All three scripts and their parameters

**Before you convert to mojo, make sure you have an output folder called 'mojo'**

* When converting from hdf5 to mojo, you use `./hd2mojo.py [hd5] [out]`
    * `[hd5]` gives the path to one hdf5 file
    * `[out]` gives the path to the mojo folder
    * remember:
        * The first group in the hd5 file is used
        * Use hd5 groups of dtype `uint8` for raw images
        * Any other dtype is assumed to be segmented images of id values

* When converting from pngs:
    * to mojo, you use `./png2mojo.py [pngs] [out]`
        * `[pngs]` gives the path containing png files
        * `[out]` gives the path to the mojo folder
    * to hdf5, you use `./png2hd.py [pngs] [out]`
        * `[pngs]` gives the path containing png files
        * `[out]` gives the full output path/name.hd5:
    * remember:
        * Each png name differs only by a number indicating z-layer
        * Pass `-c` to either function for segmented images of id values
        * Without `-c`, the pngs are assumed to be raw images

## The mojo folder layout

The resulting mojo folders have the following structure:

```
* mojo
    * ids
        * tiles
            * w=00000000
            * ...
            * w=WWWWWWWW
                * z=00000000
                    * x=00000000,y=00000000.hdf5
                    * ...
                    * x=XXXXXXXX,y=YYYYYYYY.hdf5
                * ...
                * z=ZZZZZZZZ
        * colorMap.hdf5
        * segmentInfo.db
        * tiledVolumeDescription.xml

    * images
        * tiles
            * w=00000000
            * ...
            * w=WWWWWWWW
                * z=00000000
                    * x=00000000,y=00000000.hdf5
                    * ...
                    * x=XXXXXXXX,y=YYYYYYYY.hdf5
                * ...
                * z=ZZZZZZZZ
        * tiledVolumeDescription.xml
```

where:

* `w` := How many times each layer is downscaled
* `z` := Number of z-layers from the top of volume
* `x,y` := Offset in units of `(sx,sy)/(2^w)`
* `sx,sy` := `ceil(log2(shape))` nearest power of 2
* `shape` := Original width and height of volume

