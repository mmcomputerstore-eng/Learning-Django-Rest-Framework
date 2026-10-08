from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins,generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework import filters

from .permissions import IsStafOrReadOnly
from .models import Product
from .serializers import ProductSerializers


class ProductListCreateAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serelizer = ProductSerializers(products,many=True)

        return Response(serelizer.data)

    def post(self , request):
        serilizer = ProductSerializers(data=request.data)

        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data,status=status.HTTP_201_CREATED)

        return Response(serilizer.errors,status=status.HTTP_400_BAD_REQUEST)


class ProductDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class ProductListCreateMixinView(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def get(self,request,*args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request,*args, **kwargs)

class ProductDetailsMixinView(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

    def get(self, request, *args, **kwargs):
        return self.retrieve(request , *args, **kwargs)

    def put(self , request, *args, **kwargs):
        return self.update(request , *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request , *args, **kwargs)

    def delete(self , request , *args, **kwargs):
        return self.destroy(request , *args, **kwargs)


class ProductListCreateGenericView(generics.ListCreateAPIView):
        queryset = Product.objects.all()
        serializer_class = ProductSerializers

class ProductDetailsGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    permission_classes = [IsStafOrReadOnly]
    filterset_fields = ['name', 'price', 'stock']
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'stock','created_at']

    @action(detail=True,methods=['post'])
    def increase_stock(self,request,pk=None):
        product = self.get_object()
        quantity = request.data.get('quantity',0)

        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            return Response({'error':'quantity must be an integer'},status=status.HTTP_400_BAD_REQUEST)

        if quantity <= 0:
            return Response({'error':'quantity must be greater than 0'},status=status.HTTP_400_BAD_REQUEST)

        product.stock += quantity
        product.save()
        return Response({'success':'Stock increased successfully','new_stock':product.stock,'product':product.name},status=status.HTTP_200_OK)

    @action(detail=True,methods=['post'])
    def decrease_stock(self,request,pk=None):
        product = self.get_object()
        quantity = request.data.get('quantity',0)

        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            return Response({'error':'quantity must be an integer'},status=status.HTTP_400_BAD_REQUEST)

        if quantity <= 0:
            return Response({'error':'quantity must be greater than 0'},status=status.HTTP_400_BAD_REQUEST)

        if product.stock < quantity:
            return Response({'error':'Not enough stock available'},status=status.HTTP_400_BAD_REQUEST)

        product.stock -= quantity
        product.save()
        return Response({'success':'Stock decreased successfully','new_stock':product.stock,'product':product.name},status=status.HTTP_200_OK)