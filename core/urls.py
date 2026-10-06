from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductListCreateAPIView,ProductDetailsAPIView,ProductListCreateMixinView,ProductDetailsMixinView,ProductListCreateGenericView,ProductDetailsGenericView,ProductViewSet

router = DefaultRouter()
router.register('products/viewset',ProductViewSet,basename='product')

urlpatterns = [
    path('products/',ProductListCreateAPIView.as_view(),name='product-list-create'),
    path('products/<int:pk>',ProductDetailsAPIView.as_view(),name='product-detail'),
    path('products/mixins/',ProductListCreateMixinView.as_view(),name='product-list-create-mixins'),
    path('products/mixins/<int:pk>',ProductDetailsMixinView.as_view(),name='product-details-mixins'),
    path('products/generic/',ProductListCreateGenericView.as_view(),name='product-list-create-generic'),
    path('products/generic/<int:pk>',ProductDetailsGenericView.as_view(),name='product-detail-generic'),
]+router.urls

