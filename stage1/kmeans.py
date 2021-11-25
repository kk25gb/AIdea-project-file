from sklearn.cluster import KMeans
import json
import pandas as pd

with open('vectorize_data.json',encoding='utf8') as f:
    data = json.load(f)

df = pd.DataFrame({data})

print(df)
# kmeans = KMeans(n_clusters=3)
# kmeans.fit(df)