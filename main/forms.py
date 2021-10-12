from django import forms


class MainFilterForm(forms.Form):
    date_start = forms.DateTimeField(
        label='Заезд:',
        widget=forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'}),
        required=False)
    date_end = forms.DateTimeField(
        label='Отъезд:',
        widget=forms.DateInput(format="%Y-%m-%d", attrs={'type': 'date'}),
        required=False)

    COUNT_GUEST = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)]
    guests = forms.ChoiceField(
        label='Человек:',
        choices=COUNT_GUEST,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'special'})

        self.fields['date_start'].widget.attrs.update({'class': 'form-control mx-1'})
        self.fields['date_end'].widget.attrs.update({'class': 'form-control mx-1'})
        self.fields['guests'].widget.attrs.update({'class': 'form-check ', 'default': '1'})
