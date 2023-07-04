import elasticsearch
import pandas as pd
from elasticsearch import Elasticsearch

print("Abriendo csv....")
df = pd.read_csv("/opt/spark-apps/Alumbrado.csv")
df = df.head(5500)
df = df.drop(['Unnamed: 0'], axis=1)
df2 = df.to_dict('records')

print("Creando conexion con elastic....")
client = Elasticsearch("http://10.5.0.3:9200")


print("Cargando datos en elastic...")
for i in range(len(df2)):
    client.index(index='alumbrado', document=df2[i])

print("Trabajo completado....")