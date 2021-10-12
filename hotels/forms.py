from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from hotels.models import Hotel, Country, Service, City, Room, Review, Booking
import datetime


class RoomUpdateForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

    is_booking = forms.BooleanField(
        label='Забронирована:',
        widget=forms.CheckboxInput(attrs={'type': 'checkbox'}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        self.fields['hotel'].widget = forms.HiddenInput()
        self.fields['is_booking'].widget.attrs.update({'class': 'form-check-input', 'default': False})

    def clean(self):
        cleaned_data = super().clean()
        if 'is_booking' not in cleaned_data:
            cleaned_data['is_booking'] = False
        return cleaned_data


class RoomCreationForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['hotel', 'logo', 'category', 'description', 'price']

    # запретить создание уже существующей записи
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'special'})


class CityDeleteForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['cityname', ]

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cityname'].widget.attrs.update(
            {'class': 'delete-content',
             'readonly': 'true',
             'type': '',
             'initial': self.fields['cityname']})


class CityUpdateForm(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__'

    country = forms.ModelChoiceField(
        empty_label=None,  # это лоя того, чтобы не выводилась пустая строка в начале
        queryset=Country.objects.all(),
        widget=forms.Select,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'special'})

        self.fields['country'].widget.attrs.update(
            {'class': 'special-text',
             'readonly': 'true',
             'initial': self.fields['country']})

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


class CityCreationForm(forms.ModelForm):
    class Meta:
        model = City
        fields = '__all__'

    country = forms.ModelChoiceField(
        empty_label=None,
        queryset=Country.objects.all(),
        widget=forms.Select,
        required=True,
    )


    # запретить создание уже существующей записи
    def clean(self):
        cleaned_data = super().clean()
        if 'cityname' in cleaned_data.keys():
            if City.objects.filter(cityname=cleaned_data['cityname']).exists():
                raise ValidationError(f'Такой город уже есть!')
        return cleaned_data


class ReviewCreationForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'

    Review_CLASS_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    rate = forms.ChoiceField(label='Оценка', choices=Review_CLASS_CHOICES, )
    text = forms.CharField(label='Текст отзыва', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'special'})

        self.fields['user'].widget = forms.HiddenInput()
        self.fields['hotel'].widget = forms.HiddenInput()
        self.fields['created'].widget = forms.HiddenInput()
        self.fields['rate'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['text'].widget.attrs.update({
            'class': 'form-control',
            'rows': 3,
            'maxlength': 500,
            'cols': 40
        })

    # запретить создание уже существующей записи
    def clean(self):
        cleaned_data = super().clean()

        if 'created' not in cleaned_data:
            cleaned_data['created'] = datetime.date.today().strftime('%Y-%m-%d')

        if 'user' not in cleaned_data:
            raise forms.ValidationError(f'Отзывы могут оставлять только зарегистрированные пользователи')

        if Review.objects.filter(user=cleaned_data['user'], hotel=cleaned_data['hotel'],
                                 created=cleaned_data['created']).exists():
            raise forms.ValidationError(f'Вы уже написали отзыв на этот отель!')

        return cleaned_data

    def clean_rate(self):
        rate = int(self.cleaned_data['rate'])
        if rate > 5:
            raise forms.ValidationError('Максимальная оценка - 5')
        return rate

    def get_redirect_url(self):
        hotel = self.cleaned_data.get('hotel', None)
        if not hotel:
            hotel = get_object_or_404(Hotel, pk=self.date.get('hotel'))
        return hotel.get_absolute_url() if hotel else reverse_lazy('hotels:hotels_list')


class HotelDetailForm(forms.Form):
    d_start = forms.CharField()
    d_end = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class HotelFilterForm(forms.Form):
    country = forms.ModelChoiceField(
        label='Направление',
        queryset=Country.objects.all().defer('countryname'),
        required=False, )

    date_start = forms.DateTimeField(
        label='Дата заезда',
        widget=forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date', 'style': "padding:5px"}),
        required=False)
    date_end = forms.DateTimeField(
        label='Дата отъезда',
        widget=forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date', 'style': "padding:5px"}),
        required=False)

    is_available = forms.BooleanField(
        label='Только доступные варианты',
        widget=forms.CheckboxInput(attrs={'type': 'checkbox'}),
        required=False)

    min_price = forms.CharField(widget=forms.TextInput, required=False)
    max_price = forms.CharField(widget=forms.TextInput, required=False)

    CATEGORY_1 = ''
    CATEGORY_2 = ''
    CATEGORY_3 = ''
    CATEGORY_4 = ''
    CATEGORY_5 = ''
    CATEGORY_CLASS_CHOICES = (
        (5, CATEGORY_5),
        (4, CATEGORY_4),
        (3, CATEGORY_3),
        (2, CATEGORY_2),
        (1, CATEGORY_1),
    )
    category = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=CATEGORY_CLASS_CHOICES,
        required=False,
    )

    service = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'special'})

        self.fields['country'].widget.attrs.update(
            {'class': 'form-control', 'selected': "selected", 'initial': self.fields['country']})

        self.fields['category'].widget.attrs.update({
            'initial': self.fields['category'],
            'style': ' width:40px;',
            'selected': "selected",
        })

        self.fields['service'].widget.attrs.update(
            {
                'class': 'special',
                'selected': "selected",
                'multiple': True,
                'style': 'display:block; width:60px;',
                'initial': self.fields['service']
            })

        self.fields['date_start'].widget.attrs.update({'class': 'form-control mx-1'})
        self.fields['date_end'].widget.attrs.update({'class': 'form-control mx-1'})
        self.fields['is_available'].widget.attrs.update({'class': 'form-check-input', 'default': False})
        self.fields['min_price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'от', 'initial': self.fields['min_price']})
        self.fields['max_price'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'до', 'initial': self.fields['max_price']})


class HotelCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = '__all__'

    category = forms.IntegerField(
        label='Категория (звездность)',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'special'})

        self.fields['description'].widget.attrs.update({'rows': 3})
        self.fields['is_repair'].widget.attrs.update({'class': 'custom_check'})
        self.fields['service'].widget.attrs.update({'class': 'form-control',
                                                    'multiple': True,
                                                    'style': 'min-height:120px',
                                                    'selected': "selected",
                                                    'initial': self.fields['service'],
                                                    })

    def clean_country(self):
        city = None
        if 'city' in self.cleaned_data.keys():
            city = self.cleaned_data['city']
        if not city:
            city = self.instance.city
        country = self.cleaned_data['country']
        yescountry = True if city.country_id == country.id else False  # 0
        if not yescountry:
            raise ValidationError('Страна города не совпадает со страной!')

        return country

    def clean_city(self):
        city = self.cleaned_data['city']
        list_city = list(City.objects.all().values_list('cityname', flat=True))
        yes = True if city.get_city in list_city else False  # 0
        if not yes:
            raise ValidationError('Введен город не из списка!')
        return city


class HotelCreationForm(HotelCreateUpdateForm):
    class Meta:
        model = Hotel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'special'})

    # запретить создание уже существующего события
    def clean(self):
        cleaned_data = super().clean()

        title = cleaned_data.get('title')

        if Hotel.objects.filter(title=title).exists():
            raise forms.ValidationError(f'Такой отель: {title} уже существует')

        return cleaned_data


class HotelUpdateForm(HotelCreateUpdateForm):
    class Meta:
        model = Hotel
        fields = '__all__'  # если только 1 полое, то обязательно после него + запятую!

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)


class BookingCreationForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # запретить создание уже существующей записи
    def clean(self):
        cleaned_data = super().clean()
        if Booking.objects.filter(user=cleaned_data['user'], room=cleaned_data['room'],
                                  date_start=cleaned_data['date_start']).exists():
            raise forms.ValidationError(f'Вы уже забронировали этот номер!')

        return cleaned_data
