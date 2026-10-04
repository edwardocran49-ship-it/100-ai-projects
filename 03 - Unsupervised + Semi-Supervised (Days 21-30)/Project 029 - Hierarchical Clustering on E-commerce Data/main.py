import pandas as pd
from scipy.cluster.hierarchy import fcluster,linkage
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from download_data import ensure_dataset
PROJECT_TITLE="Hierarchical Clustering on E-commerce Data"
def run_demo():
    df=pd.read_csv(ensure_dataset(),encoding="latin-1").dropna(subset=["CustomerID"]); df=df[(df.Quantity>0)&(df.UnitPrice>0)]; df["sales"]=df.Quantity*df.UnitPrice; df["InvoiceDate"]=pd.to_datetime(df.InvoiceDate)
    customers=df.groupby("CustomerID").agg(total_spent=("sales","sum"),purchase_frequency=("InvoiceNo","nunique"),avg_cart_value=("sales","mean"),last_purchase=("InvoiceDate","max")); customers["recency_days"]=(df.InvoiceDate.max()-customers.pop("last_purchase")).dt.days; customers=customers.sort_values("total_spent",ascending=False).head(2000)
    X=StandardScaler().fit_transform(customers); Z=linkage(X,method="ward"); labels=fcluster(Z,t=5,criterion="maxclust")
    return {"project":29,"title":PROJECT_TITLE,"author":"Edward Ocran","status":"ok","dataset":"UCI Online Retail transactions","records":len(customers),"clusters":5,"metrics":{"silhouette":round(float(silhouette_score(X,labels)),4)}}

def main():
    import argparse, json
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args()
    result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
