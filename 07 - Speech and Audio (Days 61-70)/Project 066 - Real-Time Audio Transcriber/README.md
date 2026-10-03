    # Project 66: Real-Time Audio Transcriber

    **Author:** Edward Ocran  
    **Category:** 07 - Speech and Audio (Days 61-70)  
    **Implementation type:** Audio

    ## Objective

    Capture audio from a microphone and transcribe it live using a speech-to-text engine

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

    - `pip install SpeechRecognition pyaudio`
- `pip install pipwin`
- `pip install openai-whisper sounddevice numpy`

    ## Success criteria

    The command exits successfully, returns `status: ok`, includes task metrics, and passes the included smoke test.
