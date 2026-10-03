    # Project 62: Text-to-Speech with ElevenLabs or Coqui

    **Author:** Edward Ocran  
    **Category:** 07 - Speech and Audio (Days 61-70)  
    **Implementation type:** Nlp

    ## Objective

    Turn any input text into audio speech output, with support for voice selection, saving

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

    - `pip install elevenlabs`
- `pip install TTS`

    ## Success criteria

    The command exits successfully, returns `status: ok`, includes task metrics, and passes the included smoke test.
