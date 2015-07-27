import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import java.lang.Double.isNaN

object linkage {
    def isHeader(line: String): Boolean = {
        line.contains("id_1")
    }

    def toDouble(s: String): Double = {
        if ("?".equals(s)) Double.NaN else s.toDouble
    }

    case class MatchData(id1: Int, id2: Int, scores: Array[Double], matched: Boolean)

    def parse(line: String): MatchData = {
        val pieces = line.split(',')
        val id1 = pieces(0).toInt
        val id2 = pieces(1).toInt
        val scores = pieces.slice(2, 11).map(toDouble)
        val matched = pieces(11).toBoolean
        // (id1, id2, scores, matched)
        MatchData(id1, id2, scores, matched)
    }

    def main(args: Array[String]){
        val rawblocks = sc.textFile("linkage/block_1.csv")

        // play with head
        val head = rawblocks.take(10)
        println("head's length " + head.length)
        println("head ")
        head.foreach(println)
        println("filter use isHeader")
        head.filter(isHeader).foreach(println)
        println("filterNot use isHeader")
        head.filterNot(isHeader).foreach(println)
        println("head's length isHeader")
        println(head.filter(isHeader).length)
        println(head.filter(!isHeader(_)).length)

        // play with noheader
        val noheader = rawblocks.filter(!isHeader(_))
        println("noheader.first")
        println(noheader.first)
        val line = head(5)
        val pieces = line.split(',')
        println(pieces)
        val md = parse(line)
        println("use MatchData")
        println(md.matched)
        println(md.id1)
        println(md.id2)
        val mds = head.filter(!isHeader(_)).map(parse)
        val parsed = noheader.map(parse)
        parsed.cache()
        val grouped = mds.groupBy(_.matched)
        grouped.mapValues(_.size).foreach(println)
        val matchCounts = parsed.map(_.matched).countByValue()
        val matchCountsSeq = matchCounts.toSeq
        matchCountsSeq.sortBy(_._1).foreach(println)
        matchCountsSeq.sortBy(_._2).foreach(println)
        matchCountsSeq.sortBy(_._2).reverse.foreach(println)
        println(parsed.map(_.scores(0)).stats())
        println(parsed.map(_.scores(0)).filter(!isNaN(_)).stats())

        val stats = (0 until 9).map(i => {
            parsed.map(_.scores(i)).filter(!isNaN(_)).stats()
        })
        stats(1)
        stats(2)
        spark.stop()
        System.exit(0)
    }
}