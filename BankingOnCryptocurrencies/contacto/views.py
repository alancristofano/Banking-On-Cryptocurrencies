from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url = '/')
def contact(request):
	if request.method == 'POST':
		print('entra')
		return render(request, 'contacto/contacto.html', {'success':True})
	return render(request, 'contacto/contacto.html', None)
