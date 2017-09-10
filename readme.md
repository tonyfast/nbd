
# It's `no big deal`, it just works.

Documentation ∀ files; based on the [`nbformat`](nbformat.readthedocs.io).

### Install with version control

`pip install git+`<code><a href="https://github.com/tonyfast/nbd/">https://github.com/tonyfast/nbd/</a></code>


## Why

* `nbconvert` doesn't accept all file formats.  `nbd` adds the concept of loaders
that transform arbitrary files to the nbformat.


```python
%%file demo.py
from nbd import *

data = notebook()
data.cells.append(markdown('# My Demo Page\n\n'))

def index(html, resources, name):
    data.cells[-1].source += '* [{}]({})\n'.format(name, name+resources['output_extension'])
    
def report():
    yield 'index', data
    
c.Docs.notebooks = ['nbd.ipynb', 'readme.md', 'config.py']
c.Docs.post, c.Docs.report = index, report
```

    Overwriting demo.py



```python
!jupyter nbd --output-dir docs/demo --config demo.py
```

    [Docs] Converting notebook nbd.ipynb to html
    [Docs] Writing 274196 bytes to docs/demo/nbd.ipynb.html
    [Docs] Converting notebook readme.md to html
    [Docs] Writing 254809 bytes to docs/demo/readme.md.html
    [Docs] Converting notebook config.py to html
    [Docs] Writing 254290 bytes to docs/demo/config.py.html
    [Docs] Converting notebook into html
    [Docs] Writing 249275 bytes to docs/demo/index.html


## Motivation

* An Ipython backed make configuration system
* It works for every file

## Developer


```python
!jupyter nbconvert --to python config.ipynb nbd.ipynb --output-dir .
!flake8 nbd.py --output-file=flake8.txt
!pyreverse -o png -p nbd nbd.py
!jupyter nbconvert --to markdown readme.ipynb
!jupyter nbd --config config.py
!mv classes_nbd.png config.py flake8.txt docs
```

    [NbConvertApp] Converting notebook config.ipynb to python
    [NbConvertApp] Writing 1381 bytes to ./config.py
    [NbConvertApp] Converting notebook nbd.ipynb to python
    [NbConvertApp] Writing 4741 bytes to ./nbd.py
    parsing nbd.py...
    [NbConvertApp] Converting notebook readme.ipynb to markdown
    [NbConvertApp] Writing 3265 bytes to readme.md
    [Docs] Converting notebook nbd.ipynb to html
    [Docs] Writing 274196 bytes to docs/nbd.ipynb.html
    [Docs] Converting notebook config.ipynb to html
    [Docs] Writing 258717 bytes to docs/config.ipynb.html
    [Docs] Converting notebook config.py to html
    [Docs] Writing 254485 bytes to docs/config.py.html
    [Docs] Converting notebook template.ipynb to html
    [Docs] Writing 249736 bytes to docs/template.ipynb.html
    [Docs] Converting notebook readme.md to html
    [Docs] Writing 257704 bytes to docs/readme.md.html
    [Docs] Converting notebook flake8.txt to html
    [Docs] Writing 261694 bytes to docs/flake8.txt.html
    [Docs] Converting notebook into html
    [Docs] Writing 255721 bytes to docs/index.html
    [Docs] Converting notebook into html
    [Docs] Writing 249084 bytes to docs/schema.html


## Visews
### HTML Views

* [Raw Git](https://rawgit.com/tonyfast/nbd/master/docs/index.html)
* [Github Pages](https://tonyfast.github.io/nbd)

### Notebook Views

* [nbviewer](http://nbviewer.jupyter.org/github/tonyfast/nbd/blob/master/readme.ipynb)
* [github](https://github.com/tonyfast/nbd/blob/master/usage/readme.ipynb)


```python

```
