# Create your views here.

from pymongo import MongoClient
from django.http import HttpResponse
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):

    template_name = "chartTemplate.html"

    def get_context_data(self, **kwargs):
        db = MongoClient().egarbage
        measures = db.measures
        cursor1 = measures.find({"id_device": 4098})
        cursor2 = measures.find({"id_device": 4101})
        measure_list = []
        measure_list2 = []
        for n in range(cursor1.count()):
            next = cursor1.next()
            chartdata = [float(next['date'].strftime("%s")), next['measure']]
            measure_list.append(chartdata)
        print "Match %s results" % len(measure_list)

        for n in range(cursor2.count()):
            next = cursor2.next()
            chartdata = [float(next['date'].strftime("%s")), next['measure']]
            measure_list2.append(chartdata)
        print "Match %s results" % len(measure_list2)


        context = super(HomePageView, self).get_context_data(**kwargs)
        context['chartdata'] = measure_list
        context['chartdata2'] = measure_list2
        #context['latest_articles'] = Article.objects.all()[:5]
        return context

