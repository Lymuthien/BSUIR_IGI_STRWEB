import calendar
import logging

from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView
from home.models import Review

from .forms import ClientSignUpForm
from .models import Profile, Client, Employee
from .utils.timezone_service import TimezoneService

logger = logging.getLogger(__name__)


class SignUpView(CreateView):
    form_class = ClientSignUpForm
    template_name = "signup.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        logger.debug(
            f"Validating form for user signup: {form.cleaned_data.get('username')}"
        )
        try:
            response = super().form_valid(form)
            user = self.object
            login(self.request, user)
            logger.info(
                f"User {user.username} (role: {user.role}) registered and logged in successfully"
            )
            return response
        except Exception:
            logger.exception(
                f"Error during user signup for {form.cleaned_data.get('username')}"
            )
            raise

    def form_invalid(self, form):
        logger.warning(f"Invalid form submission for user signup: {form.errors}")
        return super().form_invalid(form)


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profile-detail.html"

    @staticmethod
    def _format_date(dt, tz, format_str="%d/%m/%Y %H:%M:%S"):
        return dt.astimezone(tz).strftime(format_str) if dt else ""

    def _get_reviews_with_dates(self, reviews, user_timezone):
        return [
            {
                "review": review,
                "created_local": self._format_date(review.created_at, user_timezone),
                "created_utc": review.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                "updated_local": self._format_date(review.updated_at, user_timezone),
                "updated_utc": review.updated_at.strftime("%d/%m/%Y %H:%M:%S"),
            }
            for review in reviews
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.object
        user = profile.user
        logger.debug(f"Loading profile for user: {user.username}, ID: {user.id}")

        reviews = Review.objects.filter(user=user).order_by("-created_at")
        context["is_client"] = Client.objects.filter(user=user).exists()
        context["is_employee"] = Employee.objects.filter(user=user).exists()
        logger.debug(
            f"User {user.username} is_client: {context['is_client']}, is_employee: {context['is_employee']}"
        )

        try:
            user_timezone = TimezoneService.get_timezone(self.request)
            logger.info(
                f"Timezone determined for user {user.username}: {user_timezone}"
            )
        except Exception as e:
            user_timezone = timezone.get_default_timezone()
            logger.error(
                f"Failed to determine timezone for user {user.username}: {str(e)}, defaulting to {user_timezone}"
            )

        utc_now = timezone.now()
        local_now = utc_now.astimezone(user_timezone)
        logger.debug(f"UTC time: {utc_now}, Local time ({user_timezone}): {local_now}")

        utc_created = user.created_at
        local_created = utc_created.astimezone(user_timezone)

        text_calendar = calendar.TextCalendar()
        month_calendar = text_calendar.formatmonth(local_now.year, local_now.month)
        logger.debug(f"Generated calendar for {local_now.strftime('%B %Y')}")

        reviews_with_dates = self._get_reviews_with_dates(reviews, user_timezone)
        logger.debug(
            f"Processed {len(reviews_with_dates)} reviews for user {user.username}"
        )

        context.update(
            {
                "utc_date": utc_now.strftime("%d/%m/%Y"),
                "local_date": local_now.strftime("%d/%m/%Y"),
                "utc_created": utc_created.strftime("%d/%m/%Y %H:%M:%S"),
                "local_created": local_created.strftime("%d/%m/%Y %H:%M:%S"),
                "user_timezone": user_timezone,
                "calendar": month_calendar,
                "reviews": reviews_with_dates,
            }
        )

        return context
