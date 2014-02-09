import datetime
from django import template


register = template.Library()


@register.filter("age")
def age(birthday, from_date=None):
    """
    Use this filter with a users datetime object:
    {{ this_user.profile.birthday|age }}
    """
    if from_date is None:
        from_date = datetime.date.today()

    return (from_date.year - birthday.year) - int((from_date.month, from_date.day) < (birthday.month, birthday.day))