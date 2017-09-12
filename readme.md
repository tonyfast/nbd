
# It's `no big deal`, it just works.

Documentation ∀ files; based on the [`nbformat`](nbformat.readthedocs.io).

#### Install with version control

`pip install git+`<code><a href="https://github.com/tonyfast/nbd/">https://github.com/tonyfast/nbd/</a></code>


## Why

* `nbconvert` doesn't accept all file formats.  `nbd` adds the concept of loaders
that transform arbitrary files to the nbformat.

## An Example Configuration

### 1. Configure your documentation in python

More configuration options are available at [nbconvert.readthedocs.io/en/latest/config_options.html]()


```python
%%file demo.py
from nbd import *
# use nbd's super basic index

from nbd import index

# Store data in a notebook object
data = notebook(cells=[
    markdown('''# My Demo Page \n\nCheck out the complete [`nbd` documentation](../index.html).''')])

def report(): yield 'index', data
    
c.Docs.notebooks = ['nbd.ipynb', 'readme.md', 'nbd.py']
c.FilesWriter.build_directory = 'docs/demo'
c.Docs.post, c.Docs.report = __import__('nbd').index(data), report
```

    Overwriting demo.py


### 2. Execute `nbd`


```python
!jupyter nbd --config demo.py
```

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
# !wget https://bootswatch.com/readable/bootstrap.min.css --no-check-certificate
# !mv bootstrap.min.css docs/custom.css
```

    [NbConvertApp] Converting notebook config.ipynb to python
    [NbConvertApp] Writing 1182 bytes to ./config.py
    [NbConvertApp] Converting notebook nbd.ipynb to python
    [NbConvertApp] Writing 6072 bytes to ./nbd.py
    parsing nbd.py...
    [NbConvertApp] Converting notebook readme.ipynb to markdown
    [NbConvertApp] Writing 3672 bytes to readme.md
    [Docs] Converting notebook nbd.ipynb to html
    [Docs] Writing 280613 bytes to docs/nbd.ipynb.html
    [Docs] Converting notebook config.ipynb to html
    [Docs] Writing 256375 bytes to docs/config.ipynb.html
    [Docs] Converting notebook config.py to html
    [Docs] Writing 254329 bytes to docs/config.py.html
    [Docs] Converting notebook template.ipynb to html
    [Docs] Writing 250263 bytes to docs/template.ipynb.html
    [Docs] Converting notebook readme.md to html
    [Docs] Writing 258217 bytes to docs/readme.md.html
    [Docs] Converting notebook flake8.txt to html
    [Docs] Writing 271585 bytes to docs/flake8.txt.html
    [Docs] Converting notebook into html
    [Docs] Writing 252550 bytes to docs/index.html
    [Docs] Converting notebook into html
    [Docs] Writing 249380 bytes to docs/uml.html


## Views
### HTML Views

* [Raw Git](https://rawgit.com/tonyfast/nbd/master/docs/index.html)
* [Github Pages](https://tonyfast.github.io/nbd)

### Notebook Views

* [nbviewer](http://nbviewer.jupyter.org/github/tonyfast/nbd/blob/master/readme.ipynb)
* [github](https://github.com/tonyfast/nbd/blob/master/usage/readme.ipynb)


```python

```
