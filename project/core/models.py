import re
import django.db.models
import transliterate


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


class NormalizedNameFieldMixin(django.db.models.Model):
    name_normalized = django.db.models.CharField(
        max_length=200,
    )

    def save(self, *args, **kwargs):
        self.name_normalized = self._generate_normalize_name()
        super().save(*args, **kwargs)

    def _generate_normalize_name(self):
        normalized = self.name.lower()
        normalized = re.sub(r'\W', '', normalized)
        normalized = transliterate.translit(normalized, 'ru', reversed=True)

        return normalized

    class Meta:
        abstract = True

