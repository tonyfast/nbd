
# `nbd`ocumentation 

[<big>NBD</big>](https://github.com/tonyfast/nbd) creates static documentation for Jupyter noteb👀ks. 

> This minimal documentation _should_ work on most file systems and web servers; it is just a directory of html files.

## Install `nbd` from <a href="https://github.com/tonyfast/nbd">GITHUB</a> 

    pip install https://github.com/tonyfast/nbd

## Usage

For any directory containing notebooks, run 

    python -m nbd
    
to convert all notebooks, python scripts, and markdown files to a single page documentation viewer.

Add `--deep` to find notebooks in deep nested directories.

    python -m nbd --deep

## Example documentation

[`nbd` uses `nbd` to generate its documentation; the github pages view](https://tonyfast.github.io/nbd) is served by the static files generated by `nbd`.


```bash
    %%bash
    jupyter nbconvert --to notebook --execute --NbConvertApp.use_output_suffix=False usage/development.ipynb
```

    [NbConvertApp] Converting notebook usage/development.ipynb to notebook
    [NbConvertApp] Executing notebook with kernel: python3
    [NbConvertApp] Writing 1920 bytes to usage/development.ipynb


### HTML Views

* [Raw Git](https://rawgit.com/tonyfast/nbd/master/docs/index.html)
* [Github Pages](https://tonyfast.github.io/nbd)

### Notebook Views

* [nbviewer](http://nbviewer.jupyter.org/github/tonyfast/nbd/blob/master/readme.ipynb)
* [github](https://github.com/tonyfast/nbd/blob/master/usage/readme.ipynb)
