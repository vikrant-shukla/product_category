import os
from django.contrib.auth.models import User
import pandas as pd
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView
from categories_product import settings
from users.tasks import send_delayed_email, send_mail_func
from .serializers import UserSerializer
    
class ExcelDownloadView(APIView):
    """Extration of data from User table and dump excel file for three colunms
      "id","full_name" ( "first_name", "last_name"), "is_active")"""
    
    def get(self, request):
        users = User.objects.values("id", "first_name", "last_name", "is_active")
        if not users:
            data =  {"Message":"No User is present, Please run the user creation script by running 'python3 manage.py create_users'"}
            return Response(data)
        full_names = [f"{user['first_name']} {user['last_name']}" for user in users]
        serializer = UserSerializer(users, many=True)
        df = pd.DataFrame(serializer.data)
        df['full_name'] = full_names
        file_path = os.path.join(settings.MEDIA_ROOT, 'sample.xlsx')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.drop(['first_name', 'last_name'], axis=1, inplace=True)
        df.to_excel(file_path, index=False)

        with open(file_path, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(), content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="sample.xlsx"'
        return response
    
class Send_mail_to_all(APIView):
    """Sending mails to Emails provides on background"""

    def get (self, request):
        email = request.data.get("email")
        send_mail_func.delay(email)
        return HttpResponse("sending sent")
    
class Send_mail_after_call(APIView):
    """Sending mails to Emails provides on background after 2 mins of api call"""

    def get (self, request):
        email = request.data.get("email")
        send_delayed_email.apply_async(args = [email,], countdown = 120)
        return HttpResponse("mail will be send in 2 mins")