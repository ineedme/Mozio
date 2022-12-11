from django.contrib import admin
from providers_service_area.models import Provider, ServiceArea


class ProviderAdmin(admin.ModelAdmin):
    pass


class ServiceAreaAdmin(admin.ModelAdmin):
    pass


admin.site.register(Provider, ProviderAdmin)
admin.site.register(ServiceArea, ServiceAreaAdmin)
