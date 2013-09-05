# Create your views here.

from pymongo import MongoClient
from django.http import HttpResponse
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):

    template_name = "zoomTemplate.html"

    def get_context_data(self, **kwargs):
        db = MongoClient().egarbage
        measures = db.measures
        distintos = measures.distinct("id_device")
        cursores = []
        chartdatas = []
        for ide in distintos:
            cursores.append(measures.find({"id_device": ide}))

        for c in cursores:
            tempdatas = []
            for n in range(c.count()):
                next = c.next()
                chartdata = [float(next['date'].strftime("%s")), next['measure']]
                tempdatas.append(chartdata)
            chartdatas.append(tempdatas)

        print "Distintos: ", distintos
        

        context = super(HomePageView, self).get_context_data(**kwargs)
    
        context['chartdatas'] = chartdatas
        context['chartlabels'] = distintos
        #context['latest_articles'] = Article.objects.all()[:5]
        return context

