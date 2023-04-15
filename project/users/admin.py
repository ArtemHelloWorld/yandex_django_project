import django.contrib.admin
import django.contrib.auth.admin
import django.contrib.auth.models

import users.models


class UsersProfileInline(django.contrib.admin.TabularInline):
    model = users.models.Profile
    can_delete = False


class UserAdmin(django.contrib.auth.admin.UserAdmin):
    inlines = (UsersProfileInline,)


django.contrib.admin.site.unregister(django.contrib.auth.models.User)
django.contrib.admin.site.register(django.contrib.auth.models.User, UserAdmin)
