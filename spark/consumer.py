from pyspark.sql import SparkSession
from pyspark.sql.types import TimestampType, StructType, StructField, IntegerType, FloatType, StringType
from pyspark.sql.functions import from_json, col, udf, year, month, dayofmonth, date_format

def save_to_mysql(df, batch_id):
    
    df.write.format("jdbc") \
        .option("url", f"jdbc:mysql://Manager_Host:3306/manager_sales_db") \
        .option("driver", "com.mysql.jdbc.Driver") \
        .option("dbtable", "manager_sales") \
        .option("user", "root") \
        .option("password", "secret") \
        .mode("append") \
        .save()
  
    print(batch_id, "saved to MySQL")

salesSchema = [
    StructField("pos_id", IntegerType()),
    StructField("pos_name", StringType()),
    StructField("article", StringType()),
    StructField("quantity", FloatType()),
    StructField("unit_price", FloatType()),
    StructField("total", FloatType()),
    StructField("sale_type", StringType()),
    StructField("payment_mode", StringType()),
    StructField("latitude", StringType()),
    StructField("longitude", StringType()),
    StructField("sale_time", TimestampType())
]

schema = StructType([
    StructField("payload", StructType([
        StructField("before", StructType(salesSchema)),
        StructField("after", StructType(salesSchema)),
        StructField("ts_ms", StringType()),
        StructField("op", StringType())
    ]))
])

spark = SparkSession \
    .builder \
    .appName("Spark Kafka Streaming Data Pipeline") \
    .master("local[*]") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

input_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "JendoubaSales.jendouba_sales_db.jendouba_sales,BejaSales.beja_sales_db.beja_sales,KefSales.kef_sales_db.kef_sales") \
    .option("startingOffsets", "earliest") \
    .load() 

expanded_df = input_df \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select(col("data.payload.after.*")) \
    .withColumn("sale_year", year("sale_time")) \
    .withColumn("sale_month", month("sale_time")) \
    .withColumn("day_of_month", dayofmonth("sale_time")) \
    .withColumn("sale_week_number", ((col("day_of_month") - 1) / 7 + 1).cast("int")) \
    .withColumn("sale_day_of_week", date_format(col("sale_time"), "EEEE")) \
    .drop("day_of_month")  

query = expanded_df \
    .writeStream \
    .trigger(processingTime="1 seconds") \
    .foreachBatch(save_to_mysql) \
    .outputMode("update") \
    .start()

query.awaitTermination()
