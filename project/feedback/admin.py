import django.contrib.admin

import feedback.models


@django.contrib.admin.register(feedback.models.Feedback)
class FeedbackAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.created_on.field.name,
        feedback.models.Feedback.text.field.name,
        feedback.models.Feedback.status.field.name,
    )
    list_editable = (feedback.models.Feedback.status.field.name,)
