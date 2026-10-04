from pathlib import Path
import io,requests,zipfile,pandas as pd
URL="https://archive.ics.uci.edu/static/public/352/online+retail.zip"
out=Path(__file__).parent/"data";out.mkdir(exist_ok=True)
z=zipfile.ZipFile(io.BytesIO(requests.get(URL,timeout=180).content));name=next(x for x in z.namelist() if x.endswith('.xlsx'))
with z.open(name) as f:d=pd.read_excel(f)
d[("day")]=d.InvoiceDate.dt.normalize()
d=d[(d.Quantity>0)&d.StockCode.notna()&d.InvoiceDate.notna()];top=d.groupby('StockCode').day.nunique().idxmax();daily=d[d.StockCode==top].set_index('InvoiceDate').Quantity.resample('D').sum().rename('units_sold').reset_index().rename(columns={'InvoiceDate':'date'});daily.to_csv(out/'daily_sales.csv',index=False)
print('product',top,'days',len(daily))
