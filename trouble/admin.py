from django.contrib import admin
from .models import TroubleUser, TroubleCategory, Trouble


admin.site.register(Trouble)
admin.site.register(TroubleCategory)
admin.site.register(TroubleUser)
