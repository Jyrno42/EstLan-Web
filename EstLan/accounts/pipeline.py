from time import strptime, mktime
from datetime import datetime
from accounts.models import EstLanUser


def user_details(strategy, details, response, user=None, *args, **kwargs):
    """Update user details using data from provider."""

    if user:
        if kwargs['is_new']:
            gender = EstLanUser.GENDER_MALE
            date_of_birth = None

            if strategy.backend.__class__.__name__ == 'FacebookOAuth2':
                gender = response['gender']

                print response['birthday']

                date_of_birth = datetime.fromtimestamp(mktime(strptime(response['birthday'], '%m/%d/%Y')))

            changed = False
            if user.gender != gender:
                user.gender = gender
                changed = True

            if user.date_of_birth != date_of_birth:
                user.date_of_birth = date_of_birth
                changed = True

            if changed:
                user.save()