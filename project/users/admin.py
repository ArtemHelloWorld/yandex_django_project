import django.contrib.admin
import django.contrib.auth.models

import users.models

django.contrib.admin.site.register(users.models.User)
