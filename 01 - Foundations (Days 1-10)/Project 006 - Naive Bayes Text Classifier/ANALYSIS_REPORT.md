# Analysis Report: Naive Bayes Text Classifier

**Author:** Edward Ocran  
**Project:** 6  
**Run status:** Verified locally

## Question

Can word-frequency evidence separate spam from legitimate SMS messages?

## Data used

The SMS Spam Collection supplied 5,572 labeled messages. Text was converted to TF-IDF features after a stratified train/test split.

## Method

A Multinomial Naive Bayes classifier was fitted to the sparse TF-IDF matrix. I report both accuracy and spam-class F1 because the classes are imbalanced.

## Results

| Measure | Result |
|---|---:|
| Messages | 5,572 |
| Accuracy | 96.86% |
| Spam F1 | 86.69% |

## What the result means

Overall accuracy is high, but the lower spam F1 shows that minority-class errors remain the harder part of the task. That gap matters more than the headline accuracy for an inbox filter.

## Limitations

SMS language changes over time, and this corpus is mostly older English-language text. URL patterns, sender metadata, adversarial spelling, and modern scam themes are not modeled.

## Next step

Inspect false positives, tune the decision threshold, and compare character n-grams with a time-aware evaluation set.
