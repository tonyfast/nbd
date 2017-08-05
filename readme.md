
# `nbd`ocumentation
* [`github`](https://github.com/tonyfast/nbd)

`nbd` creates bare-bones documentation for Jupyter notebooks & _like_ every other kinda file. `nbd` creates a static html views of notebooks documents and code. This minimal documentation _should_ work on most file systems and web servers.  


```bash
    %%bash
    pip install https://github.com/tonyfast/nbd
    python -m nbd --deep
```

    Collecting https://github.com/tonyfast/nbd
      Downloading https://github.com/tonyfast/nbd
    docs/nbd.py.html
    docs/nbd.ipynb.html
    docs/readme.md.html
    docs/usage/basic.ipynb.html
    docs/readme.ipynb.html
    docs/setup.py.html
    docs/index.html


      Cannot unpack file /private/var/folders/0g/4z343jrx1lbb4mz0sqwlfmr00000gp/T/pip-qwjaqvnp-unpack/nbd (downloaded from /private/var/folders/0g/4z343jrx1lbb4mz0sqwlfmr00000gp/T/pip-kbtpmbi_-build, content-type: text/html; charset=utf-8); cannot detect archive format
    Cannot determine archive format of /private/var/folders/0g/4z343jrx1lbb4mz0sqwlfmr00000gp/T/pip-kbtpmbi_-build


## The First Markdown Cell

`nbd` takes the opinion that the 🥇st cell is the abstract or descriptor of a notebook.

## How it works

Every file, even non-notebooks are transformed into __NotebookNode__s that obey the __nbformat.v4__ schemas; __nbconvert__ transforms the notebook nodes to static html documents. `nbd` should not using any special __nbconvert__ templates.

## Why

Because I make a lot of notebooks that combine Python, PySpark, HTML, CoffeeScript, and Markdown.  The static view of the document is how must folks experience your work.  Static documents that contain data-driven narratives can accelerate development within multifunctional teams.

## Why Bootstrap?

Bootstrap is resilient and it ships with the default `--to html` __nbconvert__ converter.

### Convert the readme to markdown for viewing on github.

## Development

Jupyter notebook are the primary mode of development.  The bash script below

1. Creates the `readme.md` document for Github.
2. Converts `nbd` to a Python sript
3. Creates documentation for the notebooks in `nbd`.


```bash
    %%bash
    jupyter nbconvert --to markdown readme.ipynb
    jupyter nbconvert --to python nbd.ipynb
    python -m nbd --deep --ext ipynb --name tonyfast --url https://tonyfast.com/nbd --id nbd
```

    docs/usage/basic.ipynb.html
    docs/nbd.ipynb.html
    docs/readme.ipynb.html
    docs/index.html


    [NbConvertApp] Converting notebook readme.ipynb to markdown
    [NbConvertApp] Writing 1887 bytes to readme.md
    [NbConvertApp] Converting notebook nbd.ipynb to python
    [NbConvertApp] Writing 7574 bytes to nbd.py

