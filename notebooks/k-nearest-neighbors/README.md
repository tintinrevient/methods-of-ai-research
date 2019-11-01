## K-nearest Neighbors

### Vector

Represent instances using **feature vectors**, and types of features are as below:
* **Numerical** feature: e.g. number of likes, temperature.
* **Binary** feature: e.g. are A and B friends? Employed?
* **Categorical** feature: e.g. Country, Genre of a text.

Feature vectors are points in **vector space**, and each **dimension** represents a feature.

### Distance

**Distance** = **Similarity**, which can be measured in **vector space**.

**Length/Norm of a vector**
<p float="left">
	<img src="./pix/length-of-vector-2.png" width="400">
	<img src="./pix/length-of-vector-1.png" width="300">
</p>

**Euclidian/L2 distance**: Distance between endpoint of vectors.
<p float="left">
	<img src="./pix/euclidian-distance.png" width="400">
</p>

**Manhattan/L1 distance**: Distance between endpoint of vectors.
<p float="left">
	<img src="./pix/manhattan-distance.png" width="400">
</p>

Different distance measure -> Different neighborhoods
<p float="left">
	<img src="./pix/distance-comparison-1.png" width="400">
	<img src="./pix/distance-comparison-2.png" width="300">
</p>

**Minkowski distance**: Generalization of the Euclidian and Manhattan distance.
<p float="left">
	<img src="./pix/minkowski-distance.png" width="300">
</p>

**Jaccard similarity**
* Frequency and order of words are ignored.
<p float="left">
	<img src="./pix/jaccard-similarity.png" width="400">
</p>

**Dot product**
<p float="left">
	<img src="./pix/dot-product-1.png" width="400">
</p>

**Normalization of a vector to unit length**
<p float="left">
	<img src="./pix/normalization.png" width="400">
</p>

**Cosine similarity**: Normalized dot product.
<p float="left">
	<img src="./pix/cosine-similarity-1.png" width="400">
	<img src="./pix/cosine-similarity-2.png" width="300">
</p>


### K-nearest neighbors

This is **memory-based/instance-based learning**.
* Training is fast
* It’s easy to add new training data
* Making predictions is slow
* Need to store the training data

**1-nearest neighbors**
<p float="left">
	<img src="./pix/1-nearest-neighbors-2.png" width="400">
	<img src="./pix/1-nearest-neighbors-1.png" width="400">
</p>

![1-nearest-neighbors-3](./pix/1-nearest-neighbors-3.png)

**k-nearest neighbors**
<p float="left">
	<img src="./pix/k-nearest-neighbor-1.png" width="400">
</p>

* Classification speed does not depend on **number of classes**
* Classification speed depends on **number of instances**
![k-nearest-neighbor-2](./pix/k-nearest-neighbor-2.png)

**decision boundary**
![decision-boundary](./pix/decision-boundary.png)

**Decision tree vs K-nearest neighbors**
![comparison](./pix/comparison.png)

### Reference

* https://spacy.io
* https://web.stanford.edu/~jurafsky/slp3/
* http://www.nltk.org/

