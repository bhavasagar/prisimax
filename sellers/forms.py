from django import forms

CATEGORY_CHOICES = (
    ('H', 'Handicrafts'),
    ('SS', 'Sarees'),
    ('G', 'Grocery'),
    ('P', 'Daily Needs'),
    ('FW', 'Fashion Wear'),
    ('F', 'Foot Wear'),
    ('FU', 'Furniture'),
    ('MW', 'MensWear'),
    ('BC', 'Beauty Care'),
    ('E', 'Electronics'),
    ('MA', 'Mens Accessories'),
    ('WA', 'Womens Accessories'),
    ('MP', 'Mobiles and Mobile accessories'),
    ('HA', 'Home Appliances'),
    ('S', 'Sports'),
    ('HC', 'Health Care'),
    ('KW', 'Kids Wear'),
    ('B', 'Books'),
    ('AA', 'Auto Accessories'),
    ('J', 'Jewellery')
)


class ItemForm(forms.Form):
    title = forms.CharField(max_length=100)
    price = forms.FloatField()
    category = forms.CharField(widget=forms.Select(
        choices=CATEGORY_CHOICES,
        attrs={
            'class': 'dropdown-toggle form-control'
        }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4,
        'class': 'form-control mb-4',
        'placeholder': 'Describe your product .. '}))
    image = forms.ImageField()
    weight = forms.FloatField(required=True)
    has_size = forms.BooleanField(required=True)
    size = forms.CharField(max_length=100, required=False)
