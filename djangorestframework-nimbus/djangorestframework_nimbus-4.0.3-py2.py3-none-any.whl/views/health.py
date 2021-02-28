
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.views.generic import View, CreateView, ListView, DetailView, UpdateView
from rest_framework.views import APIView
from rest_framework import status


class HealthCheckerView(View):
    def get(self, *args, **kwargs):
        return HttpResponse("ok", status=status.HTTP_200_OK)
