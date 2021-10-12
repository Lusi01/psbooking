from django.shortcuts import render
from django.template import RequestContext


def page_not_found_view(request, exception):
    return render(request, 'error_page.html', status=404)

def server_error_view(request, *args, **argv):
    return render(request, 'error_page.html', status=500)

