    # Project 39: Chatbot Using DialoGPT or RAG

    **Author:** Edward Ocran  
    **Category:** 04 - NLP Projects (Days 31-40)  
    **Implementation type:** Nlp

    ## Objective

    Free-form chatting

    ## What is included

    - `main.py` - deterministic, offline runnable implementation.
    - `test_project.py` - automated smoke test.
    - `course-requirements.txt` - dependency commands mentioned by the course, when present.

    ## Run

    ```powershell
    python main.py
    python -m unittest -v test_project.py
    ```

    The default demo uses generated sample data so it runs without API keys, paid services, or large model downloads. Replace the sample data with the dataset or service described in the PDF when extending the project.

    ## Course dependency guidance

    - `pip install transformers torch`
- `pip install transformers faiss-cpu`

    ## Success criteria

    The command exits successfully, returns `status: ok`, includes task metrics, and passes the included smoke test.
