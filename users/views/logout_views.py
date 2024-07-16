# logout_views.py
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'status': 'success'}, status=200)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)