
# It's `no big deal`, it just works.

Configurable static documentation based on [`nbformat`]().

### Get it from Github

`pip install git+`<code><a href="https://github.com/tonyfast/nbd/">https://github.com/tonyfast/nbd/</a></code>


## Configuring you documentation

Use any tool you like.


```python
!rm -rf docs/**.htl
!jupyter nbconvert --to python config.ipynb nbd.ipynb --output-dir .
!flake8 nbd.py --output-file=flake8.txt
!pyreverse -o png -p nbd nbd.py
!jupyter nbconvert --to markdown readme.ipynb
!jupyter nbd --config config.py
!mv classes_nbd.png nbd.py config.py flake8.txt docs
```

## Motivation

* An Ipython backed make configuration system

### HTML Views

* [Raw Git](https://rawgit.com/tonyfast/nbd/master/docs/index.html)
* [Github Pages](https://tonyfast.github.io/nbd)

### Notebook Views

* [nbviewer](http://nbviewer.jupyter.org/github/tonyfast/nbd/blob/master/readme.ipynb)
* [github](https://github.com/tonyfast/nbd/blob/master/usage/readme.ipynb)


```python

```
