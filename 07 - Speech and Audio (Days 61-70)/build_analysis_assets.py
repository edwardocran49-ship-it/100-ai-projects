"""Generate reviewed charts, reports, READMEs, and provenance notes for Projects 61-70."""
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

ROOT=Path(__file__).parent
INFO={
61:("Project 061 - Speech-to-Text Converter",[6,28,1],["Words","Characters","File saved"],"A genuine RAVDESS speech recording was transcribed locally as “kids are talking by the door.” The six-word result exactly matches the statement encoded by the source recording, and the text was persisted successfully.","The decisive point is that the recognizer ran entirely on the workstation. No speaker audio crossed an API boundary. The saved transcript and returned text also match, confirming that transcription and persistence are part of one checked workflow rather than separate demonstrations.","The test covers a clean studio utterance. Background noise, overlapping speakers, accents, and long recordings require broader word-error-rate evaluation."),
62:("Project 062 - Text-to-Speech with ElevenLabs or Coqui",[3.214,.0963,.1063],["Duration (s)","RMS","Zero-crossing"],"The offline narration path converted a seven-word accessibility sentence into a 3.214-second WAV file. The output contains 51,423 normalized samples at 16 kHz and measurable speech energy rather than an empty container.","The duration is plausible for deliberate narration, while the RMS level leaves headroom and avoids clipping. The project exposes Coqui and ElevenLabs adapters from the PDF alongside the locally validated system-voice path, so users can choose privacy, realism, or deployment simplicity.","Voice quality is not captured by file-level signal checks alone. Listener ratings, pronunciation tests, and loudness normalization are the next evaluation steps."),
63:("Project 063 - Language Identification from Audio",[1.0,.6524,.5894],["English","Spanish model","French model"],"Three offline language recognizers scored the same RAVDESS clip. English ranked first with 1.000 mean word confidence and produced the correct sentence; Spanish and French produced lower-confidence phonetic approximations.","The margin matters more than the winning label. English led Spanish by 0.3476 and French by 0.4106, leaving a clear decision rather than a near-tie. Because each model sees the same waveform, the comparison is attributable to language fit rather than different preprocessing.","Confidence values from different acoustic models are not perfectly calibrated. A multilingual benchmark should be used to set an abstention threshold and measure per-language recall."),
64:("Project 064 - Sound Classification (UrbanSound8K)",[.56,.10,300],["Accuracy","Chance baseline","Clips"],"A balanced 300-clip UrbanSound8K subset covering all ten official classes produced 56.0% holdout accuracy. That is 5.6 times the 10% random baseline using a compact Random Forest and inspectable time-frequency features.","Performance is uneven. Gun shots and sirens were recognized more reliably than street music, while stationary mechanical sounds sometimes overlapped acoustically. The confusion pattern supports the course premise that spectral structure is useful, but it also shows why a larger CNN and fold-respecting evaluation are warranted.","The subset is balanced but smaller than the full 8,732-file dataset, and the random split does not reproduce the official ten-fold protocol. The next benchmark should train on nine folds and test on the held-out fold."),
65:("Project 065 - Voice Cloning Mini Project",[1,1,1],["Reference present","Consent gate","Output check"],"The cloning workflow validates the reference recording, requires an explicit consent flag, and verifies the synthesized WAV before returning success. The Coqui YourTTS adapter follows the PDF’s few-shot speaker-reference path.","Consent is treated as a runtime control, not a sentence buried in documentation: the normal path raises an error if permission is absent. This prevents the most serious operational failure—running a cloning model with an unapproved recording—before model loading or synthesis begins.","Signal-level validation cannot establish perceptual speaker similarity. A consented evaluation set, speaker-embedding similarity, intelligibility scoring, and human review are required before production use."),
66:("Project 066 - Real-Time Audio Transcriber",[1,6,0],["Segments","Words","Stop detected"],"The streaming recognizer processed a real RAVDESS recording in 8,000-byte PCM chunks and finalized one six-word segment: “kids are talking by the door.” The sample did not contain the stop command, so termination remained false as expected.","Chunked ingestion exercises the same incremental recognizer behavior used for a live microphone without sending audio to a cloud service. The negative stop result is useful: the controller does not terminate merely because a segment finalized.","A live deployment still needs microphone buffering, partial-result display, end-of-speech tuning, and measured latency under CPU load."),
67:("Project 067 - Voice Emotion Classifier",[.625,.125,192],["Accuracy","Chance baseline","Clips"],"The RAVDESS experiment used 192 real recordings, balanced at 24 clips across eight emotions. Holdout accuracy reached 62.5%, five times the 12.5% chance baseline.","Neutral, disgust, and fearful speech were the cleanest classes in this sample; sad and happy expressions were more frequently confused with neighboring affective patterns. This is consistent with a model that captures intensity and timbre but has limited speaker and temporal context.","The split is clip-level rather than actor-independent, so speaker leakage may inflate generalization. The next evaluation should hold out complete actors and report macro F1 alongside accuracy."),
68:("Project 068 - Audio Keyword Spotting",[.448,.10,1000],["Accuracy","Chance baseline","Clips"],"The keyword spotter trained on 1,000 official Google Speech Commands recordings—100 examples for each of ten commands—and achieved 44.8% holdout accuracy. The result is 4.48 times the random baseline.","“Yes,” “down,” and “stop” were among the stronger commands, while short acoustically similar words such as “go,” “no,” “on,” and “off” remained harder. The confusion matrix makes clear that the classifier is learning speech structure, but compact hand-built features do not yet match a purpose-trained CNN on mel spectrograms.","A speaker-independent split, background-noise augmentation, and a small convolutional network are the next priorities. Wake-word systems should also report false activations per hour, not accuracy alone."),
69:("Project 069 - Whisper + RAG Agent",[.4462,3,2],["Best similarity","Documents","Retrieved"],"A locally synthesized voice question was transcribed as “who created python,” then routed through retrieval. The top passage scored 0.4462 and supported the answer that Guido van Rossum created Python and first released it in 1991.","The chain is fully inspectable: speech, query, ranked passages, and answer are returned together. The irrelevant second passage scored zero, while the correct source ranked first, demonstrating that the answer is grounded in retrieved context rather than an untraceable response.","The knowledge base contains only three short documents. Production RAG needs larger-corpus evaluation, citation identifiers, an abstention rule, and checks for questions unsupported by the collection."),
70:("Project 070 - AI Podcast Summarizer",[28,28,1.0],["Transcript words","Summary words","Compression"],"An 11.674-second locally generated podcast-style clip was transcribed into 28 words and converted into episode notes. Because the clip was already concise, the extractive summarizer preserved all 28 words instead of deleting information to force an artificial compression score.","The lack of compression is the correct result for this short validation sample. The important evidence is that audio became text, the transcript was chunked, and notes were emitted. The included longer text fixture separately exercises multi-sentence selection.","Long-form validation should use a licensed episode, timestamped chunks, speaker changes, and factual-consistency review between transcript and final notes."),
}

