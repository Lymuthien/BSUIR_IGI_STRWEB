from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import ClientSignUpForm

def register(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = ClientSignUpForm()

    return render(request, 'register.html', {'form': form})
