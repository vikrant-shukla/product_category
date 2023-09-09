import os
from django.contrib.auth.models import User
import pandas as pd
from django.http import HttpResponse
from rest_framework.views import APIView
from categories_product import settings
from users.tasks import send_delayed_email, send_mail_func
from .serializers import UserSerializer

class ExcelDownloadView(APIView):
    def get(self, request):
        users = User.objects.values("id","username","is_active")
        # users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        df = pd.DataFrame(serializer.data)
        file_path = os.path.join(settings.MEDIA_ROOT,  'sample.xlsx')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_excel(file_path, index=False)
        with open(file_path, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(), content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="sample.xlsx"'

        return response
    
class Send_mail_to_all(APIView):
    def get (self, request):
        email = request.data.get("email")
        send_mail_func.delay(email)
        return HttpResponse("sending mail in background")
    
class Send_mail_after_call(APIView):
    def get (self, request):
        email = request.data.get("email")
        send_delayed_email.apply_async(args = (email,), countdown = 10)
        return HttpResponse("mail will will send in 2 mins")