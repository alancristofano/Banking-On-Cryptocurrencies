from django import forms
from django.forms import widgets
from crispy_forms.helper import FormHelper


opciones_cryptocompare = (
	('Price', 'Precio'),
	('minprice', 'Precio mínimo'),
	('maxprice','Precio máximo'),
	('vol', 'Vol 24 horas'),
	('change', 'Variación últimas 24h'),

)

tipos_graficas = (
	('GraficaLineal', 'Gráfica lineal de variación de precio'),
	('histogramaVolumen', 'Histograma de variación del volumen')
)


tipos_periodos = (

	('ultimoMes', 'Último mes'),
	('ultimaSemana', 'Última semana'),
	('ultimoDia', 'Último día'),
	('ultimaHora', 'Último hora'),

)

tipo_divisas = (

	('USD','USD ($)'),
	('EUR','EUR (€)'),
	('BTC','BTC (Bitcoin)'),
	('ETH','ETH (Ethereum)'),	
)

class FormRequest(forms.Form):

    moneda = forms.CharField(widget=forms.TextInput(
	attrs={
		'class': 'form-control',
		'placeholder': 'Introduzca una criptomoneda...'

	}
    ))

    


class FormRequest2(forms.Form): 

	variables = forms.MultipleChoiceField(choices=opciones_cryptocompare, required=False, widget=widgets.CheckboxSelectMultiple())

	gráficas = forms.TypedChoiceField(widget=forms.Select, choices=tipos_graficas)

	período = forms.TypedChoiceField(widget=forms.Select, choices=tipos_periodos)

	divisa  = forms.TypedChoiceField(widget=forms.Select, choices=tipo_divisas)
