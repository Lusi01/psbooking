from django.utils.text import slugify
from unidecode import unidecode
import re
import phonenumbers


def generate_unique_slug(model, value):
    unique_slug = slugify(unidecode(value if value else 'empty'), allow_unicode=True).lower()
    count = 1
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = f'{unique_slug}-{count}'
        count += 1
    return unique_slug


def phone_format(national_f):
    len_n = len(national_f)
    out_Tel = '+7 '

    while len_n > 0:
        out_Tel = out_Tel + '(' + national_f[0:3] + ') '
        len_n -= 3
        if len_n < 0:
            break
        out_Tel = out_Tel + national_f[3:6] + "-"
        len_n -= 3
        if len_n < 0:
            break
        out_Tel = out_Tel + national_f[6:8] + "-"
        len_n -= 2
        if len_n < 0:
            break
        out_Tel = out_Tel + national_f[8:]
        len_n -= 2
    return out_Tel


def generate_unique_phone(model, value):
    out_Tel_parse = phonenumbers.parse(value, "RU")  # country_code = 7, national_number = 9998886677
    out_Tel = phone_format(str(out_Tel_parse.national_number))
    return out_Tel



