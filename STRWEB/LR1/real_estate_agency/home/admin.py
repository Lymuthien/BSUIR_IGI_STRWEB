from django.contrib import admin

from .models import (
    AboutCompany,
    FAQ,
    News,
    Review,
    Contact,
    Vacancy,
    PromoCode,
    Policy,
    Partner,
)

admin.site.register(AboutCompany)
admin.site.register(FAQ)
admin.site.register(News)
admin.site.register(Review)
admin.site.register(Contact)
admin.site.register(Vacancy)
admin.site.register(PromoCode)
admin.site.register(Policy)
admin.site.register(Partner)
