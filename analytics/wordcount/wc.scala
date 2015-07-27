// spark-shell -i wc.scala
val text = sc.textFile("hdfs://localhost:9000/user/hqlgree2/linkage/block_1.csv")
val counts = text.flatMap(line => line.split(",")).map(word => (word, 1)).reduceByKey(_+_)
counts.collect
System.exit(0)
