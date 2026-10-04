# Dataset record

- **Name:** PlantVillage plant disease dataset
- **Source:** https://www.kaggle.com/datasets/emmarex/plantdisease
- **Default evaluation sample:** 240 images across healthy tomato, early blight, and late blight
- **Retrieval:** run python download_data.py

The full Kaggle dataset remains in KaggleHub's versioned cache. The project draws a reproducible balanced subset, resizes images to 32×32, and trains the PDF-specified two-layer CNN.

