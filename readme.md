
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
    [Docs] Writing 280752 bytes to docs/demo/nbd.ipynb.html
    [Docs] Converting notebook readme.md to html
    [Docs] Writing 257333 bytes to docs/demo/readme.md.html
    [Docs] Converting notebook nbd.py to html
    [Docs] Writing 275782 bytes to docs/demo/nbd.py.html
    [Docs] Converting notebook into html
    [Docs] Writing 249359 bytes to docs/demo/index.html


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
    [NbConvertApp] Writing 1376 bytes to ./config.py
    [NbConvertApp] Converting notebook nbd.ipynb to python
    [NbConvertApp] Writing 6098 bytes to ./nbd.py
    parsing nbd.py...
    invalid syntax (<string>, line 137)
    [NbConvertApp] Converting notebook readme.ipynb to markdown
    [NbConvertApp] Writing 3521 bytes to readme.md
    Traceback (most recent call last):
      File "/Users/tonyfast/anaconda/bin/jupyter-nbd", line 11, in <module>
        load_entry_point('nbd', 'console_scripts', 'jupyter-nbd')()
      File "/Users/tonyfast/anaconda/lib/python3.5/site-packages/setuptools-27.2.0-py3.5.egg/pkg_resources/__init__.py", line 565, in load_entry_point
      File "/Users/tonyfast/anaconda/lib/python3.5/site-packages/setuptools-27.2.0-py3.5.egg/pkg_resources/__init__.py", line 2598, in load_entry_point
      File "/Users/tonyfast/anaconda/lib/python3.5/site-packages/setuptools-27.2.0-py3.5.egg/pkg_resources/__init__.py", line 2258, in load
      File "/Users/tonyfast/anaconda/lib/python3.5/site-packages/setuptools-27.2.0-py3.5.egg/pkg_resources/__init__.py", line 2264, in resolve
      File "/Users/tonyfast/nbd/nbd.py", line 137
        Docs.
            ^
    SyntaxError: invalid syntax


## Views
### HTML Views

* [Raw Git](https://rawgit.com/tonyfast/nbd/master/docs/index.html)
* [Github Pages](https://tonyfast.github.io/nbd)

### Notebook Views

* [nbviewer](http://nbviewer.jupyter.org/github/tonyfast/nbd/blob/master/readme.ipynb)
* [github](https://github.com/tonyfast/nbd/blob/master/usage/readme.ipynb)


```python

```
