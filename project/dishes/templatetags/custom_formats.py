from django import template
import pymorphy2


register = template.Library()

hour_word = pymorphy2.MorphAnalyzer().parse('час')[0]
minute_word = pymorphy2.MorphAnalyzer().parse('минута')[0]


@register.filter(name='duration_format_time')
def duration_format_time(value):
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


@register.filter(name='duration_format_ingredient')
def duration_format_ingredient(value):
    quantity = value.quantity
    type = value.get_quantity_type_display()
    case_type = (pymorphy2.MorphAnalyzer().
                 parse(type)[0].make_agree_with_number(quantity).word)

    return f'{quantity}  {case_type}'
