from datetime import datetime
from django.contrib import messages
from django.contrib.auth import login, views as auth_views
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from accounts.forms import (CustomUserCreationForm, ProfileUpdateForm,
                            CustomAuthenticationForm, CustomPasswordResetForm,
                            CustomSetPasswordForm,
                            )
from accounts.models import Profile
from hotels.models import Hotel, Booking, Review
from psbooking.settings import EMAIL_HOST_USER
from allauth.account.views import LoginView
from utils.mixins import MyPermissionRequiredMixin


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'accounts/registration/signin.html'
    success_url = reverse_lazy('main:index')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect_url = reverse_lazy('main:index')
            return HttpResponseRedirect(redirect_url)

        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            redirect_url = reverse_lazy('main:index')
            return HttpResponseRedirect(redirect_url)


class CustomSignUpView(CreateView):
    model = User
    template_name = 'accounts/registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:sign_in')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            redirect_url = reverse_lazy('main:index')
            return HttpResponseRedirect(redirect_url)

        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if self.request.user.is_authenticated:
            redirect_url = reverse_lazy('main:index')
            return HttpResponseRedirect(redirect_url)

    def form_valid(self, form):
        result = super().form_valid(form)
        user = self.object
        if user is not None:
            login(self.request, user)
        return result


class ReviewView(MyPermissionRequiredMixin, ListView):
    permission_required = 'hotels.view_review'
    permission_denied_message = 'Недостаточно прав'

    model = Review
    template_name = 'accounts/review_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'отзывы'
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('hotel') \
            .order_by('hotel', '-updated')

        queryset = queryset.prefetch_related('hotel__rooms__bookings')

        user = self.request.user
        if user.profile:
            if user.profile.role.name == 'Пользователь':
                queryset = queryset.filter(user=user)
        else:
            pass
        return queryset


class BookingView(MyPermissionRequiredMixin, ListView):
    permission_required = 'hotels.view_booking'
    permission_denied_message = 'Недостаточно прав'

    model = Booking
    template_name = 'accounts/booking_list.html'
    context_object_name = 'booking_objects'  # по умолчанию: = object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking_count = Booking.objects.count()
        review_count = Review.objects.count()
        context['title'] = 'бронирования'
        context['booking_count'] = booking_count
        context['review_count'] = review_count
        context['now'] = datetime.now()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        if user.profile:
            if user.profile.role.name == 'Пользователь':
                queryset = queryset.select_related('room__hotel').filter(user=user)
        else:
            pass

        return queryset


class DashboardView(MyPermissionRequiredMixin, ListView):
    permission_required = 'hotels.view_favorite'
    permission_denied_message = '403 Forbidden - недостаточно прав для перехода на страницу '
    model = Hotel
    template_name = 'accounts/dashboard.html'
    context_object_name = 'dashboard_objects'  # по умолчанию: = object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users_count = User.objects.count()
        booking_count = Booking.objects.count()
        review_count = Review.objects.count()
        context['title'] = 'Dashboard'
        context['users_count'] = users_count
        context['booking_count'] = booking_count
        context['review_count'] = review_count
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.EvQuSet()
        return queryset


class ProfileUpdateView(MyPermissionRequiredMixin, UpdateView):
    permission_required = 'accounts.view_profile'
    permission_denied_message = 'Недостаточно прав'

    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_objects'

    def get_object(self, queryset=None):
        pk = self.request.user.pk
        self.kwargs['pk'] = pk

        queryset = super().get_queryset().filter(pk=pk)
        queryset = queryset.select_related('user').prefetch_related(
            'user__bookings__room__hotel', 'user__reviews__hotel')

        profile = super().get_object(queryset)
        profile.phone = profile.unique_phone
        profile.email = profile.get_email
        return profile

    def get(self, request, *args, **kwargs):
        if self.request.user.id == None:
            redirect_url = reverse_lazy('accounts:sign_in')
            return HttpResponseRedirect(redirect_url)

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_profile'] = True
        context['title'] = 'Мой профайл'

        return context

    def form_valid(self, form):
        messages.success(self.request, f'Данные успешно обновлены')
        return super().form_valid(form)


class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/registration/password_reset_form.html'
    form_class = CustomPasswordResetForm
    email_template_name = 'accounts/registration/password_reset_email.txt'
    subject_template_name = 'accounts/registration/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    from_email = EMAIL_HOST_USER  # Это поле вводить обязательно!!!!!!!!!

    def form_valid(self, form):
        self.request.session['reset_email'] = form.cleaned_data['email']
        return super().form_valid(form)


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/registration/password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reset_email'] = self.request.session.get('reset_email', '')

        # удалить авторизованного пользователя из сессии
        if "session_key" in self.request.session.keys():
            del self.request.session["session_key"]

        return context


class CustomPasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'accounts/registration/password_change_done.html'
    success_url = reverse_lazy('accounts:password_change_done'),

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # удалить авторизованного пользователя из сессии
        del self.request.session['_auth_user_id']
        context['user'] = None

        return context


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/registration/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/registration/password_reset_complete.html'
