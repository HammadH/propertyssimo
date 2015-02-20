from django.shortcuts import render_to_response
from django.views.generic import View


class Landing(View):
	def get(self, request, *args, **kwargs):
		return render_to_response('landing.html')


