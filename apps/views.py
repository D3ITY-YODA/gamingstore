from django.http import JsonResponse
from django.views import View

class HealthCheck(View):
    def get(self, request):
        return JsonResponse({
            "status": "ok", 
            "message": "Django health check",
            "debug": True
        })
