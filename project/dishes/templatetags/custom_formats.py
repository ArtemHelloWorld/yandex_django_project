from django import template
import pymorphy2


register = template.Library()

hour_word = pymorphy2.MorphAnalyzer().parse('час')[0]
minute_word = pymorphy2.MorphAnalyzer().parse('минута')[0]


@register.filter(name='duration_format')
def duration_format(value):
    hours, minutes, _ = str(value).split(':')
    hours = int(hours)
    minutes = int(minutes)

    if hours and minutes:
        return (
            f'{hours} {hour_word.make_agree_with_number(hours).word} и '
            f'{minutes} {minute_word.make_agree_with_number(minutes).word}'
        )
    elif hours:
        return f'{hours} {hour_word.make_agree_with_number(hours).word}'
    else:
        return f'{minutes} {minute_word.make_agree_with_number(minutes).word}'
