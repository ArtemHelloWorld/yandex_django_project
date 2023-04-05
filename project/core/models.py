import django.db.models


class IntegerRangeField(django.db.models.IntegerField):
    def __init__(
        self,
        verbose_name=None,
        name=None,
        min_value=None,
        max_value=None,
        **kwargs
    ):
        self.min_value = min_value
        self.max_value = max_value
        django.db.models.IntegerField.__init__(
            self, verbose_name, name, **kwargs
        )

    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value': self.max_value}
        defaults.update(kwargs)

        return super(IntegerRangeField, self).formfield(**defaults)


class NameFieldMixin(django.db.models.Model):
    name = django.db.models.CharField(
        max_length=100,
        verbose_name='название',
        help_text='Укажите название. Максимум 100 символов',
    )

    class Meta:
        abstract = True
