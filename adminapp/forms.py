from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from authapp.forms import ShopUserEditForm
from authapp.models import ShopUser
from mainapp.models import GameCategories, Games


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class ProductCategoryEditForm(forms.ModelForm):
    class Meta:
        model = GameCategories
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductCategoryEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"


class GameReadForm(forms.ModelForm):
    class Meta:
        model = Games
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GameReadForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"


class GameEditForm(forms.ModelForm):
    class Meta:
        model = Games
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(GameEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = "form-control"
