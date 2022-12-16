from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Account
# Register your models here.

class AccountAdmin(UserAdmin):
    # form = UserChangeForm
    # add_form = UserCreationForm
    model = Account
    list_display =  ('email', 'username', 'first_name', 'last_name','phone_number', 'date_joined', 'is_active', 'is_superuser')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined', )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        # (('Permissions'), {
        #     'fields': ('is_active', 'is_user', '', 'groups'),
        # }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'phone_number'),
        }),
        (('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone_number')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(Account, AccountAdmin)
# admin.site.register(Account)

