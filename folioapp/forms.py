from django import forms

class calculoCredito(forms.Form):
    monto = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Monto sin puntos'}))
    plazo = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Plazo de su crédito'}))
    tasa = forms.DecimalField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese Tasa de interes Anual de su Crédito'}))


class subirArchivo(forms.Form):
    file = forms.FileField()