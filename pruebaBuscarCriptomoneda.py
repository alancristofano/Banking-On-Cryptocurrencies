import json
import requests



url = 'https://www.cryptocompare.com/api/data/coinlist/'

#peticion
monedas=requests.get(url)
jmonedas=json.loads(monedas.text)['Data']#['LTC']['FullName']
#imprime todos los datos del json
#print(str(jmonedas))

print("Introduzca el nombre de la moneda deseada: ")
nombre=input()

print("Los nombres que coinciden con la busqueda son: ")
#Recorre todos los datos del json
#key es el identificador de la moneda
#value son todos los datos de la moneda 
for key,value in jmonedas.items():
	#print ("value =   "+str(value['FullName']))
	s1=value['FullName']
	#print(s1)
	#Comparacion con todo en mayusculas
	if nombre.upper() in s1.upper():
		print(s1)
