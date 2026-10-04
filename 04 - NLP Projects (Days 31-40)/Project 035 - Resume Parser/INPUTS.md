# Input record

The included data/sample_resume.txt is a fictional, non-sensitive resume created solely to demonstrate the parser. The command also accepts a path to a user-provided TXT or PDF resume.

PDF text is extracted with pdfplumber; contact details use regular expressions; names use spaCy entities; and skills and resume sections use transparent matching rules.
