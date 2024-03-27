from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

# Load the MNIST dataset
mnist_data = spark.read.format("libsvm").load("path/to/mnist_dataset.txt")

# Split the data into features and labels
features_col = [col for col in mnist_data.columns if col != "label"]
assembler = VectorAssembler(inputCols=features_col, outputCol="features")
mnist_data = assembler.transform(mnist_data)

# Split the data into training and testing sets
(train_data, test_data) = mnist_data.randomSplit([0.8, 0.2], seed=42)

# Train a Logistic Regression model
lr = LogisticRegression(maxIter=10, regParam=0.3, elasticNetParam=0.8)
lr_model = lr.fit(train_data)

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