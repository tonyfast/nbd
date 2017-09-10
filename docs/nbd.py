
# coding: utf-8

# # `Docs` built on `nbconvert`

# * Callable exporter 
# * Callable postprocessor
# * Nested file writer

# In[110]:


from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook, new_raw_cell
import nbformat
from traitlets import Any
from nbconvert.nbconvertapp import NbConvertApp
from nbconvert.exporters import html
from nbconvert import writers, postprocessors
from pathlib2 import Path

__all__ = 'main', 'launch_new_instance'


# In[108]:


class PostProcess(postprocessors.PostProcessorBase):
    callable = Any().tag(config=True)    
    def postprocess(self, write_result):
        html, resources, notebook_name = write_result
        self.callable(html, resources, notebook_name)


# In[106]:


class FilesWriter(writers.FilesWriter):
    """Use the same name so I don't have write an configuration docs.
    This monkey patch assures the parent directory exists.
    """
    def write(self, output, resources, notebook_name):
        (lambda path: path.parent.exists() or path.parent.mkdir())(
            self.build_directory / Path(notebook_name))
        super().write(output, resources, notebook_name)
        return output, resources, notebook_name
        
FilesWriter.build_directory.default_value = 'docs'


# In[102]:


def notebook(path, resources=None, **kw):
    """callable to export ipynb files"""
    return nbformat.reads(path.read_text(), 4), resources


# __`FuncExporter`__ is a flexible `nbconvert` exporter. It calls a function that returns
# a new `nbformat.NotebookNode` object and a resources dictionary.  This exporter is called
# with the `Docs` `NbConvertApp` app.

# In[101]:


class FuncExporter(html.HTMLExporter):
    callable = Any(notebook)
    def from_filename(self, file_name, resources=None, **kw):
        html, resources = self.from_notebook_node(
            *self.callable(Path(file_name), resources, **kw), **kw)
        return html, resources


# In[103]:


def minimal_style(new):
    """A minimal style wrapper other file types"""
    def _return_nb(path, resources=None, **kw):
        return new_notebook(cells=[
            nbformat.v4.new_markdown_cell("""# [{0}]({0})""".format(str(path))),
            new(path.read_text())]), resources
    return _return_nb


# In[107]:


rules = {
    ('ipynb',): notebook,
    ('py', 'pyi'): minimal_style(new_code_cell),
    ('md', 'markdown'): minimal_style(new_markdown_cell),
    ('txt',): minimal_style(new_code_cell)}


# In[105]:


class Docs(NbConvertApp):    
    loaders = Any(
        default_value=rules, help="""""").tag(config=True)
    post = Any(default_value=None).tag(config=True)
    report = Any(default_value=None).tag(config=True)

    def convert_single_notebook(self, notebook_filename, input_buffer=None):    
        path = Path(notebook_filename)
        exporter = self.exporter
        for exts, callable in self.loaders.items():
            if path.suffix[1:] in exts:
                self.exporter = FuncExporter(callable=callable)
                return super().convert_single_notebook(notebook_filename, input_buffer)
        else:
            self.exporter = exporter
        self.log.warning("{} was not converted; there is no rule for the {} suffix.".format(str(path), path.suffix))
            
    def convert_notebooks(self):
        super().convert_notebooks() or self.report and [
            name and NbConvertApp.convert_single_notebook(
                    self, name, nbformat.io.StringIO(nbformat.writes(nb))) for name, nb in self.report()]
   
    def init_single_notebook_resources(self, notebook_filename):
        resources = super().init_single_notebook_resources(notebook_filename)
        resources['name'] = resources['unique_key'] = notebook_filename
        return resources    
     
    def init_writer(self): 
        self.writer = FilesWriter(config=self.config)
        
    def init_postprocessor(self):
        if self.post: self.postprocessor = PostProcess(callable=self.post)
        else:  super().init_postprocessor()
        
main = launch_new_instance = Docs.launch_instance


# In[2]:


def basic_index(data):
    def _index(html, resources, notebook_name):
        """"""
        from bs4 import BeautifulSoup
        html = BeautifulSoup(html, 'html.parser')    
        location = notebook_name+resources['output_extension']
        data.cells.append(new_markdown_cell("""[<small>{}</small>]({})""".format(resources['name'], location)))
        data.cells.append(new_markdown_cell(
            "\n".join(
                """{} [{}]({}#{})\n""".format('#'*int(h.name[-1]),h.text, location, h.attrs['id']) 
                for h in html.select('h1,h2'))))
        data.cells[-1].source +="""\n---\n\n"""
    return _index

