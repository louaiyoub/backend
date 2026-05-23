from django.urls import path
from . import views
#from .views import ProductViewSet
#from rest_framework.routers import DefaultRouter
#router = DefaultRouter()
#router.register('products', ProductViewSet,)
#urlpatterns = router.urls

#urlpatterns = [
    #path('products/', views.ProductViewSet.as_view({'get': 'list'}), name='product-list'),
    #path('product_create', views.create_product, name='create-product'),
    #path('product_update/<int:id>/', views.ProductViewSet.as_view({'put': 'update'}), name='update-product'),
    #path('product_delete/<int:id>/', views.ProductViewSet.as_view({'delete': 'destroy'}), name='delete-product'),]
urlpatterns = [
    path('product/', views.product_list, name='product_list'),
    path('create_product/', views.create_product),
    path('update_product/<int:id>/',views.update_product,name='update_product'),
    path('delete_product/<int:id>/',views.delete_product,name='delete_product'),
    path('login/', views.login_view, name='login'),
    path('product/<int:id>/getorput', views.get_or_update_product, name='get_or_update_product'),

]
