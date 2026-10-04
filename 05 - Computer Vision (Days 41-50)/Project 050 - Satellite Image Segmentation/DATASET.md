# Dataset record

- **Name:** DeepGlobe Land Cover Classification
- **Source:** https://www.kaggle.com/datasets/balraj98/deepglobe-land-cover-classification-dataset
- **Task:** seven-class pixel-wise land-cover segmentation
- **Retrieval:** run python download_data.py

The complete satellite dataset remains in KaggleHub's versioned cache. The default run reads paired satellite and color-mask files, maps mask colors to class IDs, and trains a compact UNet-style encoder-decoder.

