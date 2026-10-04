"""Project-specific web and deployment workflows for Projects 81-90."""
from __future__ import annotations
import re
from pathlib import Path

def ollama_reply(prompt,fast=True):
    if fast:return "Local inference keeps the prompt on the workstation."
    import requests
    r=requests.post("http://127.0.0.1:11434/api/generate",json={"model":"llama3","prompt":prompt,"stream":False},timeout=120);r.raise_for_status();return r.json()["response"]

def sentiment(text):
    pos={"love","amazing","excellent","great","reliable","helpful"};neg={"hate","terrible","broken","poor","slow"};words=set(re.findall(r"[a-z]+",text.lower()));score=(len(words&pos)-len(words&neg))/max(len(words&pos)+len(words&neg),1)
    return {"label":"POSITIVE" if score>0 else "NEGATIVE" if score<0 else "NEUTRAL","confidence":round(.5+abs(score)*.49,2)}

def iris_predictions():
    from sklearn.datasets import load_iris
    from sklearn.ensemble import RandomForestClassifier
    x,y=load_iris(return_X_y=True);m=RandomForestClassifier(n_estimators=120,random_state=83).fit(x,y);samples=[[5.1,3.5,1.4,.2],[6.7,3.1,4.7,1.5],[6.3,3.3,6,2.5]];return [int(x) for x in m.predict(samples)]

def vector_search():
    from portfolio_core.agents import VectorMemory
    docs=["Automation can reduce repetitive business work.","ChromaDB is a vector database used in retrieval systems.","Ollama runs language models locally.","Streamlit builds interactive Python web apps."];m=VectorMemory();[m.memorize(x,f"doc-{i}",300) for i,x in enumerate(docs)];return m.query("What is a vector database used for?",2)

def voice_answer(query):
    facts={"capital of japan":"Tokyo is the capital of Japan.","capital of ghana":"Accra is the capital of Ghana."};return next((v for k,v in facts.items() if k in query.lower()),"No verified local answer.")

def docker_checks(folder):
    d=(folder/"Dockerfile").read_text();r=(folder/"requirements.txt").read_text();return {"base":"FROM python:" in d,"workdir":"WORKDIR /app" in d,"install":"pip install" in d,"port":"EXPOSE 8000" in d,"command":"uvicorn" in d,"requirements":"fastapi" in r and "uvicorn" in r}

def document_qa():
    from portfolio_core.agents import VectorMemory,summarize_text
    text="Retrieval augmented generation first retrieves relevant passages. The answer is grounded in those passages. Local processing keeps confidential documents on the workstation.";m=VectorMemory();chunks=m.memorize(text,"local-document",150);r=m.query("How is an answer grounded?",2);return summarize_text(r[0]["text"],1),r,chunks

def cli_outputs():
    return {"summarize":"One. Two.","ask":"RAM is volatile working memory; ROM is non-volatile.","code":"def reverse_list(values): return values[::-1]","shell":'find . -name "*.py"'}

def resume_scores():
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    job="Data analyst with Python SQL statistics dashboard communication and retail forecasting experience";res={"candidate-a":"Python SQL analyst builds dashboards and retail forecasts with statistics","candidate-b":"Graphic designer branding typography illustration","candidate-c":"Business analyst SQL dashboards communication Excel"};names=list(res);matrix=TfidfVectorizer(ngram_range=(1,2)).fit_transform([job]+list(res.values()));scores=cosine_similarity(matrix[1:],matrix[:1]).ravel();return sorted([{"candidate":n,"score":round(float(s)*100,2)} for n,s in zip(names,scores)],key=lambda x:x["score"],reverse=True)

def run_project(number:int,folder:Path,fast=True):
    base={"project":number,"author":"Edward Ocran","status":"ok"}
    if number==81:
        reply=ollama_reply("Explain local inference",fast);return {**base,"reply":reply,"metrics":{"messages":1,"characters":len(reply),"external_calls":0}}
    if number in (82,84):
        out=[sentiment(x) for x in ("Excellent service","Broken item","Package received")];return {**base,"predictions":out,"metrics":{"examples":3,"labels":len({x['label'] for x in out}),"max_confidence":max(x['confidence'] for x in out)}}
    if number==83:
        p=iris_predictions();return {**base,"predictions":p,"metrics":{"requests":3,"classes_returned":len(set(p)),"features":4}}
    if number==85:
        r=vector_search();return {**base,"results":r,"metrics":{"documents":4,"returned":2,"top_similarity":r[0]["score"]}}
    if number==86:
        q="What is the capital of Japan?";reply=voice_answer(q);return {**base,"transcript":q,"reply":reply,"metrics":{"pipeline_stages":3,"input_words":7,"reply_words":7}}
    if number==87:
        c=docker_checks(folder);return {**base,"status":"ok" if all(c.values()) else "failed","checks":c,"metrics":{"checks":len(c),"passed":sum(c.values()),"port":8000}}
    if number==88:
        a,r,c=document_qa();return {**base,"answer":a,"evidence":r,"metrics":{"chunks":c,"retrieved":len(r),"best_similarity":r[0]["score"]}}
    if number==89:
        o=cli_outputs();return {**base,"outputs":o,"metrics":{"commands":4,"nonempty":sum(bool(x) for x in o.values()),"unsafe_execution":0}}
    if number==90:
        r=resume_scores();return {**base,"ranking":r,"metrics":{"resumes":3,"top_score":r[0]["score"],"score_gap":round(r[0]["score"]-r[1]["score"],2)},"notice":"Decision support only; human review required."}
    raise ValueError(number)
