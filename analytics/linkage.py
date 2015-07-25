from pyspark import SparkContext


if __name__ == "__main__":
    sc = SparkContext(appName="linkage")
    lines = sc.textFile('hdfs://localhost:9000/user/hqlgree2/linkage')
    parts = lines.map(lambda l: l.split(','))
    grouped = parts.filter(lambda x: u"\"id_1\"" != x[0]) \
        .map(lambda x: (x[-1], 1)) \
        .reduce(lambda a, b: a + b) \
        .groupByKey()
    output = grouped.collect()
    for (key, count) in output:
        print key, count

    sc.stop()