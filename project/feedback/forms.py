import core.forms
import feedback.models


class FeedbackForm(core.forms.BootstrapForm):
    class Meta:
        model = feedback.models.Feedback
        fields = (
            feedback.models.Feedback.text.field.name,
            feedback.models.Feedback.mail.field.name,
        )
        labels = {
            feedback.models.Feedback.text.field.name: "Введите Ваше сообщение",
            feedback.models.Feedback.mail.field.name: "Введите Вашу почту",
        }
