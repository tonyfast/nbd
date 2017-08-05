
# `nbd`ocumentation

`nbd` creates bare-bones documentation for Jupyter notebooks & _like_ every other kinda file. `nbd` creates a static html views of notebooks documents and code. This minimal documentation _should_ work on most file systems and web servers.  


```python
    %load_ext importable
    import nbd
```

    The importable extension is already loaded. To reload it, use:
      %reload_ext importable


## How it works

Every file, even non-notebooks are transformed into __NotebookNode__s that obey the __nbformat.v4__ schemas; __nbconvert__ transforms the notebook nodes to static html documents. `nbd` should not using any special __nbconvert__ templates.

## Why

Because I make a lot of notebooks that combine Python, PySpark, HTML, CoffeeScript, and Markdown.  The static view of the document is how must folks experience your work.  Static documents that contain data-driven narratives can accelerate development within multifunctional teams.

## Why Bootstrap?

Bootstrap is resilient and it ships with the default `--to html` __nbconvert__ converter.

### Convert the readme to markdown for viewing on github.


```python
!jupyter nbconvert --to markdown readme.ipynb
```

    [NbConvertApp] Converting notebook readme.ipynb to markdown
    [NbConvertApp] Writing 1214 bytes to readme.md

