
# It's `no big deal`, it just works.

Documentation ∀ files; based on the [`nbformat`](nbformat.readthedocs.io).

#### Install with version control

`pip install git+`<code><a href="https://github.com/tonyfast/nbd/">https://github.com/tonyfast/nbd/</a></code>


## Why

* `nbconvert` doesn't accept all file formats.  `nbd` adds the concept of loaders
that transform arbitrary files to the nbformat.

## Example Configuration


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



```python
!jupyter nbd --output-dir docs/demo --config demo.py
```

    [Docs] Converting notebook nbd.ipynb to html
    [Docs] Writing 274530 bytes to docs/demo/nbd.ipynb.html
    [Docs] Converting notebook readme.md to html
    [Docs] Writing 256824 bytes to docs/demo/readme.md.html
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

    [NbConvertApp] Converting notebook config.ipynb to python
    [NbConvertApp] Writing 1376 bytes to ./config.py
    [NbConvertApp] Converting notebook nbd.ipynb to python
    [NbConvertApp] Writing 4789 bytes to ./nbd.py
    parsing nbd.py...
    [NbConvertApp] Converting notebook readme.ipynb to markdown
    [NbConvertApp] Writing 2186 bytes to readme.md
    [Docs] Converting notebook nbd.ipynb to html
    [Docs] Writing 274530 bytes to docs/nbd.ipynb.html
    [Docs] Converting notebook config.ipynb to html
    [Docs] Writing 257051 bytes to docs/config.ipynb.html
    [Docs] Converting notebook config.py to html
    [Docs] Writing 254521 bytes to docs/config.py.html
    [Docs] Converting notebook template.ipynb to html
    [Docs] Writing 250260 bytes to docs/template.ipynb.html
    [Docs] Converting notebook readme.md to html
    [Docs] Writing 257596 bytes to docs/readme.md.html
    [Docs] Converting notebook flake8.txt to html
    [Docs] Writing 261700 bytes to docs/flake8.txt.html
    [Docs] Converting notebook into html
    [Docs] Writing 256612 bytes to docs/index.html
    [Docs] Converting notebook into html
    [Docs] Writing 249084 bytes to docs/schema.html
    --2017-09-10 10:29:40--  https://bootswatch.com/readable/bootstrap.min.css
    Resolving bootswatch.com (bootswatch.com)... 104.28.7.66, 104.28.6.66, 2400:cb00:2048:1::681c:742, ...
    Connecting to bootswatch.com (bootswatch.com)|104.28.7.66|:443... connected.
    WARNING: cannot verify bootswatch.com's certificate, issued by ‘CN=COMODO ECC Domain Validation Secure Server CA 2,O=COMODO CA Limited,L=Salford,ST=Greater Manchester,C=GB’:
      Unable to locally verify the issuer's authority.
    HTTP request sent, awaiting response... 200 OK
    Length: unspecified [text/css]
    Saving to: ‘bootstrap.min.css’
    
    bootstrap.min.css       [ <=>                ] 121.62K  --.-KB/s    in 0.06s   
    
    2017-09-10 10:29:40 (2.11 MB/s) - ‘bootstrap.min.css’ saved [124537]
    


## Views
### HTML Views

* [Raw Git](https://rawgit.com/tonyfast/nbd/master/docs/index.html)
* [Github Pages](https://tonyfast.github.io/nbd)

### Notebook Views

* [nbviewer](http://nbviewer.jupyter.org/github/tonyfast/nbd/blob/master/readme.ipynb)
* [github](https://github.com/tonyfast/nbd/blob/master/usage/readme.ipynb)


```python

```
