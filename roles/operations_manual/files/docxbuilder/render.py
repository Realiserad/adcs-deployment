from docxtpl import DocxTemplate
import yaml

document = DocxTemplate('style.docx')
context = yaml.load(open('../../../../group_vars/all.yml'), Loader = yaml.FullLoader)
document.render(context)
document.save('../style.docx')