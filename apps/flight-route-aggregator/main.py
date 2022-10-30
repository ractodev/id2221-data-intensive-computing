import sys
import os
from geopy.geocoders import Nominatim
from pyspark.conf import SparkConf
from pyspark.sql import SparkSession, Catalog
from pyspark.sql import DataFrame, DataFrameStatFunctions, DataFrameNaFunctions
from pyspark.sql import functions as F
from pyspark.sql import types as T
from pyspark.sql.types import Row
from operator import add

spark_conf = SparkConf()
spark_conf.setAll([
    ('spark.master', 'spark://spark-master:7077'),
    ('spark.app.name', 'TestApp'),
    # ('spark.submit.deployMode', 'client'),
    # ('spark.ui.showConsoleProgress', 'true'),
    # ('spark.eventLog.enabled', 'false'),
    # ('spark.logConf', 'false'),
    # ('spark.driver.bindAddress', 'vps00'),
    # ('spark.driver.host', 'localhost'),
])

spark = SparkSession.builder.config(conf=spark_conf).getOrCreate()
sc = spark.sparkContext

# Reverse geolocator function (input: (lat, lon) | output: country name)    
def locator(lat, lon):
    try:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.reverse(lat + "," + lon)
        country = location.raw['address'].get('country', '')
        return country
    except:
        return "International Waters"

data = sc.parallelize(list("Hello World"))
counts = data.map(lambda x:
                  (x, 1)).reduceByKey(add).sortBy(lambda x: x[1],
                                                  ascending=False).collect()

for (word, count) in counts:
    print("{}: {}".format(word, count))

spark.stop()
quit()
