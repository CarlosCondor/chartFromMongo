# Create your views here.

from pymongo import MongoClient
from django.http import HttpResponse
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):

    template_name = "chartTemplate.html"

    def get_context_data(self, **kwargs):
        db = MongoClient().egarbage
        measures = db.measures
        cursor = measures.find()
        measure_list = []
        for n in range(cursor.count()):
            next = cursor.next()

            chartdata = [float(next['date'].strftime("%s")+"000"), next['measure']]
            measure_list.append(chartdata)
        print "Match %s results" % len(measure_list)


        context = super(HomePageView, self).get_context_data(**kwargs)
        context['chartdata'] = measure_list
        #context['latest_articles'] = Article.objects.all()[:5]
        return context

