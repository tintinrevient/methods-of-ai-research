## First Order Logic

a **model** M = (D, I):
* D is **domain**
* I is **interpretation** that interprets the language in D
	* for n-ary predicate P(x<sub>1</sub>, ..., x<sub>n</sub>), I(P) is a subset of D<sup>n</sup>
	* for n-ary function f(x<sub>1</sub>, ..., x<sub>n</sub>), I(f) is a function from D<sup>n</sup> to D
* **valuation**/**variable assignment** μ assigns elements of D to the variables
* **denotation** |t| or |t|<sub>I, μ</sub> of a term t:
	* if t is a variable x, then |x|<sub>I, μ</sub> = μ(x)
	* if t = f(t<sub>1</sub>, ..., t<sub>n</sub>), then |t|<sub>I, μ</sub> = I(f)(|t<sub>1</sub>|<sub>I, μ</sub>, ..., |t<sub>n</sub>|<sub>I, μ</sub>)

![denotation](./pix/denotation.png)

a formula φ is **valid**/**satisfied** in M under valuation μ: (M, μ |= φ) if:
* φ = P(x<sub>1</sub>, ..., x<sub>n</sub>) and (|t<sub>1</sub>|<sub>I, μ</sub>, ..., |t<sub>n</sub>|<sub>I, μ</sub>) belongs to I(P)
* φ = φ1 ∧ φ2, and (M, μ) |= φ1 and (M, μ) |= 􏳚φ2
* φ = φ1 ∨ φ2, and (M, μ) |= φ1 or (M, μ) |= 􏳚φ2
* φ = ¬ψ, and (M, μ̸) does not entail 􏳚ψ
* φ = ∃x ψ(x), if (M, μ') |= ψ(x) for some valuation μ' that differs from μ at most at x
* φ = ∀x ψ(x), if (M, μ') |= ψ(x) for all valuations μ' that differ from μ at most at x

![valid](./pix/valid.png)

### Syllogism

<p float="left">
	<img src="./pix/syllogism.png" width="600" />
</p>
