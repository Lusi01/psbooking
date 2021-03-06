from django.shortcuts import render


def page_not_found_view(request, exception):
    return render(request, 'error_page.html', status=404)


def server_error_view(request, *args, **argv):
    return render(request, 'error_page500.html', status=500)


def error_404(request):
    return render(request, 'error_page.html', status=200)
