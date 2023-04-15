from django import template

register = template.Library()


@register.filter(name='duration_format')
def duration_format(value):
    hours, minutes, _ = str(value).split(':')
    hours = int(hours)
    minutes = int(minutes)

    if hours == 0:
        hours_str = ''
    elif hours == 1:
        hours_str = '1 час '
    elif hours <= 4:
        hours_str = f'{hours} часа '
    else:
        hours_str = f'{hours} часов '

    if minutes == 0:
        minutes_str = ''
    elif minutes == 1:
        minutes_str = '1 минута'
    elif minutes <= 4:
        minutes_str = f'{minutes} минуты'
    else:
        minutes_str = f'{minutes} минут'

    if hours_str and minutes_str:
        return f'{hours_str} и {minutes_str}'
    elif hours_str:
        return hours_str
    else:
        return minutes_str
