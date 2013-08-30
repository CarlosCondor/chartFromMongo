# Create your views here.

from pymongo import MongoClient
from django.http import HttpResponse
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):

    template_name = "chartTemplate.html"

    def get_context_data(self, **kwargs):
        db = MongoClient('localhost', 27017).egarbage

        context = super(HomePageView, self).get_context_data(**kwargs)

        #context['latest_articles'] = Article.objects.all()[:5]
        return context

