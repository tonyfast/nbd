
# `nbd`ocumentation
* [`github`](https://github.com/tonyfast/nbd)

`nbd` creates bare-bones documentation for Jupyter notebooks & _like_ every other kinda file. `nbd` creates a static html views of notebooks documents and code. This minimal documentation _should_ work on most file systems and web servers.  


```python
    #     !pip install https://github.com/tonyfast/nbd
    !python -m nbd --deep
```

    docs/setup.py.html
    docs/usage/basic.ipynb.html
    docs/nbd.ipynb.html
    docs/nbd.py.html
    docs/readme.ipynb.html
    docs/readme.md.html
    docs/index.html



```python
    import nbd
```

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
