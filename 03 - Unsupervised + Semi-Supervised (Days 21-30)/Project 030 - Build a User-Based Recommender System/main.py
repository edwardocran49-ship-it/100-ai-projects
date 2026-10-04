import numpy as np,pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.metrics.pairwise import cosine_similarity
from download_data import ensure_dataset
PROJECT_TITLE="Build a User-Based Recommender System"
def run_demo():
    ratings=pd.read_csv(ensure_dataset()); test=ratings.sort_values("timestamp").groupby("userId").tail(1); train=ratings.drop(test.index); matrix=train.pivot(index="userId",columns="movieId",values="rating").fillna(0); similarity=cosine_similarity(matrix); users=list(matrix.index); position={u:i for i,u in enumerate(users)}; predictions=[]; actual=[]
    global_mean=float(train.rating.mean())
    for row in test.itertuples():
        if row.movieId not in matrix.columns: pred=global_mean
        else:
            scores=similarity[position[row.userId]].copy(); scores[position[row.userId]]=0; item=matrix[row.movieId].to_numpy(); mask=item>0; pred=float(np.dot(scores[mask],item[mask])/scores[mask].sum()) if scores[mask].sum()>0 else global_mean
        predictions.append(np.clip(pred,0.5,5)); actual.append(row.rating)
    return {"project":30,"title":PROJECT_TITLE,"author":"Edward Ocran","status":"ok","dataset":"MovieLens latest-small ratings","records":len(ratings),"users":len(users),"metrics":{"leave_one_out_rmse":round(float(mean_squared_error(actual,predictions)**0.5),4)}}

def main():
    import argparse, json
    parser=argparse.ArgumentParser(description=PROJECT_TITLE); parser.add_argument("--json",action="store_true"); args=parser.parse_args()
    result=run_demo(); print(json.dumps(result,sort_keys=True) if args.json else json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__": main()
