import json
import requests
import datetime
import pandas as pd
import matplotlib.pyplot as plt



url = 'https://www.cryptocompare.com/api/data/coinlist/'


def price(symbol, comparison_symbols=['USD'], exchange=''):
    url = 'https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms={}'\
            .format(symbol.upper(), ','.join(comparison_symbols).upper())
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()
    simbolo=str(symbol)
    try :
    	print("Precio  "+str(data['RAW'][simbolo]['USD']['PRICE'])+ " dolares.")
    	print("Volumen 24h  "+str(data['RAW'][simbolo]['USD']['VOLUME24HOUR'])+ " dolares.")
    	print("Hight 24h  "+str(data['RAW'][simbolo]['USD']['HIGH24HOUR'])+ " dolares.")
    	print("Low 24h  "+str(data['RAW'][simbolo]['USD']['LOW24HOUR'])+ " dolares.")
    	print("Change 24h  "+str(data['RAW'][simbolo]['USD']['CHANGE24HOUR'])+ " %.")
    	print('\n')
    	
    except:
    	print(str(data['Message']))

def daily_price_historical(symbol, comparison_symbol, limit, aggregate, exchange=''):
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df

def hourly_price_historical(symbol, comparison_symbol, limit, aggregate, exchange=''):
    url = 'https://min-api.cryptocompare.com/data/histohour?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df

def minutly_price_historical(symbol, comparison_symbol, limit, aggregate, exchange=''):
    url = 'https://min-api.cryptocompare.com/data/histominute?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)
    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.datetime.fromtimestamp(d) for d in df.time]
    return df

def daily_volume_historical(symbol, comparison_symbol, limit, aggregate, exchange=''):
    url = 'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&limit={}&aggregate={}'\
            .format(symbol.upper(), comparison_symbol.upper(), limit, aggregate)
    if exchange:
        url += '&e={}'.format(exchange)

    page = requests.get(url)
    data = page.json()['Data']
    df = pd.DataFrame(data)
    df['timestamp'] = [datetime.date.fromtimestamp(d) for d in df.time]

    return df


def exchangesCC(symbol, comparison_symbols):
    url = 'https://www.cryptocompare.com/api/data/coinsnapshot/?fsym={}&tsym={}'\
            .format(symbol.upper(), comparison_symbols.upper())
    page = requests.get(url)
    #print(url)
    mercados=[]
    try:
    	mercados = page.json()['Data']['Exchanges']
    except:
	    print('no hay datos de los exchanges')
	    return
    

    return mercados

def exchangesCC_Analyze(mercados):    
    df = pd.DataFrame(mercados)
    df2=pd.DataFrame()
    df2['nombre'] = [d for d in df.MARKET]
    df2['volumen'] = [float(d) for d in df.VOLUME24HOUR]
    df2['precio'] = [float(d) for d in df.PRICE]
    df2=df2.sort_values(['volumen'],ascending=False)

    return df2
    
def print_exchanges(mercados):
	try:
		print('Los mercados para esta moneda son : ')
		for n in mercados:
			print(str(n['MARKET'])+'  volumen =  '+str(n['VOLUME24HOUR']))
		return
	except:
		pass

#peticion
monedas=requests.get(url)
jmonedas=json.loads(monedas.text)['Data']


print("Introduzca el nombre de la moneda deseada: ")
nombre=input()

print("Los nombres que coinciden con la busqueda son: ")
#Recorre todos los datos del json
#key es el identificador de la moneda
#value son todos los datos de la moneda 
for key,value in jmonedas.items():
	s1=value['FullName']
	#Comparacion con todo en mayusculas
	if nombre.upper() in s1.upper():
		print(s1)
		x = str(key)
		price(x)
		conversor='USD'
		print_exchanges(exchangesCC(x,conversor)) #esto devuelve el json de todos los mercados con sus datos

		print("Que histograma quiere? Ultimo dia(1),Ultima hora(2),30 minutos(3), Ultima semana(4),Ultimo mes(5), Volumen (6), Exchanges (7)")
		hist=int(input())
		if hist==1:
			df = hourly_price_historical(x,conversor,24,1)
			plt.xlabel('Fecha')
			plt.ylabel('Precio')
			plt.title('Histograma diario')
			plt.plot(df.timestamp,df.close)
			plt.xticks(rotation=45)
			plt.show()
		elif hist==2:
			df = minutly_price_historical(x,conversor,60,1)
			plt.xlabel('Fecha')
			plt.ylabel('Precio')
			plt.title('Histograma por horas ')
			plt.plot(df.timestamp,df.close)
			plt.xticks(rotation=45)
			plt.show()
		elif hist==3:
			df = minutly_price_historical(x,conversor,30,1)
			plt.xlabel('Fecha')
			plt.ylabel('Precio')
			plt.title('Histograma por minutos ')
			plt.plot(df.timestamp,df.close)
			plt.xticks(rotation=45)
			plt.show()
		elif hist==4:
			df = daily_price_historical(x,conversor,7,1)
			plt.xlabel('Fecha')
			plt.ylabel('Precio')
			plt.title('Histograma por semanas ')
			plt.plot(df.timestamp,df.close)
			plt.xticks(rotation=45)
			plt.show()
		elif hist==5:
			df = daily_price_historical(x,conversor,31,1)
			plt.xlabel('Fecha')
			plt.ylabel('Precio')
			plt.title('Histograma mes ')
			plt.plot(df.timestamp,df.close)
			plt.xticks(rotation=45)
			plt.show()
		elif hist==6:
			
			df = daily_volume_historical(x,conversor,5,1)
			df.plot.bar('timestamp','volumefrom', color='b') 

			plt.xticks(rotation=45)
			plt.show()
		elif hist==7:
			try:
				df = exchangesCC_Analyze(exchangesCC(x,conversor)) 
				df2= pd.DataFrame() 
				df3= pd.DataFrame() 
				df4= pd.DataFrame(index=['Total'],columns=['nombre','volumen','precio'])
				
				davg = df.volumen.mean()/2
				df2 = df[df.volumen> davg]	
				df3 = df[df.volumen< davg]	
				df4.loc['Total'] = pd.Series(df3['volumen'].sum(), index = ['volumen'])
				df4.loc['Total','nombre'] = 'Otros'
				#df4.loc['Total','precio'] = 0
				df2=df2.append(df4)
				df2 = df2[df2.volumen>1]
				#print(str(df2))
				df2.plot(kind='pie',y = 'volumen', figsize=(20, 20),autopct='%0.2f%%',colors=['b', 'g', 'r', 'c', 'm', 'y', 'w'] ,labels=df2['nombre'],labeldistance= 1.05 ,startangle=0, shadow=False, legend = False, fontsize=30)
				plt.xlabel('')
				plt.ylabel('')
				plt.title(str(s1),fontsize=55)
				#plt.savefig("/home/dani/Escritorio/" + "foto" + ".png")
				plt.show()
			except:
				pass
			









