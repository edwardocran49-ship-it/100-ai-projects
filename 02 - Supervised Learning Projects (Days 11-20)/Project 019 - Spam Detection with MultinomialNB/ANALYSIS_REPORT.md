# Analysis Report: Spam Detection with MultinomialNB

**Author:** Edward Ocran  
**Project:** 19  
**Run status:** Verified locally

## Question

How effectively does a bag-of-words MultinomialNB model catch SMS spam?

## Data used

The same 5,572-message SMS Spam Collection was split with label stratification. This project uses raw counts rather than TF-IDF, making it a useful comparison with Project 6.

## Method

English stop words were removed by `CountVectorizer`, followed by Multinomial Naive Bayes.

## Results

| Measure | Result |
|---|---:|
| Messages | 5,572 |
| Accuracy | 98.39% |
| Spam F1 | 93.84% |

## What the result means

On this split, count features outperformed the TF-IDF baseline from Project 6, especially on spam F1. The result suggests that repeated token evidence is valuable in this corpus, though the comparison should be confirmed across the same cross-validation folds.

## Limitations

The corpus is dated and English-only. Random splitting may place near-duplicate campaign wording in both sets, and modern URL or sender signals are not included.

## Next step

Deduplicate messages, compare both representations under repeated cross-validation, and test on a newer scam corpus.
