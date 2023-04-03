import django.conf
import django.conf.urls.static
import django.contrib.admin
import django.urls

urlpatterns = [
    django.urls.path('admin/', django.contrib.admin.site.urls),
]

if django.conf.settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        django.urls.path(
            '__debug__/', django.urls.include(debug_toolbar.urls)
        ),
    )
if django.conf.settings.DEBUG:
    urlpatterns += django.conf.urls.static.static(
        django.conf.settings.MEDIA_URL,
        document_root=django.conf.settings.MEDIA_ROOT,
    )
