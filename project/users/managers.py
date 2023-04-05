import django.db.models


class UserManager(django.db.models.Manager):
    def get_queryset(self):
        return (
            super(UserManager, self)
            .get_queryset()
            .prefetch_related('profile')
        )
