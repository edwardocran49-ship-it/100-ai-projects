# Web source

- **Page:** Artificial intelligence
- **Source:** https://en.wikipedia.org/wiki/Artificial_intelligence
- **Retrieval:** live HTTP request during the normal run

Paragraph text is chunked into memory once. Questions retrieve the closest stored passages with TF-IDF cosine similarity, preserving the page URL with each result.
