# Detecting deepfakes images processed with JPEG AI

## Compression of the dataset

## Evaluation

## Forensic analysis
It is crucial to observe how JPEG AI modifies the frequency components of a given image, whether it is real or a deepfake. Regardless of the veracity of an image, JPEG AI tends to leave recognizable traces in images in the frequency domain, and it is also possible to recognize how these traces vary based on BPP.

An immediate example is the following, in which the average of the azimuthal average is evaluated on a set of images:

<div align="center">
<img src="data/plots/az_avarage_gaugan_real.png" width="400">
</div>

these profiles were calculated on the real images of the _Gaugan_ dataset, compressing the images at 12, 50 and 100 BPP.
Note how compressed images tend to have an increasingly lower average energy than uncompressed images, and the average energy of compressed images is higher if the BPP is higher. All compressed images have the same anomaly: A high frequency energy peak, which uncompressed images do not have (around 180 Hz).

More details [here](https://github.com/CasuFrost/JPEG-AI-deepfake-detection/tree/main/results/frequency_analysis.md).

## Mitigation strategies