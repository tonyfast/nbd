
# coding: utf-8

# # A Pure Configuration Approach to Docs

# Rely on `nbformat` for the schema.

# ## Data Objects
# 
# Create data objects directly in the configuration file.  These will be appended and written later.

# In[5]:


from pathlib2 import Path
data = __import__('nbformat').reads(Path('template.ipynb').read_text(), 4)
last = data.cells.pop(-1)


# In[6]:


from nbformat.v4 import *
def basic(html, resources, notebook_name):
    from bs4 import BeautifulSoup
    html = BeautifulSoup(html, 'html.parser')    
    location = notebook_name+resources['output_extension']
    data.cells.append(new_markdown_cell("""[<small>{}</small>]({})""".format(resources['name'], location)))
    data.cells.append(new_markdown_cell(
        "\n".join(
            """{} [{}]({}#{})\n""".format('#'*int(h.name[-1]),h.text, location, h.attrs['id']) 
            for h in html.select('h1,h2'))))
    data.cells[-1].source +="""\n---\n\n"""


# ## Creating custom reports

# In[7]:


def report():
    data.cells.append(new_markdown_cell(
        """### [Schema](schema.html)"""
    ))
    data.cells.append(last)
    yield 'index', data
    yield 'schema', new_notebook(cells=[
        new_markdown_cell("""![classes_nbd.png](classes_nbd.png)""")])


# In[8]:


try:
    c
except NameError:
    c= __import__('traitlets').config.Config()

c.FilesWriter.build_directory = 'docs'
c.Docs.update(
    post=basic, 
    report=report,
    notebooks=[
        'nbd.ipynb',
        'config.ipynb',
        'config.py',
        'template.ipynb',
        'readme.md', 'flake8.txt'])

