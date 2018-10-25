from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

import os
from django.conf import settings
from django.template import Context

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    # print("@@@@@@@@@@@@@@@ passed in url @@@@@@@@@@@@@@@@@ ")
    # print("@@@@@@@@@@@@@@@ end passed in url @@@@@@@@@@@@@@@@@ ")

    
    if uri.startswith(sUrl):
    	# print(sRoot)
    	path = os.path.join(sRoot, uri.replace(sUrl, ""))
    	print(path)
    elif uri.startswith(mUrl):
    	print("***************found /ststic/media********************")
    	path = os.path.join(mRoot, uri.replace(mUrl, ""))
    else:
    	print("*************** Not found /ststic/********************")
    	return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path


def render_to_pdf_with_image(template_src, context_dict={}):
	template_path = template_src
	context = context_dict
	# Create a Django response object, and specify content_type as pdf
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="report.pdf"'
	# find the template and render it.
	template = get_template(template_path)
	html = template.render(context)

	# # Create a Django response object, and specify content_type as pdf
	# response = HttpResponse(content_type='application/pdf')
	# response['Content-Disposition'] = 'attachment; filename="report.pdf"'
	# # find the template and render it.
	# template = get_template(template_src)
	# html = template.render(context_dict)

	# create a pdf
	pisaStatus = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
	# if error then show some funy view
	
	if pisaStatus.err:
		return HttpResponse('We had some errors <pre>' + html + '</pre>')
    	
	return response

	# result = BytesIO()
	# pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	# if not pdf.err:
	# 	return HttpResponse(result.getvalue(), content_type='application/pdf')
	# return None	