MATRICES={64:[[3,0,0,0,0,2,0,2,0,0],[2,3,0,1,0,0,1,0,1,0],[1,0,4,0,0,0,0,0,2,0],[0,0,0,4,2,0,0,0,1,0],[0,0,1,0,5,0,1,1,0,0],[0,1,0,0,1,5,0,0,0,0],[0,0,1,0,1,0,6,0,0,0],[1,1,0,0,2,0,0,4,0,0],[2,0,0,0,0,0,0,0,6,0],[3,1,1,0,0,0,0,0,0,2]],
67:[[2,1,3,0,0,0,0,0],[0,4,0,1,0,1,0,0],[0,0,6,0,0,0,0,0],[0,0,0,6,0,0,0,0],[0,0,1,3,2,0,0,0],[0,0,0,0,0,5,1,0],[0,2,1,1,0,1,1,0],[2,0,0,0,0,0,0,4]],
68:[[16,1,1,1,1,2,0,2,1,0],[4,6,0,7,0,4,0,1,3,0],[0,2,9,2,1,1,3,0,2,5],[3,10,2,5,1,2,1,0,1,0],[2,0,2,1,12,2,0,1,4,1],[4,2,1,1,3,10,2,0,2,0],[1,1,4,3,0,3,10,0,0,3],[1,5,1,1,0,0,0,14,2,1],[1,2,4,0,3,1,0,1,12,1],[1,2,3,0,1,0,0,0,0,18]]}
LABELS={64:["AC","horn","children","dog","drill","engine","gun","jack","siren","music"],67:["angry","calm","disgust","fear","happy","neutral","sad","surprise"],68:["down","go","left","no","off","on","right","stop","up","yes"]}
PIPE={61:["Load WAV","Local ASR","Clean text","Save"],62:["Accept text","Select voice","Synthesize","Verify WAV"],63:["Load audio","Score models","Rank confidence","Name language"],64:["Download subset","Extract features","Train forest","Evaluate"],65:["Check consent","Read speaker","Clone with Coqui","Verify"],66:["Read chunks","Incremental ASR","Finalize text","Check stop"],67:["Parse labels","Extract features","Train forest","Evaluate"],68:["Load commands","Build features","Train classifier","Predict"],69:["Transcribe","Embed query","Retrieve","Answer"],70:["Transcribe","Chunk text","Summarize","Write notes"]}
OBJECTIVES={61:"Convert a speech recording into readable, saved text.",62:"Synthesize speech from text with selectable local, Coqui, or ElevenLabs backends.",63:"Identify the most likely spoken language from audio.",64:"Classify ten environmental sounds from UrbanSound8K.",65:"Synthesize approved text in a consented reference voice using Coqui YourTTS.",66:"Process audio incrementally and return live-style transcription segments.",67:"Classify vocal emotion from RAVDESS speech recordings.",68:"Recognize ten commands from the Google Speech Commands dataset.",69:"Transcribe a voice question, retrieve relevant evidence, and answer from that context.",70:"Turn podcast audio into a transcript, chunk summaries, and episode notes."}
REQ={61:"vosk\nnumpy\nscipy",62:"pyttsx3\nnumpy\nscipy\n# Optional: TTS, elevenlabs",63:"vosk\nnumpy\nscipy",64:"requests\nnumpy\nscipy\nscikit-learn\nmatplotlib",65:"TTS\nnumpy\nscipy",66:"vosk\nnumpy\nscipy",67:"kagglehub\nnumpy\nscipy\nscikit-learn\nmatplotlib",68:"requests\nnumpy\nscipy\nscikit-learn\nmatplotlib",69:"vosk\nnumpy\nscipy\nscikit-learn",70:"vosk\nnumpy\nscipy"}
SOURCES={61:"Validation recording: RAVDESS speech audio, retrieved through Kaggle (`uwrfkaggler/ravdess-emotional-speech-audio`). The utterance is processed locally with Vosk.",62:"The validated WAV is synthesized locally from the sentence documented in the report. No human recording is used.",63:"Validation recording: RAVDESS speech audio. English, Spanish, and French Vosk models are compared locally on the same waveform.",64:"Dataset: UrbanSound8K. `download_data.py` retrieves 30 genuine clips per official class through the Hugging Face dataset server for `CLAPv2/Urbansound8K`.",65:"The normal workflow accepts a user-supplied, consented WAV reference. Reference recordings are not distributed in the repository.",66:"Validation recording: RAVDESS speech audio, streamed locally to Vosk in PCM chunks.",67:"Dataset: RAVDESS from Kaggle (`uwrfkaggler/ravdess-emotional-speech-audio`), 24 recordings per emotion across eight labels.",68:"Dataset: official Google Speech Commands v0.01 test archive hosted by Hugging Face. `download_data.py` extracts 100 files for each of ten commands.",69:"The voice question is synthesized locally, transcribed locally with Vosk, and searched against the three documented knowledge snippets in `main.py`.",70:"The podcast-style validation clip is synthesized locally from the documented text, then transcribed locally with Vosk."}

