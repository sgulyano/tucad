import time

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.views.generic.detail import DetailView
from django.http import HttpResponse
from django.urls import reverse

from .forms import ChestXrayForm
from .models import ChestXray
from django.conf import settings

import os
import shutil
import sys
import json

# from cxrnet.pred_one import find_pred_one, show_pred_one

class Upload(View):
    def get(self, request):
        print("aa")
        print(request)
        print(request.is_ajax())
        print(request.method)
        return render(self.request, 'cxr/index.html', {})

    def post(self, request):
        form = ChestXrayForm(self.request.POST, self.request.FILES)
        print("bb")
        print(request.is_ajax())
        print(request.method)
        print(form.is_valid())
        if form.is_valid():
            xrimg = form.save()
            analyse_url = reverse('cxr:analysis', args=(xrimg.pk,))
            #print (hoho)
            #import pdb; pdb.set_trace()
            data = {'is_valid': True, 'name': xrimg.file.name, 
                    'url': xrimg.file.url, 'id': xrimg.pk, 
                    'analyse_url': analyse_url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

class Analysis(DetailView):
    model = ChestXray
    template_name = 'cxr/analysis.html'
    def get_object(self, queryset=None):
        obj = super(Analysis, self).get_object(queryset=queryset)
        obj.description = 'Chest X-ray Image'
        img_path = os.path.join(settings.BASE_DIR, obj.file.url[1:])
        print(img_path)
        # [preds, cxr, img_tensor, model] = find_pred_one(img_path)
        # fn = show_pred_one(preds, cxr, img_tensor, model, 0, settings.MEDIA_ROOT)
        
        # pred_dict = dict(zip(preds.index.tolist(), preds['Predicted Probability'].tolist()))
        # obj.preds = json.dumps(pred_dict)
        # obj.heatmap = os.path.join(settings.MEDIA_URL, fn)
        return obj

class SystemView(View):
    def get(self, request):
        xrimgs_list = ChestXray.objects.all()
        return render(self.request, 'cxr/systemview.html', {'xrimgs': xrimgs_list})

def clear_database(request):
    for img in ChestXray.objects.all():
        img.file.delete()
        img.delete()
    return redirect(request.POST.get('next'))
