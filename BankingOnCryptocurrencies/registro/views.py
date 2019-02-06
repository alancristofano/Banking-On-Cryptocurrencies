from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from . import forms

# Create your views here.


@login_required(login_url = '/registro/signin')
def signout(request):
	logout(request)
	return HttpResponseRedirect('/')

def signin(request):
	logged = False
	form = forms.UserForm()
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				logged = True
				return HttpResponseRedirect('/query')
			else:
				return HttpResponse("Cuenta inactiva")
		else :
			return render (request,'registro/signin.html',{'Error':True})	
		
	return render(request, 'registro/signin.html', {'form':form})

def registro(request):
	registered = False
	if request.method == 'POST':
			user_form = forms.UserForm(data=request.POST)

			if user_form.is_valid():
				user_form.save()
				registered = True
				return render(request, 'registro/register.html', {'user_form': user_form, 'registered': registered})
				
			else:
				if user_form.cleaned_data.get('password1') != user_form.cleaned_data.get('password2'):
					return render(request, 'registro/register.html', {'user_form': user_form,'contrasena':True})
				else:
					return render(request, 'registro/register.html', {'user_form': user_form,'usuario':True})
	user_form = forms.UserForm()
	return render(request, 'registro/register.html', {'user_form': user_form})

