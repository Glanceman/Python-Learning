from pyspark import SparkContext
import os
import sys

#args = sys.argv
#inp = args[1]
#out = args[2]
sc = SparkContext()
text_file = sc.textFile("s3://mlspark/data/file01.txt")
counts = text_file.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
counts.saveAsTextFile("s3://mlspark/result")
sc.stop()
