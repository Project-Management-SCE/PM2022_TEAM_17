from django.contrib import admin
from .models import Agent, Customer
from .models import Customer
# Register your models here.

#admin.site.register(Agent)
admin.site.register(Customer)

class AgentAdmin(admin.ModelAdmin):
    list_display = ('emp_ID','full_name','email', 'city','Mobile', 'isAgent')
    list_filter = ['isAgent']

    # def get_queryset(self, request):
    #     qs = super(AgentAdmin, self).get_queryset(request)
    #     return qs.filter(isAgent='False')
        
admin.site.register(Agent, AgentAdmin)