from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Question_attempt)
admin.site.register(Quiz_attempt)
