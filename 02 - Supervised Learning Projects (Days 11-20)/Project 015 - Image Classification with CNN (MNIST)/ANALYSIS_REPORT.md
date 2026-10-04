# Analysis Report: Image Classification with CNN (MNIST)

**Author:** Edward Ocran  
**Project:** 15  
**Run status:** Verified locally

## Question

How well can a compact convolutional feature pipeline recognize MNIST digits?

## Data used

The run read 12,000 genuine MNIST training images from the Kaggle CSV: 10,000 for fitting and 2,000 for evaluation.

## Method

Sobel-style convolution filters were followed by ReLU, 2×2 max pooling, and a multinomial linear classifier. This keeps the run lightweight while preserving the convolution–activation–pooling structure.

## Results

| Measure | Result |
|---|---:|
| Images used | 12,000 |
| Holdout accuracy | 93.40% |

## What the result means

The compact pipeline gets more than nine of ten digits right, but it trails a learned modern CNN. Fixed edge filters are useful features; they cannot adapt to the digit-specific shapes the way trained kernels can.

## Limitations

The evaluation uses a slice of the training CSV rather than the official test file, and the convolution kernels are fixed. Error rates by digit are not yet shown.

## Next step

Train the kernels end to end with a small PyTorch CNN and evaluate once on the official 10,000-image MNIST test set.
