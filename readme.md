
# `nbd`ocumentation 

[<big>NBD</big>](https://github.com/tonyfast/nbd) creates static documentation for Jupyter noteb👀ks. 

> Create documentation from a full featured python script using the nbconvert configuration system.

Below is a sample configuration file to create an index file.


```python
%%file nbd_config.py
from nbd import ReduceExport
from nbconvert.exporters.html import HTMLExporter 
from nbformat.v4 import new_markdown_cell

c.NbConvertApp.notebooks = ['nbd.ipynb', 'readme.ipynb', 'nbd.py']
c.TemplateExporter.template_path = ['templates']
c.FilesWriter.build_directory = 'docs'

# shit = HTMLExporter(config=c).environment.get_template('shit')

class SoupyIndex(ReduceExport):
    def add_entry(self, item, resources):
        return """{header} [{title}]({href})\n""".format(
            header='#'*(int(item.name[-1]) + 3),
            title=item.text,
            href='/'.join([
                resources.get('name')+resources.get('output_extension')
            ])+'#'+str(item.attrs['id']))
    
    def from_render(self, output, resources, **kw):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(output, 'html.parser')
        
        self.nb.cells.append(
            new_markdown_cell('\n'.join([
                self.add_entry(item, resources)
                for item in soup.select('h1,h2,h3')])))
        
        return output, resources
c.StaticExporter.post_render = [SoupyIndex(filename='index')]
```

    Overwriting nbd_config.py



```bash
%%bash
rm -rf docs
mkdir docs
jupyter nbconvert --to python nbd.ipynb
jupyter nbconvert --to markdown readme.ipynb
jupyter nbd --config nbd_config.py
cp custom.css docs/
ls docs/
```

    custom.css
    index.html
    readme.ipynb.html
    readme.md.html


    [NbConvertApp] Converting notebook nbd.ipynb to python
    [NbConvertApp] Writing 3882 bytes to nbd.py
    [NbConvertApp] Converting notebook readme.ipynb to markdown
    [NbConvertApp] Writing 1991 bytes to readme.md
    [NbdApp] Converting notebook readme.md to nbd.StaticExporter
    [NbdApp] Writing 256143 bytes to docs/readme.md.html
    [NbdApp] Converting notebook readme.ipynb to nbd.StaticExporter
    [NbdApp] Writing 252760 bytes to docs/readme.ipynb.html
    [NbdApp] Converting notebook into nbd.StaticExporter
    [NbdApp] Writing 250184 bytes to docs/index.html


### HTML Views

* [Raw Git](https://rawgit.com/tonyfast/nbd/master/docs/index.html)
* [Github Pages](https://tonyfast.github.io/nbd)

### Notebook Views

* [nbviewer](http://nbviewer.jupyter.org/github/tonyfast/nbd/blob/master/readme.ipynb)
* [github](https://github.com/tonyfast/nbd/blob/master/usage/readme.ipynb)
