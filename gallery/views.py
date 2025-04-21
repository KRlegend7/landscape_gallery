from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Landscape

class CSVImportView(LoginRequiredMixin, View):
    template_name = 'gallery/upload.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # We'll implement this later
        return render(request, self.template_name)

class LandscapeListView(LoginRequiredMixin, View):
    template_name = 'gallery/list.html'

    def get(self, request):
        landscapes = Landscape.objects.all()
        return render(request, self.template_name, {'landscapes': landscapes})