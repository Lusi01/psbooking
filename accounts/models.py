from django.db import models
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.conf import settings
from utils.models import generate_unique_phone
from hotels.models import Country, City


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.FileField(null=True, blank=True, upload_to="accounts/list", validators=[
        FileExtensionValidator(['jpg', 'png', 'gif', 'svg'])])
    phone = models.CharField(max_length=20, null=True, blank=True)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE, related_name='users')
    city = models.ForeignKey(City, null=True, on_delete=models.CASCADE, related_name='users')
    role = models.ForeignKey(Group, null=True, on_delete=models.CASCADE, related_name='groups')

    class Meta:
        verbose_name_plural = 'Профайлы'
        verbose_name = 'Профайл'

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('accounts:profile')

    @property
    def avatar_url(self):
        return self.avatar.url if self.avatar else f'{settings.STATIC_URL}images/accounts/1.jpg'

    @property
    def get_login(self):
        return self.user.username

    @property
    def get_email(self):
        return self.user.email

    # найти профиль пользователя по e-mail
    @staticmethod
    def get_by_email(email):
        return Profile.objects.filter(email__exact=email).first()

    @property
    def unique_phone(self):
        return generate_unique_phone(Profile, self.phone) if self.phone else ''
