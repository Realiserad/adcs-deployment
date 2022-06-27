from genericpath import isfile
from os import listdir
from docxtpl import DocxTemplate
from docxtpl import InlineImage
from docx.shared import Mm
import yaml
from datetime import date

# Loop over all the files in this directory with the file extension .docx and
# render them using Jinja2.
def render_files(directory):
    for file_name in directory:
        if file_name.endswith(".docx"):
            render_file(file_name)

# Renders a single file using Jinja2.
def render_file(file_name):
    document = DocxTemplate(file_name)
    context = yaml.load(open('../../group_vars/all.yml'), Loader = yaml.FullLoader)

    context['__datestring'] = date.today().strftime('%B %d, %Y')
    context['__logo'] = InlineImage(
        document,
        image_descriptor = '../customer/logo.png',
        width = Mm(20),
        height = Mm(10))

    document.render(context)
    document.save('../../release/' + file_name)

# Get the names of all files in the current directory
def get_files():
    return [f for f in listdir('.') if isfile('./' + f)]

render_files(get_files())