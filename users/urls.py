from django.urls import  path
from categories_product import settings
from users.views import ExcelDownloadView, Send_mail_to_all, Send_mail_after_call

from django.conf.urls.static import static

urlpatterns = [
    path('excel', ExcelDownloadView.as_view(), name='excel'),
    path('mail', Send_mail_to_all.as_view(), name='mail'),
    path('mail_after', Send_mail_after_call.as_view(), name='mail_after'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
