import django.conf
import django.conf.urls.static
import django.contrib.admin
import django.contrib.auth.urls
import django.urls

urlpatterns = [
    django.urls.path('dishes/', django.urls.include('dishes.urls')),
    django.urls.path('users/', django.urls.include('users.urls')),
    django.urls.path('users/', django.urls.include(django.contrib.auth.urls)),
    django.urls.path('taggit/', django.urls.include('taggit_selectize.urls')),
    django.urls.path('tinymce/', django.urls.include('tinymce.urls')),
    django.urls.path('tz_detect/', django.urls.include('tz_detect.urls')),
    django.urls.path('feedback/', django.urls.include('feedback.urls')),
    django.urls.path('admin/', django.contrib.admin.site.urls),
    django.urls.path('', django.urls.include('home.urls')),
]

if django.conf.settings.DEBUG:
    urlpatterns += (
        django.urls.path(
            '__debug__/', django.urls.include('debug_toolbar.urls')
        ),
    )

    urlpatterns += django.conf.urls.static.static(
        django.conf.settings.MEDIA_URL,
        document_root=django.conf.settings.MEDIA_ROOT,
    )