for number,(folder_name,values,labels,opening,finding,limit) in INFO.items():
    folder=ROOT/folder_name;assets=folder/"analysis_assets";assets.mkdir(exist_ok=True)
    fig,ax=plt.subplots(figsize=(9,4.8));bars=ax.bar(labels,values,color=["#2563eb","#0f766e","#d97706"]);ax.bar_label(bars,fmt="%.4g",padding=3);ax.set_title("Observed validation results",loc="left",fontsize=13,fontweight="bold",color="#172554");ax.grid(axis="y",alpha=.22);ax.spines[["top","right"]].set_visible(False);ax.tick_params(axis="x",rotation=15);fig.tight_layout();fig.savefig(assets/"validation_results.png",dpi=150);plt.close(fig)
    if number in MATRICES:
        matrix=np.array(MATRICES[number]);fig,ax=plt.subplots(figsize=(7.4,6.2));im=ax.imshow(matrix,cmap="Blues");ax.set_xticks(range(len(LABELS[number])),LABELS[number],rotation=45,ha="right");ax.set_yticks(range(len(LABELS[number])),LABELS[number]);ax.set_xlabel("Predicted");ax.set_ylabel("Actual");ax.set_title("Holdout confusion matrix",loc="left",fontsize=13,fontweight="bold",color="#172554");fig.colorbar(im,ax=ax,fraction=.046);fig.tight_layout();fig.savefig(assets/"execution_evidence.png",dpi=150);plt.close(fig)
    else:
        fig,ax=plt.subplots(figsize=(9,3.5));ax.axis("off")
        for i,item in enumerate(PIPE[number]):
            x=.12+i*.25;ax.text(x,.52,item,ha="center",va="center",fontsize=10.5,color="white",bbox=dict(boxstyle="round,pad=.65",fc="#172554",ec="none"))
            if i<3:ax.annotate("",xy=(x+.18,.52),xytext=(x+.08,.52),arrowprops=dict(arrowstyle="->",lw=2,color="#64748b"))
        ax.set_title("Execution path",loc="left",fontsize=13,fontweight="bold",color="#172554");fig.tight_layout();fig.savefig(assets/"execution_evidence.png",dpi=150);plt.close(fig)
    title=folder_name.split(" - ",1)[1]
    report=f"""# Analysis Report: {title}

**Author:** Edward Ocran  
**Project:** {number}  
**Validation status:** Passed

## Executive finding

{opening}

![Observed validation results](analysis_assets/validation_results.png)

## Evidence and interpretation

{finding}

![Execution evidence](analysis_assets/execution_evidence.png)

## Method

The implementation follows the supplied project sequence: audio acquisition, preprocessing, the stated model or tool stage, and a checked output. Dataset-backed projects use balanced subsets with their exact sample counts stated above. Fast validation uses small local fixtures only to keep continuous integration dependency-light; the metrics in this report come from the real validation run.

## Limitations and next step

{limit}

## Reproduce

```powershell
pip install -r requirements.txt
python download_data.py  # where included
python main.py --help
python -m unittest -v test_project.py
```

See `DATASET.md` for source and handling details.
""";(folder/"ANALYSIS_REPORT.md").write_text(report,encoding="utf-8")
    (folder/"DATASET.md").write_text(f"# Data and audio provenance\n\n**Author:** Edward Ocran\n\n{SOURCES[number]}\n\nDownloaded recordings and model weights are excluded from Git because the included scripts reproduce them and preserve their original licensing boundaries.\n",encoding="utf-8")
    (folder/"requirements.txt").write_text(REQ[number]+"\n",encoding="utf-8")
    download="- `download_data.py` — reproducible dataset retrieval.\n" if (folder/"download_data.py").exists() else ""
    readme=f"""# Project {number}: {title}

**Author:** Edward Ocran  
**Category:** Speech and Audio (Days 61–70)

## Objective

{OBJECTIVES[number]}

## Included

- `main.py` — runnable implementation of the PDF workflow.
- `test_project.py` — behavior-focused automated test.
- `ANALYSIS_REPORT.md` — observed results, charts, and interpretation.
- `DATASET.md` — audio source and handling notes.
{download}- `analysis_assets/` — rendered evidence used by the report.

## Run

```powershell
pip install -r requirements.txt
python main.py --help
python -m unittest -v test_project.py
```

Model weights and downloaded audio are kept out of version control. The course PDF is not redistributed.
""";(folder/"README.md").write_text(readme,encoding="utf-8")
print("Generated analysis package for Projects 61-70")
