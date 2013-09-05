# Create your views here.

from pymongo import MongoClient
from django.http import HttpResponse
from django.views.generic.base import TemplateView
import datetime

class HomePageView(TemplateView):

    template_name = "zoomTemplate.html"

    def get_context_data(self, **kwargs):
        db = MongoClient().egarbage
        measures = db.measures
        distintos = measures.distinct("id_device")
        cursores = []
        chartdatas = []
        syncerrors = []
        synctime = 0
        lastsync = 0
        for ide in distintos:
            cursores.append(measures.find({"id_device": ide}))
        ccc=0
        for c in cursores:
            tempdatas = []
            for n in range(c.count()):
                next = c.next()
                chartdata = [float(next['date'].strftime("%s")), next['measure']]
                tempdatas.append(chartdata)

            if (float(datetime.datetime.now().strftime("%s"))-tempdatas[-1][0]) > 10*60:
                syncerrors.append("%s no sincroniza desde %s" % (distintos[ccc], datetime.datetime.fromtimestamp(float(tempdatas[-1][0]))))
            
            i=0
            while synctime < 5 or i < 5:
                synctime = tempdatas[-1][0]-tempdatas[-i][0]
                lastsync = tempdatas[-1][0]
                print "synctime: ", synctime
                i+=1

            print tempdatas[-1]
            chartdatas.append(tempdatas)
            ccc+=1

        print "Distintos: ", distintos
        print syncerrors
        

        context = super(HomePageView, self).get_context_data(**kwargs)
    
        context['chartdatas'] = chartdatas
        context['chartlabels'] = distintos
        context['syncerrors'] = syncerrors
        context['synctime'] = synctime
        context['lastsync'] = lastsync
        #context['latest_articles'] = Article.objects.all()[:5]
        return context

