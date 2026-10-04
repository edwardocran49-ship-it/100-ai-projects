# 100 AI Projects


> The licensed course PDFs are not included in this public repository. Each implementation and test is original portfolio code.
**Author:** Edward Ocran

A 100-project AI learning portfolio organized into ten course-aligned sections. Each project contains a runnable implementation, setup guidance, and an automated smoke test. Dataset-backed projects use the named source from the course wherever it is available; projects based on APIs, pretrained models, user-supplied files, or an explicitly simulated exercise identify that input honestly.

## Dataset policy

- Small redistributable datasets are stored beside their projects in `data/`.
- Large or access-controlled datasets use a reproducible downloader and remain outside Git.
- Every upgraded data project includes `DATASET.md` with its source, local path, size, retrieval date, and licensing/provenance note.
- Every completed project includes `ANALYSIS_REPORT.md` with the measured result, a plain-language interpretation, limitations, and a concrete next step.
- The course PDFs are not redistributed.

## Validate everything

```powershell
python -m pip install -r requirements.txt
python validate_all.py
```

## Project index

| # | Project | Section | Demo type |
|---:|---|---|---|
| 1 | [Predict House Prices (Boston Housing Dataset)](01%20-%20Foundations%20(Days%201-10)/Project%20001%20-%20Predict%20House%20Prices%20(Boston%20Housing%20Dataset)/README.md) | 01 - Foundations (Days 1-10) | regression |
| 2 | [Logistic Regression on Titanic Dataset](01%20-%20Foundations%20(Days%201-10)/Project%20002%20-%20Logistic%20Regression%20on%20Titanic%20Dataset/README.md) | 01 - Foundations (Days 1-10) | regression |
| 3 | [K-Means Clustering for Customer Segmentation](01%20-%20Foundations%20(Days%201-10)/Project%20003%20-%20K-Means%20Clustering%20for%20Customer%20Segmentation/README.md) | 01 - Foundations (Days 1-10) | clustering |
| 4 | [Decision Tree Classifier for Credit Risk](01%20-%20Foundations%20(Days%201-10)/Project%20004%20-%20Decision%20Tree%20Classifier%20for%20Credit%20Risk/README.md) | 01 - Foundations (Days 1-10) | classification |
| 5 | [Random Forest on Breast Cancer Dataset](01%20-%20Foundations%20(Days%201-10)/Project%20005%20-%20Random%20Forest%20on%20Breast%20Cancer%20Dataset/README.md) | 01 - Foundations (Days 1-10) | classification |
| 6 | [Naive Bayes Text Classifier](01%20-%20Foundations%20(Days%201-10)/Project%20006%20-%20Naive%20Bayes%20Text%20Classifier/README.md) | 01 - Foundations (Days 1-10) | nlp |
| 7 | [SVM for Handwritten Digit Recognition](01%20-%20Foundations%20(Days%201-10)/Project%20007%20-%20SVM%20for%20Handwritten%20Digit%20Recognition/README.md) | 01 - Foundations (Days 1-10) | classification |
| 8 | [PCA for Dimensionality Reduction](01%20-%20Foundations%20(Days%201-10)/Project%20008%20-%20PCA%20for%20Dimensionality%20Reduction/README.md) | 01 - Foundations (Days 1-10) | classification |
| 9 | [Build Your Own Gradient Descent from Scratch](01%20-%20Foundations%20(Days%201-10)/Project%20009%20-%20Build%20Your%20Own%20Gradient%20Descent%20from%20Scratch/README.md) | 01 - Foundations (Days 1-10) | classification |
| 10 | [Hyperparameter Tuning with GridSearchCV](01%20-%20Foundations%20(Days%201-10)/Project%20010%20-%20Hyperparameter%20Tuning%20with%20GridSearchCV/README.md) | 01 - Foundations (Days 1-10) | classification |
| 11 | [Predict Stock Prices with LSTM](02%20-%20Supervised%20Learning%20Projects%20(Days%2011-20)/Project%20011%20-%20Predict%20Stock%20Prices%20with%20LSTM/README.md) | 02 - Supervised Learning Projects (Days 11-20) | regression |
| 12 | [Predict Bike Rentals with Time-Series Models](02%20-%20Supervised%20Learning%20Projects%20(Days%2011-20)/Project%20012%20-%20Predict%20Bike%20Rentals%20with%20Time-Series%20Models/README.md) | 02 - Supervised Learning Projects (Days 11-20) | regression |
| 13 | [Forecast Weather Using ARIMA](02%20-%20Supervised%20Learning%20Projects%20(Days%2011-20)/Project%20013%20-%20Forecast%20Weather%20Using%20ARIMA/README.md) | 02 - Supervised Learning Projects (Days 11-20) | regression |
| 14 | [Predict Heart Disease with XGBoost](02%20-%20Supervised%20Learning%20Projects%20(Days%2011-20)/Project%20014%20-%20Predict%20Heart%20Disease%20with%20XGBoost/README.md) | 02 - Supervised Learning Projects (Days 11-20) | classification |
| 15 | [Image Classification with CNN (MNIST)](02%20-%20Supervised%20Learning%20Projects%20(Days%2011-20)/Project%20015%20-%20Image%20Classification%20with%20CNN%20(MNIST)/README.md) | 02 - Supervised Learning Projects (Days 11-20) | vision |
| 16 | [Voice Gender Classifier](02%20-%20Supervised%20Learning%20Projects%20(Days%2011-20)/Project%20016%20-%20Voice%20Gender%20Classifier/README.md) | 02 - Supervised Learning Projects (Days 11-20) | audio |
| 17 | [Flight Delay Predictor](02%20-%20Supervised%20Learning%20Projects%20(Days%2011-20)/Project%20017%20-%20Flight%20Delay%20Predictor/README.md) | 02 - Supervised Learning Projects (Days 11-20) | classification |
| 18 | [Student Grade Predictor with Linear Regression](02%20-%20Supervised%20Learning%20Projects%20(Days%2011-20)/Project%20018%20-%20Student%20Grade%20Predictor%20with%20Linear%20Regression/README.md) | 02 - Supervised Learning Projects (Days 11-20) | regression |
| 19 | [Spam Detection with MultinomialNB](02%20-%20Supervised%20Learning%20Projects%20(Days%2011-20)/Project%20019%20-%20Spam%20Detection%20with%20MultinomialNB/README.md) | 02 - Supervised Learning Projects (Days 11-20) | classification |
| 20 | [Fraud Detection with Isolation Forests](02%20-%20Supervised%20Learning%20Projects%20(Days%2011-20)/Project%20020%20-%20Fraud%20Detection%20with%20Isolation%20Forests/README.md) | 02 - Supervised Learning Projects (Days 11-20) | classification |
| 21 | [Anomaly Detection in Server Logs](03%20-%20Unsupervised%20+%20Semi-Supervised%20(Days%2021-30)/Project%20021%20-%20Anomaly%20Detection%20in%20Server%20Logs/README.md) | 03 - Unsupervised + Semi-Supervised (Days 21-30) | classification |
| 22 | [Autoencoder for Noise Reduction](03%20-%20Unsupervised%20+%20Semi-Supervised%20(Days%2021-30)/Project%20022%20-%20Autoencoder%20for%20Noise%20Reduction/README.md) | 03 - Unsupervised + Semi-Supervised (Days 21-30) | classification |
| 23 | [Clustering Movie Genres with K-Means](03%20-%20Unsupervised%20+%20Semi-Supervised%20(Days%2021-30)/Project%20023%20-%20Clustering%20Movie%20Genres%20with%20K-Means/README.md) | 03 - Unsupervised + Semi-Supervised (Days 21-30) | clustering |
| 24 | [Dimensionality Reduction with t-SNE](03%20-%20Unsupervised%20+%20Semi-Supervised%20(Days%2021-30)/Project%20024%20-%20Dimensionality%20Reduction%20with%20t-SNE/README.md) | 03 - Unsupervised + Semi-Supervised (Days 21-30) | classification |
| 25 | [Self-Supervised Pretraining on Images](03%20-%20Unsupervised%20+%20Semi-Supervised%20(Days%2021-30)/Project%20025%20-%20Self-Supervised%20Pretraining%20on%20Images/README.md) | 03 - Unsupervised + Semi-Supervised (Days 21-30) | vision |
| 26 | [Semi-Supervised Learning for Document Labeling](03%20-%20Unsupervised%20+%20Semi-Supervised%20(Days%2021-30)/Project%20026%20-%20Semi-Supervised%20Learning%20for%20Document%20Labeling/README.md) | 03 - Unsupervised + Semi-Supervised (Days 21-30) | classification |
| 27 | [Outlier Detection in Financial Data](03%20-%20Unsupervised%20+%20Semi-Supervised%20(Days%2021-30)/Project%20027%20-%20Outlier%20Detection%20in%20Financial%20Data/README.md) | 03 - Unsupervised + Semi-Supervised (Days 21-30) | classification |
| 28 | [Gaussian Mixture Models for Speaker Identification](03%20-%20Unsupervised%20+%20Semi-Supervised%20(Days%2021-30)/Project%20028%20-%20Gaussian%20Mixture%20Models%20for%20Speaker%20Identification/README.md) | 03 - Unsupervised + Semi-Supervised (Days 21-30) | clustering |
| 29 | [Hierarchical Clustering on E-commerce Data](03%20-%20Unsupervised%20+%20Semi-Supervised%20(Days%2021-30)/Project%20029%20-%20Hierarchical%20Clustering%20on%20E-commerce%20Data/README.md) | 03 - Unsupervised + Semi-Supervised (Days 21-30) | clustering |
| 30 | [Build a User-Based Recommender System](03%20-%20Unsupervised%20+%20Semi-Supervised%20(Days%2021-30)/Project%20030%20-%20Build%20a%20User-Based%20Recommender%20System/README.md) | 03 - Unsupervised + Semi-Supervised (Days 21-30) | clustering |
| 31 | [Sentiment Analysis with BERT](04%20-%20NLP%20Projects%20(Days%2031-40)/Project%20031%20-%20Sentiment%20Analysis%20with%20BERT/README.md) | 04 - NLP Projects (Days 31-40) | nlp |
| 32 | [Text Summarizer with T5](04%20-%20NLP%20Projects%20(Days%2031-40)/Project%20032%20-%20Text%20Summarizer%20with%20T5/README.md) | 04 - NLP Projects (Days 31-40) | nlp |
| 33 | [Question Answering System (Using Transformers)](04%20-%20NLP%20Projects%20(Days%2031-40)/Project%20033%20-%20Question%20Answering%20System%20(Using%20Transformers)/README.md) | 04 - NLP Projects (Days 31-40) | nlp |
| 34 | [Email Spam Classifier](04%20-%20NLP%20Projects%20(Days%2031-40)/Project%20034%20-%20Email%20Spam%20Classifier/README.md) | 04 - NLP Projects (Days 31-40) | nlp |
| 35 | [Resume Parser](04%20-%20NLP%20Projects%20(Days%2031-40)/Project%20035%20-%20Resume%20Parser/README.md) | 04 - NLP Projects (Days 31-40) | nlp |
| 36 | [Named Entity Recognition with spaCy](04%20-%20NLP%20Projects%20(Days%2031-40)/Project%20036%20-%20Named%20Entity%20Recognition%20with%20spaCy/README.md) | 04 - NLP Projects (Days 31-40) | nlp |
| 37 | [Semantic Search with Sentence Transformers](04%20-%20NLP%20Projects%20(Days%2031-40)/Project%20037%20-%20Semantic%20Search%20with%20Sentence%20Transformers/README.md) | 04 - NLP Projects (Days 31-40) | nlp |
| 38 | [Zero-Shot Text Classification](04%20-%20NLP%20Projects%20(Days%2031-40)/Project%20038%20-%20Zero-Shot%20Text%20Classification/README.md) | 04 - NLP Projects (Days 31-40) | nlp |
| 39 | [Chatbot Using DialoGPT or RAG](04%20-%20NLP%20Projects%20(Days%2031-40)/Project%20039%20-%20Chatbot%20Using%20DialoGPT%20or%20RAG/README.md) | 04 - NLP Projects (Days 31-40) | nlp |
| 40 | [Multilingual Translation Bot](04%20-%20NLP%20Projects%20(Days%2031-40)/Project%20040%20-%20Multilingual%20Translation%20Bot/README.md) | 04 - NLP Projects (Days 31-40) | nlp |
| 41 | [Face Detection and Blur](05%20-%20Computer%20Vision%20(Days%2041-50)/Project%20041%20-%20Face%20Detection%20and%20Blur/README.md) | 05 - Computer Vision (Days 41-50) | vision |
| 42 | [Image Caption Generator](05%20-%20Computer%20Vision%20(Days%2041-50)/Project%20042%20-%20Image%20Caption%20Generator/README.md) | 05 - Computer Vision (Days 41-50) | vision |
| 43 | [Object Detection with YOLOv8](05%20-%20Computer%20Vision%20(Days%2041-50)/Project%20043%20-%20Object%20Detection%20with%20YOLOv8/README.md) | 05 - Computer Vision (Days 41-50) | vision |
| 44 | [Image Style Transfer (Neural Style Transfer)](05%20-%20Computer%20Vision%20(Days%2041-50)/Project%20044%20-%20Image%20Style%20Transfer%20(Neural%20Style%20Transfer)/README.md) | 05 - Computer Vision (Days 41-50) | vision |
| 45 | [License Plate Detection](05%20-%20Computer%20Vision%20(Days%2041-50)/Project%20045%20-%20License%20Plate%20Detection/README.md) | 05 - Computer Vision (Days 41-50) | vision |
| 46 | [OCR for Handwritten Notes](05%20-%20Computer%20Vision%20(Days%2041-50)/Project%20046%20-%20OCR%20for%20Handwritten%20Notes/README.md) | 05 - Computer Vision (Days 41-50) | vision |
| 47 | [Plant Disease Classifier](05%20-%20Computer%20Vision%20(Days%2041-50)/Project%20047%20-%20Plant%20Disease%20Classifier/README.md) | 05 - Computer Vision (Days 41-50) | vision |
| 48 | [Emotion Detection from Faces](05%20-%20Computer%20Vision%20(Days%2041-50)/Project%20048%20-%20Emotion%20Detection%20from%20Faces/README.md) | 05 - Computer Vision (Days 41-50) | vision |
| 49 | [Image Super-Resolution with SRGAN](05%20-%20Computer%20Vision%20(Days%2041-50)/Project%20049%20-%20Image%20Super-Resolution%20with%20SRGAN/README.md) | 05 - Computer Vision (Days 41-50) | vision |
| 50 | [Satellite Image Segmentation](05%20-%20Computer%20Vision%20(Days%2041-50)/Project%20050%20-%20Satellite%20Image%20Segmentation/README.md) | 05 - Computer Vision (Days 41-50) | vision |
| 51 | [Math Reasoning Agent (ReAct Pattern)](06%20-%20AI%20Agents%20+%20Automation%20(Days%2051-60)/Project%20051%20-%20Math%20Reasoning%20Agent%20(ReAct%20Pattern)/README.md) | 06 - AI Agents + Automation (Days 51-60) | agent |
| 52 | [Coding Bot with Tool Use](06%20-%20AI%20Agents%20+%20Automation%20(Days%2051-60)/Project%20052%20-%20Coding%20Bot%20with%20Tool%20Use/README.md) | 06 - AI Agents + Automation (Days 51-60) | agent |
| 53 | [PDF Summarizer with Agents](06%20-%20AI%20Agents%20+%20Automation%20(Days%2051-60)/Project%20053%20-%20PDF%20Summarizer%20with%20Agents/README.md) | 06 - AI Agents + Automation (Days 51-60) | agent |
| 54 | [AI Calendar Scheduler Agent](06%20-%20AI%20Agents%20+%20Automation%20(Days%2051-60)/Project%20054%20-%20AI%20Calendar%20Scheduler%20Agent/README.md) | 06 - AI Agents + Automation (Days 51-60) | agent |
| 55 | [Self-Correcting Essay Grader](06%20-%20AI%20Agents%20+%20Automation%20(Days%2051-60)/Project%20055%20-%20Self-Correcting%20Essay%20Grader/README.md) | 06 - AI Agents + Automation (Days 51-60) | agent |
| 56 | [File Organizer Agent (Desktop AI)](06%20-%20AI%20Agents%20+%20Automation%20(Days%2051-60)/Project%20056%20-%20File%20Organizer%20Agent%20(Desktop%20AI)/README.md) | 06 - AI Agents + Automation (Days 51-60) | agent |
| 57 | [Browser Agent with Memory](06%20-%20AI%20Agents%20+%20Automation%20(Days%2051-60)/Project%20057%20-%20Browser%20Agent%20with%20Memory/README.md) | 06 - AI Agents + Automation (Days 51-60) | agent |
| 58 | [API Router with LLM](06%20-%20AI%20Agents%20+%20Automation%20(Days%2051-60)/Project%20058%20-%20API%20Router%20with%20LLM/README.md) | 06 - AI Agents + Automation (Days 51-60) | agent |
| 59 | [Recursive Research Agent](06%20-%20AI%20Agents%20+%20Automation%20(Days%2051-60)/Project%20059%20-%20Recursive%20Research%20Agent/README.md) | 06 - AI Agents + Automation (Days 51-60) | agent |
| 60 | [Cooking Assistant (Voice + Tools)](06%20-%20AI%20Agents%20+%20Automation%20(Days%2051-60)/Project%20060%20-%20Cooking%20Assistant%20(Voice%20+%20Tools)/README.md) | 06 - AI Agents + Automation (Days 51-60) | agent |
| 61 | [Speech-to-Text Converter](07%20-%20Speech%20and%20Audio%20(Days%2061-70)/Project%20061%20-%20Speech-to-Text%20Converter/README.md) | 07 - Speech and Audio (Days 61-70) | nlp |
| 62 | [Text-to-Speech with ElevenLabs or Coqui](07%20-%20Speech%20and%20Audio%20(Days%2061-70)/Project%20062%20-%20Text-to-Speech%20with%20ElevenLabs%20or%20Coqui/README.md) | 07 - Speech and Audio (Days 61-70) | nlp |
| 63 | [Language Identification from Audio](07%20-%20Speech%20and%20Audio%20(Days%2061-70)/Project%20063%20-%20Language%20Identification%20from%20Audio/README.md) | 07 - Speech and Audio (Days 61-70) | audio |
| 64 | [Sound Classification (UrbanSound8K)](07%20-%20Speech%20and%20Audio%20(Days%2061-70)/Project%20064%20-%20Sound%20Classification%20(UrbanSound8K)/README.md) | 07 - Speech and Audio (Days 61-70) | audio |
| 65 | [Voice Cloning Mini Project](07%20-%20Speech%20and%20Audio%20(Days%2061-70)/Project%20065%20-%20Voice%20Cloning%20Mini%20Project/README.md) | 07 - Speech and Audio (Days 61-70) | audio |
| 66 | [Real-Time Audio Transcriber](07%20-%20Speech%20and%20Audio%20(Days%2061-70)/Project%20066%20-%20Real-Time%20Audio%20Transcriber/README.md) | 07 - Speech and Audio (Days 61-70) | audio |
| 67 | [Voice Emotion Classifier](07%20-%20Speech%20and%20Audio%20(Days%2061-70)/Project%20067%20-%20Voice%20Emotion%20Classifier/README.md) | 07 - Speech and Audio (Days 61-70) | audio |
| 68 | [Audio Keyword Spotting](07%20-%20Speech%20and%20Audio%20(Days%2061-70)/Project%20068%20-%20Audio%20Keyword%20Spotting/README.md) | 07 - Speech and Audio (Days 61-70) | audio |
| 69 | [Whisper + RAG Agent](07%20-%20Speech%20and%20Audio%20(Days%2061-70)/Project%20069%20-%20Whisper%20+%20RAG%20Agent/README.md) | 07 - Speech and Audio (Days 61-70) | agent |
| 70 | [AI Podcast Summarizer](07%20-%20Speech%20and%20Audio%20(Days%2061-70)/Project%20070%20-%20AI%20Podcast%20Summarizer/README.md) | 07 - Speech and Audio (Days 61-70) | audio |
| 71 | [Medical Diagnosis Support Tool](08%20-%20Healthcare%20+%20Finance%20+%20Retail%20(Days%2071-80)/Project%20071%20-%20Medical%20Diagnosis%20Support%20Tool/README.md) | 08 - Healthcare + Finance + Retail (Days 71-80) | classification |
| 72 | [Insurance Claim Classifier](08%20-%20Healthcare%20+%20Finance%20+%20Retail%20(Days%2071-80)/Project%20072%20-%20Insurance%20Claim%20Classifier/README.md) | 08 - Healthcare + Finance + Retail (Days 71-80) | classification |
| 73 | [Drug Similarity Finder](08%20-%20Healthcare%20+%20Finance%20+%20Retail%20(Days%2071-80)/Project%20073%20-%20Drug%20Similarity%20Finder/README.md) | 08 - Healthcare + Finance + Retail (Days 71-80) | classification |
| 74 | [Financial Forecasting Agent](08%20-%20Healthcare%20+%20Finance%20+%20Retail%20(Days%2071-80)/Project%20074%20-%20Financial%20Forecasting%20Agent/README.md) | 08 - Healthcare + Finance + Retail (Days 71-80) | agent |
| 75 | [AI Loan Eligibility Checker](08%20-%20Healthcare%20+%20Finance%20+%20Retail%20(Days%2071-80)/Project%20075%20-%20AI%20Loan%20Eligibility%20Checker/README.md) | 08 - Healthcare + Finance + Retail (Days 71-80) | classification |
| 76 | [Retail Sales Predictor](08%20-%20Healthcare%20+%20Finance%20+%20Retail%20(Days%2071-80)/Project%20076%20-%20Retail%20Sales%20Predictor/README.md) | 08 - Healthcare + Finance + Retail (Days 71-80) | regression |
| 77 | [Customer Churn Predictor](08%20-%20Healthcare%20+%20Finance%20+%20Retail%20(Days%2071-80)/Project%20077%20-%20Customer%20Churn%20Predictor/README.md) | 08 - Healthcare + Finance + Retail (Days 71-80) | classification |
| 78 | [Visual Price Tag Detection for Retail](08%20-%20Healthcare%20+%20Finance%20+%20Retail%20(Days%2071-80)/Project%20078%20-%20Visual%20Price%20Tag%20Detection%20for%20Retail/README.md) | 08 - Healthcare + Finance + Retail (Days 71-80) | vision |
| 79 | [Product Review Analyzer](08%20-%20Healthcare%20+%20Finance%20+%20Retail%20(Days%2071-80)/Project%20079%20-%20Product%20Review%20Analyzer/README.md) | 08 - Healthcare + Finance + Retail (Days 71-80) | nlp |
| 80 | [Doctor-Patient Conversational AI](08%20-%20Healthcare%20+%20Finance%20+%20Retail%20(Days%2071-80)/Project%20080%20-%20Doctor-Patient%20Conversational%20AI/README.md) | 08 - Healthcare + Finance + Retail (Days 71-80) | classification |
| 81 | [Deploy LLM on Streamlit + Ollama](09%20-%20Web%20+%20Deployment%20(Days%2081-90)/Project%20081%20-%20Deploy%20LLM%20on%20Streamlit%20+%20Ollama/README.md) | 09 - Web + Deployment (Days 81-90) | web |
| 82 | [Gradio App - Text Classifier](09%20-%20Web%20+%20Deployment%20(Days%2081-90)/Project%20082%20-%20Gradio%20App%20-%20Text%20Classifier/README.md) | 09 - Web + Deployment (Days 81-90) | nlp |
| 83 | [FastAPI for Model Inference](09%20-%20Web%20+%20Deployment%20(Days%2081-90)/Project%20083%20-%20FastAPI%20for%20Model%20Inference/README.md) | 09 - Web + Deployment (Days 81-90) | web |
| 84 | [Create a Hugging Face Space](09%20-%20Web%20+%20Deployment%20(Days%2081-90)/Project%20084%20-%20Create%20a%20Hugging%20Face%20Space/README.md) | 09 - Web + Deployment (Days 81-90) | vision |
| 85 | [Build and Query Your Own Vector DB](09%20-%20Web%20+%20Deployment%20(Days%2081-90)/Project%20085%20-%20Build%20and%20Query%20Your%20Own%20Vector%20DB/README.md) | 09 - Web + Deployment (Days 81-90) | web |
| 86 | [Voice-Enabled AI Web Assistant](09%20-%20Web%20+%20Deployment%20(Days%2081-90)/Project%20086%20-%20Voice-Enabled%20AI%20Web%20Assistant/README.md) | 09 - Web + Deployment (Days 81-90) | audio |
| 87 | [Dockerize Your AI App](09%20-%20Web%20+%20Deployment%20(Days%2081-90)/Project%20087%20-%20Dockerize%20Your%20AI%20App/README.md) | 09 - Web + Deployment (Days 81-90) | web |
| 88 | [Build Local Document Q&A App](09%20-%20Web%20+%20Deployment%20(Days%2081-90)/Project%20088%20-%20Build%20Local%20Document%20Q&A%20App/README.md) | 09 - Web + Deployment (Days 81-90) | web |
| 89 | [Create an AI CLI Tool](09%20-%20Web%20+%20Deployment%20(Days%2081-90)/Project%20089%20-%20Create%20an%20AI%20CLI%20Tool/README.md) | 09 - Web + Deployment (Days 81-90) | web |
| 90 | [AI-Powered Resume Screener Web App](09%20-%20Web%20+%20Deployment%20(Days%2081-90)/Project%20090%20-%20AI-Powered%20Resume%20Screener%20Web%20App/README.md) | 09 - Web + Deployment (Days 81-90) | nlp |
| 91 | [Build a Local AGI Agent with Memory + Tools](10%20-%20Advanced,%20Experimental,%20and%20Ethics%20(Days%2091-100)/Project%20091%20-%20Build%20a%20Local%20AGI%20Agent%20with%20Memory%20+%20Tools/README.md) | 10 - Advanced, Experimental, and Ethics (Days 91-100) | agent |
| 92 | [Quantum Circuit Classifier with PennyLane](10%20-%20Advanced,%20Experimental,%20and%20Ethics%20(Days%2091-100)/Project%20092%20-%20Quantum%20Circuit%20Classifier%20with%20PennyLane/README.md) | 10 - Advanced, Experimental, and Ethics (Days 91-100) | agent |
| 93 | [Ethics-Aware AI Chatbot (Rule-Constrained)](10%20-%20Advanced,%20Experimental,%20and%20Ethics%20(Days%2091-100)/Project%20093%20-%20Ethics-Aware%20AI%20Chatbot%20(Rule-Constrained)/README.md) | 10 - Advanced, Experimental, and Ethics (Days 91-100) | agent |
| 94 | [Red Team Your LLM with Adversarial Inputs](10%20-%20Advanced,%20Experimental,%20and%20Ethics%20(Days%2091-100)/Project%20094%20-%20Red%20Team%20Your%20LLM%20with%20Adversarial%20Inputs/README.md) | 10 - Advanced, Experimental, and Ethics (Days 91-100) | agent |
| 95 | [Model Cards + Datasheets Generator](10%20-%20Advanced,%20Experimental,%20and%20Ethics%20(Days%2091-100)/Project%20095%20-%20Model%20Cards%20+%20Datasheets%20Generator/README.md) | 10 - Advanced, Experimental, and Ethics (Days 91-100) | agent |
| 96 | [BCI Signal Classifier (OpenBCI Data)](10%20-%20Advanced,%20Experimental,%20and%20Ethics%20(Days%2091-100)/Project%20096%20-%20BCI%20Signal%20Classifier%20(OpenBCI%20Data)/README.md) | 10 - Advanced, Experimental, and Ethics (Days 91-100) | agent |
| 97 | [Simulated Society of AI Agents (LangGraph)](10%20-%20Advanced,%20Experimental,%20and%20Ethics%20(Days%2091-100)/Project%20097%20-%20Simulated%20Society%20of%20AI%20Agents%20(LangGraph)/README.md) | 10 - Advanced, Experimental, and Ethics (Days 91-100) | agent |
| 98 | [AGI Alignment Simulator (Multi-Agent Goal Drift)](10%20-%20Advanced,%20Experimental,%20and%20Ethics%20(Days%2091-100)/Project%20098%20-%20AGI%20Alignment%20Simulator%20(Multi-Agent%20Goal%20Drift)/README.md) | 10 - Advanced, Experimental, and Ethics (Days 91-100) | agent |
| 99 | [Build Your Own LLM Evaluation Suite](10%20-%20Advanced,%20Experimental,%20and%20Ethics%20(Days%2091-100)/Project%20099%20-%20Build%20Your%20Own%20LLM%20Evaluation%20Suite/README.md) | 10 - Advanced, Experimental, and Ethics (Days 91-100) | agent |
| 100 | [Design a Personal AI Manifesto (Reflection Project)](10%20-%20Advanced,%20Experimental,%20and%20Ethics%20(Days%2091-100)/Project%20100%20-%20Design%20a%20Personal%20AI%20Manifesto%20(Reflection%20Project)/README.md) | 10 - Advanced, Experimental, and Ethics (Days 91-100) | ethics |
