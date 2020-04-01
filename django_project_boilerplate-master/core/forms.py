from django import forms

PAYMENT_CHOICES = (
    ('N', 'Оплатит при доставке'),
    ('C', 'Оплатить с помощью карты'),
    ('K', 'Click'),
    ('P', 'Payme')
)


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Яккасарайский район, улица Шота Руставели, дом 77'
    }))

    city = forms.ChoiceField()
    same_billing_adress = forms.BooleanField(widget=forms.CheckboxInput())
    save_info = forms.BooleanField(widget=forms.CheckboxInput())
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
