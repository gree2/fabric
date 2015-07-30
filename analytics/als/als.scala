import org.apache.spark.mllib.recommendation._

val rawUserArtistData = sc.textFile("hdfs://localhost:9000/user/hqlgree2/asl/user_artist_data.txt")
rawUserArtistData.map(_.split(' ')(0).toDouble).stats()
rawUserArtistData.map(_.split(' ')(1).toDouble).stats()

val rawArtistData = sc.textFile("hdfs://localhost:9000/user/hqlgree2/asl/artist_data.txt")
// span() splits the line by its first tab
// and retains the rest as the artist name
// with whitespace and the tab removed
val artistById = rawArtistData.map { line =>
	val (id, name) = line.span(_ != '\t')
	(id.toInt, name.trim)
}

val artistById = rawArtistData.flatMap { line =>
	val (id, name) = line.span(_ != '\t')
	if (name.isEmpty) {
		None
	} else {
		try {
			Some((id.toInt, name.trim))
		} catch {
			case e: NumberFormatException => None
		}
	}
}

val rawArtistAlias = sc.textFile("hdfs://localhost:9000/user/hqlgree2/artist_alias.txt")
val artistAlias = rawArtistAlias.flatMap { line =>
	val tokens = line.split('\t')
	if (tokens(0).isEmpty) {
		None
	} else {
		Some((tokens(0).toInt, tokens(1).toInt))
	}
}.collectAsMap()

// artistById.lookup(6803336).head
// artistById.lookup(1000010).head

val bArtistAlias = sc.broadcast(artistAlias)

val trainData = rawArtistData.map { line =>
	val Array(userId, artistId, count) = line.split(' ').map(_.toInt)
	// get artist's alias if it exist, else get original artist
	val finalArtistId = bArtistAlias.value.getOrElse(artistId, artistId)
	Rating(userId, finalArtistId, count)
// als algorithm is iterative
// typically need to access 10 times or more
}.cache()

// finally we can build a model
val model = ALS.trainImplicit(trainData, 10, 5, 0.01, 1.0)
// feature vectors
model.userFeatures.mapValues(_.mkString(", ")).first()

// ----------------------------------------------
// spot checking recommendations
val rawArtistForUser = rawUserArtistData.map(_.split(' ')).
	// 1. find lines whose user is 2093760
	filter { case Array(user, _, _) => user.toInt == 2093760 }

val existingProducts = rawArtistForUser.
	map { case Array(_, artist, _) => artist.toInt }.
	// 2. collect unique artists
	collect().toSet

artistById.filter { case (id, name) =>
	existingProducts.contains(id)
// 3. filter in those artists, get just artist, and print
}.values.collect().foreach(println)

// make five recommendations for this user
val recommendations = model.recommendations(2093760, 5)
recommendations.foreach(println)
// e.g. Rating(2093760, 4605, 0.027118271894797333)
// userId, artistId, numeric value between 0 and 1
// higher values mean a better recommendation

val recommendedProductIds = recommendations.map(_.product).toSet

artistById.filter { case (id, name) =>
	recommendedProductIds.contains(id)
}.values.collect().foreach(println)

// ----------------------------------------------
// evaluating recommendation quality
// receiver operating characteristic (roc) curve
// area under the curve (auc)
// mean auc
// mean average percision (map)
// cross-validation (cv)

// ----------------------------------------------
// computing auc

import org.apache.spark.rdd._

def areaUnderCurve(
	positiveData: RDD[Rating],
	bAllItemIds: Broadcast[Array[Int]],
	predictFunction: (RDD[(Int, Int)] => RDD[Rating])) = {

}

// this function is defined in accompanying source code
val allData = buildRatings(rawUserArtistData, bArtistAlias)
val Array(trainData, cvData) = allData.randomSplit(Array(0.9, 0.1))
trainData.cache()
cvData.cache()

// remove duplicates and collect to driver
val allItemIds = allData.map(_.product).distinct().collect()
val bAllItemIds = sc.broadcast(allItemIds)

val model = ALS.trainImplicit(trainData, 10, 5, 0.01, 1.0)
val auc = areaUnderCurve(cvData, bAllItemIds, model.predict)

def predictMostListened(
	sc: SparkContext,
	train: RDD[Rating])(allData: RDD[(Int, Int)]) = {

	val bListenCount = sc.broadcast(
		train.map(r => (r.product, r.rating)).
			reduceByKey(_ + _).collectAsMap()
	)

	allData.map{ case (user, product) =>
		Rating(
			user,
			product,
			bListenCount.value.getOrElse(product, 0.0)
		)
	}
}

val auc = areaUnderCurve(
	cvData, bAllItemIds, predictMostListened(sc, trainData)
)

// hyperparameter selection
val evaluations =
	// read as a triply nested for loop
	for (rank <- Array(10, 50);
		lambda <- Array(1.0, 0.0001);
		alpha <- Array(1.0, 40.0))
		yield {
			val model = ALS.trainImplicit(trainData, rank, 10, lambda, alpha)
			val auc = areaUnderCurve(cvData, bAllItemIds, model.predict)
			((rank, lambda, alpha), auc)
		}

// sort by second value (auc), descending
evaluations.sortBy(_._2).reverse.foreach(println)

// copy 100 (distinct) users to the driver
val someUsers = allData.map(_.user).distinct().take(100)
// map() is a local scala operation here
val someRecommendations = someUsers.map(userId => model.recommendProducts(userId, 5))
someRecommendations.map(
	// mkString joins a collection to a string with a delimiter
	recs => recs.head.user + " -> " + recs.map(_.product).mkString(", ")
).foreach(println)
