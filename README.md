# Synthetic-Image-Generator
A script to generate training data for image recognition models

## Prerequisites
A list of dependencies are stored in `requirements.txt`

```
pip install -r requirements.txt
```

This script overlays supplied images on supplied backgrounds and provides label files.

## Setup

- Images should be placed in `/data/foreground/`.  These should be png images with an alpha layer applied.  The name of the file will also serve as the class name for labeling.

- Background images should be placed in `/data/background/`.  These should be jpg images; file name does not matter.

- The generated images will be saved in `/output/images/` and will be named "output_xxxxxx.jpg".

- The generated labels will be saved in `/output/labels/` with the same name as the corresponding image, "output_xxxxxx.txt".

The labels follow a commonly used labeling convention:
```
<class> <center_x> <center_y> <width> <height>

where center_x, center_y, width, and height are from [0,1] as a proportion of the total image dimensions
```
