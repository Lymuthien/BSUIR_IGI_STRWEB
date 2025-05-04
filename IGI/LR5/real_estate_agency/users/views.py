from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import ClientSignUpForm

def signup(request):
    if request.method == 'POST':
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = ClientSignUpForm()

    return render(request, 'signup.html', {'form': form})
