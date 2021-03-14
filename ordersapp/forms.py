from django import forms

from mainapp.models import Games
from ordersapp.models import Order, OrderItem


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OrderItemForm(forms.ModelForm):

    price = forms.CharField(label='цена за единицу', required=False)
    quantity_storage = forms.IntegerField(label='Количество на складе', required=False)

    class Meta:
        model = OrderItem
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['product'].queryset = Games.get_items()
