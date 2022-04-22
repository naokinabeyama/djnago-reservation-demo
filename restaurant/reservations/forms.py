from django import forms
from datetime import date, timedelta, datetime
from .models import Reservations
from django.utils import timezone

# 2週間
TWO_WEEK = []
today = date.today()
for i in range(0, 13):
    TWO_WEEK.append((f'{today + timedelta(days=i)}', f'{today + timedelta(days=i)}'))

# 予約時間
TIME = [
    ('11:00:00', '11:00 ~ 13:00'),
    ('13:00:00', '13:00 ~ 15:00'),
    ('15:00:00', '15:00 ~ 17:00'),
    ('17:00:00', '17:00 ~ 19:00'),
    ('19:00:00', '19:00 ~ 21:00'),
    ('21:00:00', '21:00 ~ 23:00')
]

# 予約人数
COUNT = []
for i in range(1, 7):
    COUNT.append((f'{i}', f'{i}'))



# 予約登録、更新フォーム
class ReservationForm(forms.Form):
    last_name = forms.CharField(max_length=15)
    first_name = forms.CharField(max_length=15)
    reservation_day = forms.ChoiceField(choices=TWO_WEEK, widget=forms.widgets.Select)
    reservation_time = forms.ChoiceField(choices=TIME, widget=forms.widgets.Select)
    reservation_count = forms.ChoiceField(choices=COUNT, widget=forms.widgets.Select)
    tell = forms.CharField(max_length=12)
    celebration_existence = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput())
    demand = forms.CharField(required=False, widget=forms.Textarea())

    # バリデーション
    def clean(self):
        messages = []
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        messages.append(validationNullCheck(first_name, '氏名（名）'))
        last_name = cleaned_data.get('last_name')
        messages.append(validationNullCheck(last_name, '氏名（姓）'))
        tell = cleaned_data.get('tell')
        messages.append(validationNullCheck(tell, '電話番号'))
        celebration_existence = cleaned_data.get('celebration_existence')
        demand = cleaned_data.get('demand')
        if celebration_existence == True and demand == '':
            messages.append(validationNullCheck(demand, '要望'))
        
        error_msg = []
        for message in messages:
            if message != None:
                error_msg.append(message)
        if len(error_msg) != 0:
            raise forms.ValidationError(error_msg)


def validationNullCheck(value, item):
    if value == None or len(value) == 0:
        return f'{item}を入力して下さい'

