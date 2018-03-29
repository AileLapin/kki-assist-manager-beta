from django.contrib import admin
# from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin
from account.models import MyUser
from account.forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and chage user instances

    form = UserChangeForm
    add_form = UserCreationForm

    # The fileds to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('stu_num', 'last_name', 'first_name',
                    'nickname', 'is_staff', 'is_superuser',)
    list_filter = ('stu_num',)
    search_fields = ('stu_num', 'last_name', 'first_name', 'nickname')
    fieldsets = (
        (None, {'fields': ('stu_num', 'password')}),
        ('Personal info', {'fields': ('last_name', 'first_name', 'nickname',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)})
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldset to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('stu_num', 'last_name', 'first_name', 'nickname',
                       'password1', 'password2', 'is_staff', 'is_superuser'),
            }),
        )
    ordering = ('stu_num',)


# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)
