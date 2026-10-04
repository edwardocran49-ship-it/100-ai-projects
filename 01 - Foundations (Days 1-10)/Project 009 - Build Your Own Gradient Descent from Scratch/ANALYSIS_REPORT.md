# Analysis Report: Build Your Own Gradient Descent from Scratch

**Author:** Edward Ocran  
**Project:** 9  
**Run status:** Verified locally

## Question

Can a hand-written gradient descent loop recover a known linear relationship?

## Data used

This exercise intentionally generates 100 reproducible observations from a line with slope 3.2 and intercept 4.5, plus small uniform noise. No external dataset is appropriate here because the goal is to verify the optimizer itself.

## Method

Slope and intercept start at zero and are updated for 5,000 full-batch iterations using analytically derived mean-squared-error gradients.

## Results

| Measure | Result |
|---|---:|
| Observations | 100 |
| Learned slope | 3.2059 |
| Learned intercept | 4.4602 |
| Final MSE | 0.021286 |

## What the result means

The learned parameters land close to the generating values, and the remaining error matches the injected noise. That is the result this exercise should produce: evidence that the gradient implementation converges rather than evidence about a real-world population.

## Limitations

The problem is convex, one-dimensional, and well scaled. It does not expose the optimizer to correlated features, poor conditioning, minibatches, or local minima.

## Next step

Add convergence plots, feature scaling experiments, and a multivariate version checked against scikit-learn's closed-form solution.
