
# It's `no big deal`, it just works.

Documentation ∀ files; based on the [`nbformat`](nbformat.readthedocs.io).

#### Install with version control

`pip install git+`<code><a href="https://github.com/tonyfast/nbd/">https://github.com/tonyfast/nbd/</a></code>


## Why

* `nbconvert` doesn't accept all file formats.  `nbd` adds the concept of loaders
that transform arbitrary files to the nbformat.

## An Example Configuration

### 1. Execute from the application


```python
%%file demo.py
from nbd import *

data = notebook()
data.cells.append(markdown('# My Demo Page\n\n'))

def index(html, resources, name):
    data.cells[-1].source += '* [{}]({})\n'.format(name, name+resources['output_extension'])
    
def report():
    yield 'index', data
    
c.Docs.notebooks = ['nbd.ipynb', 'readme.md', 'nbd.py']
c.Docs.post, c.Docs.report = index, report
```

    Overwriting demo.py


### 2. Execute from the application


```python
!jupyter nbd --output-dir docs/demo --config demo.py
```

    [Docs] Converting notebook nbd.ipynb to html
    [Docs] Writing 274530 bytes to docs/demo/nbd.ipynb.html
    [Docs] Converting notebook readme.md to html
    [Docs] Writing 257958 bytes to docs/demo/readme.md.html
    [Docs] Converting notebook nbd.py to html
    [Docs] Writing 272320 bytes to docs/demo/nbd.py.html
    [Docs] Converting notebook into html
    [Docs] Writing 249269 bytes to docs/demo/index.html


## Motivation

* An Ipython backed make configuration system
* It works for every file

## Developer

Configure the documentation for this project through the readme file.


```python
!jupyter nbconvert --to python config.ipynb nbd.ipynb --output-dir .
!flake8 nbd.py --output-file=flake8.txt
!pyreverse -o png -p nbd nbd.py
!jupyter nbconvert --to markdown readme.ipynb
!jupyter nbd --config config.py
!mv classes_nbd.png config.py flake8.txt docs
!wget https://bootswatch.com/readable/bootstrap.min.css --no-check-certificate
!mv bootstrap.min.css docs/custom.css
```

## Views
### HTML Views

* [Raw Git](https://rawgit.com/tonyfast/nbd/master/docs/index.html)
* [Github Pages](https://tonyfast.github.io/nbd)

### Notebook Views

* [nbviewer](http://nbviewer.jupyter.org/github/tonyfast/nbd/blob/master/readme.ipynb)
* [github](https://github.com/tonyfast/nbd/blob/master/usage/readme.ipynb)


```python

```
