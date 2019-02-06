from django.shortcuts import render
from . import forms
import json
import requests
import datetime
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.contrib.auth.decorators import login_required



# Create your views here.



def coin_data(symbol, comparison_symbols):
    url = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}'\
            .format(symbol.upper(), comparison_symbols.upper())
    
    page = requests.get(url)
    data = page.json()
    try:
    	return data['RAW'][symbol][comparison_symbols]
    except:
    	return data


def data_historical(symbol, comparison_symbol, limit, moment): #dia = day hora=hour minuto=minute
    url = 'https://min-api.cryptocompare.com/data/histo{}?fsym={}&tsym={}&limit={}'\
            .format(moment , symbol.upper(), comparison_symbol.upper(), limit)

    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['Hora'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    df['Fecha'] = [datetime.date.fromtimestamp(d) for d in df.time]

    return df


def exchangesCC(symbol, comparison_symbols):
    url = 'https://www.cryptocompare.com/api/data/coinsnapshot/?fsym={}&tsym={}'\
            .format(symbol.upper(), comparison_symbols.upper())
    page = requests.get(url)
    mercados = page.json()
    return mercados


def exchangesCC_Analyze(mercados):    
    df = pd.DataFrame(mercados)
    df2=pd.DataFrame()
    df2['nombre'] = [d for d in df.MARKET]
    df2['volumen'] = [float(d) for d in df.VOLUME24HOUR]
    df2['precio'] = [float(d) for d in df.PRICE]
    df2=df2.sort_values(['volumen'],ascending=False)

    return df2



@login_required(login_url = '/')
def search(request):
	
	form = forms.FormRequest()
	if request.method == 'POST':
		form = forms.FormRequest(request.POST)
		if form.is_valid():
			
			#Recojemos el dato del formulario
			moneda = form.cleaned_data['moneda']
			#Preparamos los datos de la petición
			url = 'https://www.cryptocompare.com/api/data/coinlist/'
			#Enviamos la petición
			monedas=requests.get(url)
			#Obtenemos la respuesta y leemos el json
			jmonedas=json.loads(monedas.text)['Data']
			
			#Recorre todos los datos del json
			#key es el identificador de la moneda	
			#value son todos los datos de la moneda 
			coin_list = []
			for key,value in jmonedas.items():
				fullname=value['FullName']
				name=key
				#Comparacion con todo en mayusculas
				if moneda.upper() in fullname.upper():
					coin_list.append([fullname,name])
			
			context={'coin_list':coin_list}
			return render(request, 'consulta/coin_list.html', context)
	return render(request, 'consulta/search.html', {'form': form})

@login_required(login_url = '/')
def coin_selected (request, coin_id):

	
	form = forms.FormRequest2()
	url = 'https://www.cryptocompare.com/api/data/coinlist/'
	monedas=requests.get(url)
	imagen =json.loads(monedas.text)['Data'][coin_id]['ImageUrl']
	nombre =json.loads(monedas.text)['Data'][coin_id]['CoinName']
	
	context={'coin_id': coin_id, 'coin_form': form, 'imagen': imagen, 'nombre': nombre }
		
	return render(request, 'consulta/coin_detail.html', context )

@login_required(login_url = '/')
def result (request, coin_id):
	
	form = forms.FormRequest2(request.POST)
	if form.is_valid():
	# Recojemos los datos del formulario
		variables_seleccionadas = form.cleaned_data['variables']
		variables = ",".join(str(e) for e in variables_seleccionadas)

		grafica = form.cleaned_data['gráficas']
		periodo = form.cleaned_data['período']
		divisa = form.cleaned_data['divisa']

		# Envíamos la petición
		data = coin_data(coin_id, divisa)		
		try:			
			price = ''
			minprice = ''
			maxprice = ''
			vol = ''
			change = ''
					
			
			if 'Price' in variables: 
				price = data['PRICE']
			if 'minprice' in variables:
				minprice = data['LOW24HOUR']
			if 'maxprice' in variables: 
				maxprice = data['HIGH24HOUR']
			if 'vol' in variables: 
				vol = data['VOLUME24HOUR']
			if 'change' in variables:
				change = data['CHANGE24HOUR']

			
			'''
			########################################################
					Gráficas lineales
			########################################################
			'''

			
			ruta = "/app/consulta/static/consulta/imagenes/grafica.png"

			if (grafica == 'GraficaLineal' and periodo == 'ultimaHora'):
				df=data_historical(coin_id, divisa , 60, 'minute')
				df.plot('Hora', 'close',legend=False,figsize=(9,5.2))	
				plt.title('Variación de precio de la última hora en ' + str(divisa),fontsize=16)			
				plt.savefig(ruta)
				plt.close()
				
			elif (grafica == 'GraficaLineal' and periodo == 'ultimaSemana'):
				df=data_historical(coin_id, divisa , 7, 'day')
				df.plot('Fecha', 'close',legend=False,figsize=(9,4))	
				plt.title('Variación de precio de la última semana en ' + str(divisa),fontsize=16)			
				plt.savefig(ruta)
				plt.close()
				

			elif (grafica == 'GraficaLineal' and periodo == 'ultimoDia'):
				df=data_historical(coin_id, divisa , 24, 'hour')
				df.plot('Hora', 'close',legend=False,figsize=(9,5.2))	
				plt.title('Variación de precio del último día en ' + str(divisa),fontsize=16)			
				plt.savefig(ruta)
				plt.close()
				

			elif (grafica == 'GraficaLineal' and periodo == 'ultimoMes'):
				df=data_historical(coin_id, divisa , 30, 'day')
				df.plot('Fecha', 'close',legend=False,figsize=(9,4))	
				plt.title('Variación de precio del último mes en ' + str(divisa),fontsize=16)				
				plt.savefig(ruta)
				plt.close()

			
			'''
			########################################################
					Histogramas
			########################################################
			'''

			if (grafica == 'histogramaVolumen' and periodo == 'ultimoMes'):
				df=data_historical(coin_id, divisa , 30, 'day')
				plt.xticks(rotation=25)
				df.plot.bar('Fecha', 'volumefrom', color='b', legend=False, figsize=(12,6))
				plt.title('Variación del volumen del último mes en '+ str(divisa),fontsize=16)
				plt.xticks(size= 'small',rotation=45)			
				plt.savefig(ruta)
				plt.close()


			
			if (grafica == 'histogramaVolumen' and periodo == 'ultimaSemana'):
				df=data_historical(coin_id, divisa , 7, 'day')
				df.plot.bar('Fecha', 'volumefrom', color='b', legend=False, figsize=(12,6))	
				plt.title('Variación del volumen de la última semana en '+ str(divisa),fontsize=16)
				plt.xticks(rotation=0)			
				plt.savefig(ruta)
				plt.close()


			
			if (grafica == 'histogramaVolumen' and periodo == 'ultimoDia'):
				df=data_historical(coin_id, divisa , 24, 'hour')
				df.plot.bar('Hora', 'volumefrom', color='b', legend=False, figsize=(12,6))
				plt.title('Variación del volumen del último día en '+ str(divisa),fontsize=16)			
				plt.xticks(size = 'small')						
				plt.savefig(ruta)
				plt.close()


			
			
			if (grafica == 'histogramaVolumen' and periodo == 'ultimaHora'):
				df=data_historical(coin_id, divisa , 60, 'minute')
				df.plot.bar('Hora', 'volumefrom', color='b', legend=False, figsize=(12,6))			
				plt.title('Variación del volumen de la última hora en '+ str(divisa),fontsize=16)
				plt.xticks(size= 'small')
				plt.savefig(ruta)
				plt.close()

			try:
				mercados = exchangesCC(coin_id,divisa)['Data']['Exchanges']
				'''
				########################################################
						Gráfica Circular
				########################################################
				'''

				ruta2 = "/app/consulta/static/consulta/imagenes/grafica2.png"
				dfe = exchangesCC_Analyze(mercados) 
				dfe2= pd.DataFrame() 
				dfe3= pd.DataFrame() 
				dfe4= pd.DataFrame(index=['otros'],columns=['nombre','volumen','precio'])
				
				davg = dfe.volumen.mean()
				dfe2 = dfe[dfe.volumen> davg]	
				mercados2 = dfe2.values.tolist()
				dfe3 = dfe[dfe.volumen< davg]	
				dfe4.loc['otros'] = pd.Series(dfe3['volumen'].sum(), index = ['volumen'])
				dfe4.loc['otros','nombre'] = 'Otros'
				dfe4.loc['otros','precio'] = dfe3['precio'].sum()
				dfe2=dfe2.append(dfe4)
				dfe2 = dfe2[dfe2.volumen>1]
				#print(str(dfe2))
				dfe2.plot(kind='pie',y = 'volumen', figsize=(7, 7),colors=['tab:green', 'b','tab:orange', 'y', 'c','0.7', 'tab:brown', 'tab:red', 'k','tab:pink'] ,labels=dfe2['nombre'],labeldistance= 1.05 ,startangle=0, shadow=False, legend = False, fontsize=10)
				plt.xlabel('')
				plt.ylabel('')
				plt.title("Volumen por mercado en "+str(divisa),fontsize=16)
				plt.savefig(ruta2)
				plt.close()
			except:
				
				context={ 'coin_id': coin_id, 'price': price, 'minprice': minprice, 'maxprice': maxprice, 'vol': vol, 'change': change, 'divisa': divisa , 'grafica': grafica}
				return render(request, 'consulta/without_market.html', context )

							
			context={ 'coin_id': coin_id, 'price': price, 'minprice': minprice, 'maxprice': maxprice, 'vol': vol, 'change': change, 'divisa': divisa , 'grafica': grafica, 'periodo': periodo, 'mercados': mercados2}
			
			return render(request, 'consulta/result.html', context )
		except:
			
			return render(request, 'consulta/no_data.html', None )
	
	

	
	 
	
