from django import forms
from .models import Category, Product, ProductPicture
from django.core.files.base import ContentFile
from .models import ProductReview
# Custom widget for multiple file input
class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class LocalProductForm(forms.Form):
    name = forms.CharField(max_length=150)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    description = forms.CharField(widget=forms.Textarea(attrs={'style': 'display:inline-block'}))
    email = forms.EmailField(max_length=150)
    images = forms.FileField(
        widget=MultiFileInput(attrs={'multiple': True, 'style': 'display:inline-block'}),
        required=False
    )
    category_choices = forms.ChoiceField(choices=[], required=False, label='Choose Category')
    add_category = forms.CharField(max_length=150, required=False, label='or Enter Category')

    def __init__(self, *args, **kwargs):
        # Grab files from kwargs
        self.files_data = kwargs.pop('files', None)
        super(LocalProductForm, self).__init__(*args, **kwargs)
        self.fields['category_choices'].choices = [(c.id, c.categories) for c in Category.objects.all()]

    def clean(self):
        cleaned_data = super().clean()
        category_choices = cleaned_data.get('category_choices')
        add_category = cleaned_data.get('add_category')

        if not category_choices and not add_category:
            raise forms.ValidationError('Please choose an existing category or enter a new one.')
        if category_choices and add_category:
            raise forms.ValidationError('Choose either an existing category or a new one, not both.')
        return cleaned_data

    def set_user(self, user):
        self.user = user

    def save(self, product=None, commit=True):
        if product is None:
            product = Product()

        product.name = self.cleaned_data['name']
        product.price = self.cleaned_data['price']
        product.description = self.cleaned_data['description']
        product.email = self.cleaned_data['email']
        product.local = True
        product.user = self.user

        if self.cleaned_data['category_choices']:
            product.category_id = self.cleaned_data['category_choices']
        elif self.cleaned_data['add_category']:
            category = Category(type='Product', categories=self.cleaned_data['add_category'])
            category.save()
            product.category = category

        if commit:
            product.save()

        # Save multiple images
        if self.files_data:
            images = self.files_data.getlist('images')
            for image in images:
                ProductPicture.objects.create(product=product, picture=image)

        return product
    


class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['stars_given', 'comment']
        widgets = {
            'stars_given': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 0.5}),
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review...'}),
        }
