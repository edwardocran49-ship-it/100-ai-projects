from fastapi import FastAPI
from pydantic import BaseModel
from portfolio_core.deployment import iris_predictions
app=FastAPI(title="Iris Inference")
class IrisInput(BaseModel):
 sepal_length:float;sepal_width:float;petal_length:float;petal_width:float
@app.post("/predict")
def predict(x:IrisInput):return {"prediction":iris_predictions()[0]}
