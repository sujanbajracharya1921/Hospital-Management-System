import random
import string
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa  
from django.conf import settings

SHORTCODE_MIN=getattr(settings,"SHORTCODE_MIN",4)


def code_generator(size=SHORTCODE_MIN,chars=string.ascii_lowercase+string.digits):
    #new_code=''
    #for _in range(size):
    #  new_code+=random.choice(chars)
    #return new_code
    return ''.join(random.choice(chars)for _ in range(size))

def render_to_pdf(template_src,context_dict={}):
    template=get_template(template_src)
    html=template.render(context_dict)
    result=BytesIO()
    pdf=pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type="application/pdf")
    return None
