from django.forms import ModelForm
from .models import Residency,Room_details,Room_type
from django import forms

Aminties = [
        ('AC', 'AC'),  
        ('Heating', 'Heating'),
        ('Wi-Fi', 'Wi-Fi'),
        ('Television', 'Television'),
        ('Refrigerator', 'Refrigerator'),
        ('Microwave', 'Microwave'),
        ('Balcony', 'Balcony'),
        ('Private Bathroom', 'Private Bathroom'),
        ('Parking', 'Parking'),
        ('Kitchenette', 'Kitchenette'),
        ('Swimming Pool Access', 'Swimming Pool Access'),
        ('Gym Access', 'Gym Access'),
        ('Room Service', 'Room Service'),
    ]


class ResidencyForm(ModelForm):
    class Meta:
        model=Residency
        exclude=("created_by",)

class CreateRoomTypeForm(ModelForm):
    class Meta:
        model = Room_type
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            self.fields['residency'].queryset = Residency.objects.filter(created_by=user)
        else:
            self.fields['residency'].queryset = Residency.objects.none()  

class Create_Room_forms(ModelForm):
    key_features=forms.MultipleChoiceField(choices=Aminties,widget=forms.CheckboxSelectMultiple)
    class Meta:
        model=Room_details
        exclude=("key_features",'no_new','disable',)
    def __init__(self,*args,**kwargs):
        user=kwargs.pop("user",None)
        super().__init__(*args,**kwargs)
        if user:
            self.fields['residency'].queryset=Residency.objects.filter(created_by=user)
            self.fields['room_type'].queryset=Room_type.objects.filter(residency__created_by=user)
        else:
            self.fields['residency'].queryset=Residency.objects.none()
            self.fields['room_type'].queryset=Room_type.objects.none()

        
class SearchForm(forms.Form):
    search=forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class":"form-control",
                "placeholder":"search residency Here.."
            }
        )
    )

sort_choice=[
    ('HTL',"High To low"),
    ("LTH","Low To HIgh")
    ]

class filterpriceForm(forms.Form):
    options=forms.ChoiceField(
        choices=sort_choice,
        widget=forms.RadioSelect(attrs={"id":"sort-price"}),
        label="Sort Price"
        )
    
    # def __init__(self, maxprice, minprice,*args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['range_field'] = forms.IntegerField(
    #         widget=forms.NumberInput(attrs={
    #             'type': 'range',
    #             'min': minprice,
    #             'max': maxprice,
    #             'step': '500',
    #             'value': '5000',
    #             'id': 'range-slider',
    #         }),
    #         label="Filter by Price Range"
    #     )