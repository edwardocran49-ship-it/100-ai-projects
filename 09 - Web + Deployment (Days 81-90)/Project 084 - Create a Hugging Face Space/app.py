import gradio as gr
from portfolio_core.deployment import sentiment
gr.Interface(sentiment,"text","json",title="Text Classifier").launch()
