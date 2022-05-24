from docxtpl import DocxTemplate
from docxtpl import InlineImage
from docx.shared import Mm
import yaml
from datetime import date

document = DocxTemplate('proposal-pki-assessment.docx')
context = yaml.load(open('../../group_vars/all.yml'), Loader=yaml.FullLoader)

context['__datestring'] = date.today().strftime('%B %d, %Y')
context['__logo'] = InlineImage(
    document, 
    image_descriptor='../customer/logo.png', 
    width=Mm(20), 
    height=Mm(10))

document.render(context)
document.save('../../Anbud - Genomlysning av PKI.docx')
