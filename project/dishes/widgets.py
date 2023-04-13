from django.forms.widgets import MultiWidget, NumberInput


class DurationWidget(MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            NumberInput(
                attrs={
                    'class': 'form-control col-4',
                    'min': 0,
                    'placeholder': 'Часы'
                }),
            NumberInput(
                attrs={
                    'class': 'form-control col-4',
                    'min': 0,
                    'max': 59,
                    'placeholder': 'Минуты'
                }),
        ]
        super().__init__(widgets, attrs=attrs)

    def decompress(self, value):
        if value:
            value = int(value)
            hours = value // 3600
            minutes = value // 60 % 60
            return [hours, minutes]
        return [None, None]

    def value_from_datadict(self, data, files, name):
        hours, minutes = super().value_from_datadict(data, files, name)

        if hours is None or minutes is None:
            return None
        return int(hours) * 3600 + int(minutes) * 60
