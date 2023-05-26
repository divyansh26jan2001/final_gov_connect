from django.contrib import admin
from chatbot.models import information,electricity,Jal_Jeevan_Mission, raised_questions

# Register your models here.
class information_admin(admin.ModelAdmin):
    list_display = ('SNo','que','ans')

class electricity_admin(admin.ModelAdmin):
    list_display = ('SNo','que','ans')

class Jal_Jeevan_Mission_admin(admin.ModelAdmin):
    list_display = ('SNo','que','ans')

class raised_questions_admin(admin.ModelAdmin):
    list_display = ('SNo', 'que', 'dept')

admin.site.register(information,information_admin)
admin.site.register(electricity,electricity_admin)
admin.site.register(Jal_Jeevan_Mission,Jal_Jeevan_Mission_admin)
admin.site.register(raised_questions, raised_questions_admin)

