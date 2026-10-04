# Autoencoder for Noise Reduction — Analysis Report

**Author:** Edward Ocran  
**Project:** 22  
**Validation status:** Reproduced locally from the project dataset and code

## Executive Summary

- The fully connected autoencoder reduces reconstruction MSE from 0.06232 to 0.03242, removing 47.98% of injected-noise error.
- The reduction is material: nearly half of the corruption is removed through a learned 64-unit bottleneck. The remaining error reflects both unrecovered detail and the network’s tendency to smooth fine strokes.
- **Recommended action:** Preserve this benchmark and compare with a nonlinear convolutional autoencoder using the same corruption process.

## Analytical Question

How much injected image noise can a trained fully connected autoencoder remove?

## Data and Evaluation Design

The run uses 6,000 MNIST images scaled to 0-1. Gaussian noise with standard deviation 0.35 is added to each image. A trained fully connected TensorFlow autoencoder compresses 784 pixels through a 64-unit bottleneck and reconstructs the clean target; 5,000 images train the network and 1,000 test it.

## Results

| Measure | Result |
|---|---:|
| Images | 6,000 |
| Noisy-input MSE | 0.06232 |
| Autoencoder reconstruction MSE | 0.03242 |
| Error removed | 47.98% |

## Visual Evidence

![Verified model performance](analysis/performance.png)

![Benchmark and analytical context](analysis/context.png)

## What the Evidence Says

The reduction is material: nearly half of the corruption is removed through a learned 64-unit bottleneck. The remaining error reflects both unrecovered detail and the network’s tendency to smooth fine strokes.

## Risks and Limitations

The corruption is simulated and MSE does not capture every aspect of visual quality. The evaluation uses a sampled MNIST file rather than the official test split.

## Recommendations

1. Preserve this benchmark and compare with a nonlinear convolutional autoencoder using the same corruption process.
2. Save before-and-after image grids and compare the dense model with a convolutional autoencoder under the same noise process.

## Reproducibility Notes

- Run `python main.py --json` from this project folder to reproduce the headline metrics.
- Dataset acquisition and provenance are documented in `DATASET.md` where an external dataset is used.
- Rebuild these figures from the repository root with `python tools/build_analysis_reports.py`.
- Charts are stored as regular PNG files so they render directly in GitHub Markdown.
