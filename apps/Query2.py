import os
import pyspark
import json
from pyspark.sql import SparkSession, SQLContext, Row

print("Load Apache Cassandra Source Connector...")
os.environ['PYSPARK_SUBMIT_ARGS'] = '--jars /opt/spark-apps/elasticsearch-hadoop-8.8.1/dist/elasticsearch-spark-20_2.11-8.8.1.jar pyspark-shell'  
conf = pyspark.SparkConf()

print("Set config Cassandra-Spark...")
conf.setMaster("spark://spark-master:7077")
conf.setAppName("Consulta")
conf.set("spark.driver.bindAddress", "0.0.0.0")
conf.set("spark.cores.max", "7")
conf.set("spark.executor.memory", "3g")
conf.set("spark.blockManager.port", "7004")

sc = pyspark.SparkContext(conf=conf)
es_conf = {"es.nodes": "elasticsearch", "es.port": "9200", "es.resource": "alumbrado"}
alumbrado_rdd = sc.newAPIHadoopRDD("org.elasticsearch.hadoop.mr.EsInputFormat","org.apache.hadoop.io.NullWritable", "org.elasticsearch.hadoop.mr.LinkedMapWritable", conf=es_conf)
spark = SparkSession.builder.appName("Spark SQL").getOrCreate()

alumbrado_rdd = alumbrado_rdd.map(lambda x: x[1])
df = alumbrado_rdd.map(lambda l: Row(**dict(l))).toDF()

df.createOrReplaceTempView("consulta1")

print("Query...")

spark.sql("""SELECT date(Fecha_Dia) as Fecha, CM, 
    round(max(EA)-min(EA),1) as EA, max(PA)/1000 as max_PA
    FROM consulta1 
    group by date(Fecha_Dia), CM""").show()

spark.stop()