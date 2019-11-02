## Regression

### Linear Regression

![linear-regression](./pix/linear-regression-1.png)

#### This is a **linear model**
<p float="left">
	<img src="./pix/linear-regression-2.png" width="400" />
	<img src="./pix/linear-regression-3.png" width="400" />
</p>

### Logistic Regression

#### Probability can be used for predicting a class.
* predict 1, when P(y=1|x) ≥ 0.5
* when we increase the threshold from 0.5 to 0.8, precision goes up and recall goes down.
<p float="left">
	<img src="./pix/linear-regression-2.png" width="400" />
	<img src="./pix/logistic-function.png" width="400" />
</p>

#### Decision boundaries: Logistic regression is a linear classifier!
<p float="left">
	<img src="./pix/logistic-regression-1.png" width="400" />
</p>


#### Example
![logistic-regression-2](./pix/logistic-regression-2.png)

Where does the sigmoid function come from?
![sigmoid](./pix/sigmoid.png)

### Learning

![learning](./pix/learning.png)

#### Loss Function

![loss-function-1](./pix/loss-function-1.png)

**Log tranformation**:
![log-transformation](./pix/log-transformation.png)

**Cross-entropy loss**
![cross-entropy-loss-1](./pix/cross-entropy-loss-1.png)
![cross-entropy-loss-2](./pix/cross-entropy-loss-2.png)

**Loss function**
![loss-function-2](./pix/loss-function-2.png)

#### Gradient Descent

**Gradient is a multi-variable generalization of the slope!**

When w is a scalar, below is the example where y is the loss function, y = (w + 3)<sup>2</sup>
![gradient-descent-1](./pix/gradient-descent-1.png)

When w is a matrix:
<p float="left">
	<img src="./pix/gradient-descent-2.png" width="400" />
</p>

#### Regularization

![regularization-1](./pix/regularization-1.png)
![regularization-2](./pix/regularization-2.png)

### Multiclass classification

![softmax](./pix/softmax.png)

### Comparison

**Features**:
* **Decision trees**: Features are manually specified, only a small number of features are used.
* **K-nearest neighbors**: Features are manually specified, all features are used with equal weight.
* **Logistic regression**: Features are manually specified, All features are used, but some features are more important than others.
* **Neural networks**: Features are NOT manually specified.

**Decision boundaries**:
* **Decision trees**: non-linear decision boundaries.
* **K-nearest neighbors**: non-linear decision boundaries.
* **Logistic regression**: a linear decision boundary.
* **Neural networks**: non-linear decision boundaries.

![logistic-regression-3](./pix/logistic-regression-3.png)

### XOR network
![xor-1](./pix/xor-1.png)
![xor-2](./pix/xor-2.png)
![xor-3](./pix/xor-3.png)
![xor-4](./pix/xor-4.png)

### Neural Networks

#### Hyperparameters
* Number of hidden layers
* Size of hidden layers at each layer
* Learning rate
* Batch size
* Dropout rate
* Regularization parameters
* Activation functions

### Reference

* https://developers.google.com/machine-learning/crash-course/reducing-loss/an-iterative-approach
* https://karpathy.github.io/2019/04/25/recipe/
* https://www.thispersondoesnotexist.com/
* http://www.whichfaceisreal.com/
* https://keras.io/
* https://pytorch.org/
* https://www.tensorflow.org/


