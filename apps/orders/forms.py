from django import forms

class CheckoutAddressForm(forms.Form):
    address = forms.CharField(
        label='آدرس کامل',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'شهر، خیابان، کدپستی، تلفن تماس'}),
    )
    def clean_address(self):
        address = self.cleaned_data['address'].strip()
        if len(address) < 10:
            raise forms.ValidationError('آدرس را کامل وارد کنید.')
        return address

class CheckoutPaymentForm(forms.Form):
    METHOD_CHOICES = [('online', 'پرداخت آنلاین (درگاه تست)')]
    payment_method = forms.ChoiceField(label='روش پرداخت', choices=METHOD_CHOICES, widget=forms.RadioSelect)
