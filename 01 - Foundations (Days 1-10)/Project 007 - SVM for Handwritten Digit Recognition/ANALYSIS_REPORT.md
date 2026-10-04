# Analysis Report: SVM for Handwritten Digit Recognition

**Author:** Edward Ocran  
**Project:** 7  
**Run status:** Verified locally

## Question

How well does an RBF support-vector machine recognize small handwritten digit images?

## Data used

The scikit-learn digits dataset contains 1,797 labeled 8×8 grayscale images. Pixel values were standardized before fitting.

## Method

An RBF SVM with `C=5` was trained on a stratified 80% split.

## Results

| Measure | Result |
|---|---:|
| Images | 1,797 |
| Holdout accuracy | 98.06% |

## What the result means

The model missed about two images in every hundred on the holdout set. This is a strong result for the low-resolution digits benchmark and confirms that nonlinear boundaries suit the pixel representation.

## Limitations

These 8×8 images are cleaner and smaller than real handwriting. The report does not yet show which digit pairs are confused or how performance changes under rotation and noise.

## Next step

Add a confusion matrix, visualize support-vector errors, and test robustness with shifted and noisy images.
