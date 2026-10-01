from django import forms
from django.forms import inlineformset_factory
from .models import Artwork, ArtworkImage

class ArtworkForm(forms.ModelForm):
    class Meta:
        model = Artwork
        fields = ['title', 'slug', 'category', 'description', 'price',
                  'width', 'height', 'technique', 'year_created',
                  'status', 'main_image', 'is_featured']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise forms.ValidationError('قیمت باید بیشتر از صفر باشد.')
        return price

    def clean_year_created(self):
        year = self.cleaned_data['year_created']
        if year < 1000 or year > 2026:
            raise forms.ValidationError('سال خلق معتبر نیست.')
        return year

ArtworkImageFormSet = inlineformset_factory(
    Artwork, ArtworkImage,
    fields=['image', 'caption'],
    extra=3, can_delete=True
)
