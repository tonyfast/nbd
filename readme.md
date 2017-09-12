
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

    [Docs] Converting notebook nbd.ipynb to html
    [Docs] Writing 280231 bytes to docs/demo/nbd.ipynb.html
    [Docs] Converting notebook readme.md to html
    [Docs] Writing 257617 bytes to docs/demo/readme.md.html
    [Docs] Converting notebook nbd.py to html
    [Docs] Writing 275472 bytes to docs/demo/nbd.py.html
    [Docs] Converting notebook into html
    [Docs] Writing 250170 bytes to docs/demo/index.html


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
    [NbConvertApp] Writing 5966 bytes to ./nbd.py


## Views
### HTML Views

* [Raw Git](https://rawgit.com/tonyfast/nbd/master/docs/index.html)
* [Github Pages](https://tonyfast.github.io/nbd)

### Notebook Views

* [nbviewer](http://nbviewer.jupyter.org/github/tonyfast/nbd/blob/master/readme.ipynb)
* [github](https://github.com/tonyfast/nbd/blob/master/usage/readme.ipynb)


```python

```
