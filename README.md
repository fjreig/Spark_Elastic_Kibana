## Docker Stacks


```
docker build -t cluster-apache-spark:3.2.1 .
```

```
docker compose up -d
```

### Cargar ficheros en elastic

```
docker exec -it spark-master python3 /opt/spark-apps/SubirFicheros.py
```

### Consulta de spark

```
docker exec -it spark-master python3 /opt/spark-apps/Query.py

docker exec -it spark-master python3 /opt/spark-apps/Query2.py
```
