
# coding: utf-8

# The main source for the `nbd` jupyter application and its notebook creation tools.  The nbformat namespace was renamed to simplify the creation of new notebooks.  When someone is using `nbd` they should expect to make one python configuration file that is executed from the command line with 
# 
#         jupyter nbd --config config.py

# In[1]:


__all__ = 'markdown', 'notebook', 'code', 'raw', 'output', 'reads'


# In[2]:


from nbconvert.nbconvertapp import NbConvertApp
from traitlets import Any  # These should be properly assigned
import typing as t

class Docs(NbConvertApp):    
    loaders = Any(default_value=tuple(), help="""""").tag(config=True)
    post = Any(default_value=None, help="""""").tag(config=True)
    report = Any(default_value=None, help="""""").tag(config=True)
                
    def convert_notebooks(self):
        super().convert_notebooks() or self.report and [
            name and NbConvertApp.convert_single_notebook(
                    self, name, io.StringIO(writes(nb))) for name, nb in self.report()]
   
    def init_single_notebook_resources(self, notebook_filename):
        resources = super().init_single_notebook_resources(notebook_filename)
        resources['name'] = resources['unique_key'] = notebook_filename
        return resources    

main = launch_new_instance = Docs.launch_instance


# Continuing on attributes are appened to the `Docs` class as they become necessary.

# ## Callable Exporter

# In[3]:


from nbformat import reads, io, writes, NotebookNode

def identity(path, resources: dict=None, **kw) -> t.Tuple[NotebookNode, dict]:
    """callable to export ipynb files"""
    return reads(path.read_text(), 4), resources

class FuncExporter(__import__('nbconvert').exporters.html.HTMLExporter):
    callable = Any(identity)
    def from_filename(self, file_name: str, resources: dict=None, **kw) -> t.Tuple[str, dict]:
        html, resources = self.from_notebook_node(
            *self.callable(Path(file_name), resources, **kw), **kw)
        return html, resources


# Update the exporter each time a new notebook is accessed.

# In[4]:


def convert_single_notebook(self, name, buffer=None):    
    path = Path(name)
    for exts, exporter in reversed([*RULES, *self.loaders]):  # There is a better way to have default loaders
        if path.suffix[1:] in exts:
            self.exporter = (
                isinstance(exporter, __import__('nbconvert').exporters.base.Exporter)
                and exporter or FuncExporter(callable=exporter))
            return super(Docs, self).convert_single_notebook(name, buffer)
    else:
        self.log.warning("{} was not converted; there is no rule for the {} suffix.".format(str(path), path.suffix))

Docs.convert_single_notebook = convert_single_notebook


# ## The Loaders.
# 
# The default loader is notebooks only.  

# In[112]:


def minimal_style(callable: t.Callable[[str, dict], NotebookNode]
                 ) -> t.Callable[[str, dict], t.Tuple[NotebookNode, dict]]:
    """A minimal style wrapper other file types"""
    def _return_nb(path, resources=None, **kw):
        return notebook(cells=[
            markdown("""# [{}]({})""".format(str(path), str(path)+'.html')),
            callable(path.read_text())]), resources
    return _return_nb


# Notebooks are created using objects in the `nbformat` package; rename these objects to have shorter namespaces.

# ### Default loaders

# In[6]:


from nbformat.v4 import (
    new_code_cell     as code, 
    new_markdown_cell as markdown, 
    new_notebook      as notebook, 
    new_raw_cell      as raw, 
    new_output        as output)

RULES = [
    (('ipynb',), identity), 
    (('py', 'pyi'), minimal_style(code)), 
    (('md', 'markdown'), minimal_style(markdown)), 
    (('txt',), minimal_style(code))]


# ## Post Processing
# 
# The standard post processor recieves just the notebook name, this one recieves the exported text, resources, and name.

# In[7]:


class CallablePostProcessor(__import__('nbconvert').postprocessors.PostProcessorBase):
    """Call an arbitrary function after it has been writen to disk."""
    callable = Any().tag(config=True)    
    def postprocess(self, result: t.Tuple[str, dict, str]) -> None:
        html, resources, notebook_name = result
        self.callable(html, resources, notebook_name)


# In[8]:


def init_postprocessor(self):
    if self.post: self.postprocessor = CallablePostProcessor(callable=self.post)
    else:  super(Docs, self).init_postprocessor()

Docs.init_postprocessor = init_postprocessor


# ## Writing 
# 
# The post processor above requires a patched files writer.

# In[9]:


class FilesWriter(__import__('nbconvert').writers.FilesWriter):
    """Use the same name so configuration works the same.  This patch assures the parent directory exists and returns the output, resources, and name.
    """
    def write(self, output: str, resources: dict, notebook_name: str) -> t.Tuple[str, dict, str]:
        """Returns a tuple of the output html, resources, and file destination. These
        values are available to the post processor."""
        (lambda path: path.parent.exists() or path.parent.mkdir())(
            self.build_directory / Path(notebook_name))
        return output, resources, super().write(output, resources, notebook_name)


# Change the default directory path to docs to be consistent with github pages.

# In[10]:


FilesWriter.build_directory.default_value = 'docs'
Docs.writer_class.default_value = 'nbd.FilesWriter'


# > A Most Basic Index that lists the notebooks.

# In[111]:


def index(data):
    def _index(html, resources, destination):
        """"""
        data.cells.append(markdown("""# [{0}]({1})\n\n---\n\n""".format(
            resources.get('name'),resources.get('name') + destination.split(resources.get('name'), 1)[-1])))
    return _index


# If imports are needed in scope then don't import them.

# In[ ]:


from pathlib2 import Path

