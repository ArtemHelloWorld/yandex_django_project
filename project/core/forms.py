class BootstrapClassAndPlaceholderFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control form-control-lg'
            field.field.widget.attrs['placeholder'] = field.field.label
