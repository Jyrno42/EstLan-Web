# coding:utf-8
from django.views.generic.base import TemplateView


class FrontPageView(TemplateView):
    template_name = 'frontpage/frontpage.html'