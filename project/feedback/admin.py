from django.contrib import admin

import feedback.models


@admin.register(feedback.models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.text.field.name,
        feedback.models.Feedback.mail.field.name,
    )
