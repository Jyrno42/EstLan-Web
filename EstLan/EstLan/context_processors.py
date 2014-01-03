from django.conf import settings
from django.utils.translation import ugettext_lazy as _


def seo_tags(request):
    return {
        'meta_description': _(
            "EstLan Digital Festival is a series of charitable LAN Parties "
            "which helps the children in need in our local area which is Estonia, "
            "therefore the name Est(onian)Lan. With the big help of our sponsors "
            "we're trying to make a real difference in the Baltic gaming scene. "
            "Gaming for good - EstLan."),
        'meta_keywords': _(
            "lanparty, gaming, charity, digital, festival, gathering, "
            "league, legends, dota, cs, estlan, estonia, boomcasters"
        ),
        'SITE_NAME': settings.SITE_NAME,
        'SITE_VERSION': settings.SITE_VERSION,
    }
