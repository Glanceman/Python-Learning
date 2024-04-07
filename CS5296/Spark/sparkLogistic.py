from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
# Create a SparkSession
spark = SparkSession.builder.getOrCreate()
# # Load the MNIST dataset
# # train_data = spark.read.csv("s3://mlspark/data/mnist_train.csv", header=True,inferSchema = True)
# # test_data = spark.read.csv("s3://mlspark/data/mnist_test.csv", header=True,inferSchema = True)
S3="s3://mlspark/"
LOCAL="E:/Python/CS5296/Spark/"
BASE_URL=S3
train_data = spark.read.csv(BASE_URL+"data/mnist_train.csv", header=True,inferSchema = True)
test_data = spark.read.csv(BASE_URL+"data/mnist_test.csv", header=True,inferSchema = True)


assembler = VectorAssembler(inputCols=train_data.columns[1:], outputCol="features")
train_data  = assembler.transform(train_data).select("label", "features").toDF("label", "features").cache()
assembler = VectorAssembler(inputCols=test_data.columns[1:], outputCol="features")
test_data  = assembler.transform(test_data).select("label", "features").toDF("label", "features").cache()

print("Here")

train_data.show()
# Train a Logistic Regression model
lr = LogisticRegression(featuresCol="features",labelCol="label",maxIter=1000, regParam=0.1, elasticNetParam=0.1)
lr_model=lr.fit(train_data)

# Make predictions on the test data
predictions = lr_model.transform(test_data)

# Evaluate the model's performance
evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print(f"Accuracy = {accuracy}")

# Other evaluation metrics
evaluator = MulticlassClassificationEvaluator(metricName="precisionByLabel")
precision = evaluator.evaluate(predictions)
print(f"Precision = {precision}")

evaluator = MulticlassClassificationEvaluator(metricName="recallByLabel")
recall = evaluator.evaluate(predictions)
print(f"Recall = {recall}")

evaluator = MulticlassClassificationEvaluator(metricName="f1")
f1_score = evaluator.evaluate(predictions)
print(f"F1 Score = {f1_score}")


# with open(BASE_URL+"evaluation.txt", "w") as f:
#     f.write(f"Accuracy: {accuracy}\n")
#     f.write(f"Recall: {recall}\n")
#     f.write(f"Precision: {precision}\n")
#     f.write(f"F1 Score: {f1_score}\n")


spark.stop()