from django.contrib import admin, messages
from django import forms
from .models import CustomUser

admin.site.site_header = "Volingual Admin Dashboard"
admin.site.site_title = "Volingual Admin Portal"
admin.site.index_title = "Welcome to the Volingual Admin Portal"


class MyAdminSite(admin.AdminSite):
    class Media:
        css = {
           'all': ('css/admin.css',)
        }


admin_site = MyAdminSite()


class CountryFilter(admin.SimpleListFilter):
    title = 'country'  # Human-readable title which will be displayed in the right admin sidebar just above the filter options.
    parameter_name = 'country'  # Parameter for the filter that will be used in the URL query.

    def lookups(self, request, model_admin):
        countries = set([c.country for c in model_admin.model.objects.all()])
        return [(c, c) for c in countries]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(country__iexact=self.value())
        else:
            return queryset


class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if "example.com" in email:
            raise forms.ValidationError("Email addresses from example.com are not allowed.")
        return email


class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserAdminForm
    list_display = ('email', 'first_name', 'last_name', 'country', 'is_active', 'is_staff')
    list_filter = (CountryFilter, 'is_staff', 'is_active',)
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    actions = ['make_inactive', 'make_active']

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected users have been deactivated.", messages.SUCCESS)

    make_inactive.short_description = "Deactivate selected users"

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected users have been activated.", messages.SUCCESS)

    make_active.short_description = "Activate selected users"


admin.site.register(CustomUser, CustomUserAdmin)
