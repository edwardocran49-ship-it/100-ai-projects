# Analysis Report: K-Means Clustering for Customer Segmentation

**Author:** Edward Ocran  
**Project:** 3  
**Run status:** Verified locally

## Question

Do annual income and spending score form stable customer segments?

## Data used

The analysis used 200 Mall Customers records. Annual income and spending score were standardized so neither scale dominated the distance calculation.

## Method

K-means was fitted with five clusters, twenty initializations, and a fixed seed. Separation was checked with the silhouette coefficient.

## Results

| Measure | Result |
|---|---:|
| Customers | 200 |
| Clusters | 5 |
| Silhouette score | 0.5547 |

## What the result means

A silhouette score near 0.55 indicates reasonably distinct groups in this two-dimensional view. The result supports the familiar high/low income and high/low spending segments, though the clusters are descriptive rather than proof of different customer needs.

## Limitations

The sample is small and contains no purchase history, geography, tenure, or profitability. K-means also favors spherical groups and forces every customer into exactly one segment.

## Next step

Test two through eight clusters, inspect stability across seeds, and validate the segments against purchase frequency or campaign response.
