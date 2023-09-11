from django.urls import path
from products_creation.views import CategoryList,CategoryDetail,ProductList,ProductDetail

# router = DefaultRouter()
# router.register(r'categories', views.CategoryViewSet)
urlpatterns = [
    path('categories', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>', CategoryDetail.as_view(), name='category-detail'),
    path('products', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>', ProductDetail.as_view(), name='product-detail'),

]
