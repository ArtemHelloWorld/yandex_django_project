class BootstrapClassFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control form-control-lg'


class BootstrapPlaceholderFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ignore_placeholder = ['cooking_time']

        for field in self.visible_fields():
            if field.name in ignore_placeholder:
                continue
            field.field.widget.attrs['placeholder'] = field.field.label


class BootstrapSelectClassFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-select form-select-lg'
