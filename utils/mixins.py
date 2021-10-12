from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from accounts.models import Profile


class PERMISSION_REQUIRED(PermissionRequiredMixin):
    permission_required = None


class MyPermissionRequiredMixin(PERMISSION_REQUIRED):

    def has_permission(self):
        perms = self.get_permission_required()
        return self.request.user.has_perms(perms)

    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            str_url = self.request.environ['HTTP_REFERER']
            path = self.request.path
            mess = self.permission_denied_message + 'для перехода по ' + path
            messages.error(self.request, mess)
            return HttpResponseRedirect(str_url)

        if self.request.method == 'GET':
            return super().get(self.request)
        else:
            return super().post(self.request)

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return super().handle_no_permission()

        if not self.has_permission():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class AjaxFormMixin(object):
    def form_invalid(self, form):
        response = super(AjaxFormMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxFormMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'message': "Данные отправлены успешно."
            }
            return JsonResponse(data)
        else:
            return response
