import calendar

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import CreateView, DetailView

from .forms import ClientSignUpForm
from .models import Profile
from .services.timezone_service import TimezoneService
from home.models import Review


class SignUpView(CreateView):
    form_class = ClientSignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return response


class ProfileView(DetailView):
    model = Profile
    template_name = 'profile-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        user = profile.user

        reviews = Review.objects.filter(user=user).order_by('-created_at')

        user_timezone = TimezoneService.get_timezone(self.request)
        utc_now = timezone.now()
        local_now = utc_now.astimezone(user_timezone)

        utc_created = user.created_at
        local_created = utc_created.astimezone(user_timezone)

        text_calendar = calendar.TextCalendar()
        month_calendar = text_calendar.formatmonth(local_now.year, local_now.month)

        reviews_with_dates = []
        for review in reviews:
            reviews_with_dates.append({
                'review': review,
                'created_local': review.created_at.astimezone(user_timezone).strftime('%d/%m/%Y %H:%M:%S'),
                'created_utc': review.created_at.strftime('%d/%m/%Y %H:%M:%S'),
                'updated_local': review.updated_at.astimezone(user_timezone).strftime('%d/%m/%Y %H:%M:%S'),
                'updated_utc': review.updated_at.strftime('%d/%m/%Y %H:%M:%S'),
            })

        context.update({
            'utc_date': utc_now.strftime('%d/%m/%Y'),
            'local_date': local_now.strftime('%d/%m/%Y'),
            'utc_created': utc_created.strftime('%d/%m/%Y %H:%M:%S'),
            'local_created': local_created.strftime('%d/%m/%Y %H:%M:%S'),
            'user_timezone': user_timezone,
            'calendar': month_calendar,
            'reviews': reviews_with_dates,
        })

        return context
