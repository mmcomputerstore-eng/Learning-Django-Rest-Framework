from django.db.migrations import serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins,generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework import filters
from .pagination import ProductPagination,ProductPagination2
from drf_spectacular.utils import extend_schema,OpenApiResponse

from .permissions import IsStafOrReadOnly
from .models import Product
from .serializers import ProductSerializers

@extend_schema(
    tags=['Products'],
    description='List products and create a product.',
)
class ProductListCreateAPIView(APIView):

    @extend_schema(
        operation_id='product_list',
        summary='List all products',

        description='Get List of All Products.',
        responses=ProductSerializers(many=True),
        tags=['Products'],
    )
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializers(products, many=True)

        return Response(serializer.data)

    @extend_schema(
    operation_id='product_create',
    summary='Create a product',
    description='Create a new product in the inventory.',
    request=ProductSerializers,
    responses={
        201: ProductSerializers,
        400: OpenApiResponse(
            description='Invalid product data.'
        ),
    },
    tags=['Products'],
)
    def post(self, request):
        serializer = ProductSerializers(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

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


@extend_schema(
    tags=['Products'],
    description='API endpoints for managing inventory products.'
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('owner').all()
    serializer_class = ProductSerializers
    permission_classes = [IsStafOrReadOnly]
    filterset_fields = ['name', 'price', 'stock']
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'stock','created_at']
    pagination_class = ProductPagination2

    @extend_schema(
        summary='List all products',
        description='Retrieve a paginated list of inventory products.',
        tags=['Products'],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary='Create a product',
        description='Create a new inventory product.',
        tags=['Products'],
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
    summary='Retrieve a product',
    description='Retrieve the details of a specific product by its ID.',
    tags=['Products'],
)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


    @extend_schema(
    summary='Update a product',
    description='Update all required product fields.',
    tags=['Products'],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


    @extend_schema(
    summary='Partially update a product',
    description='Update only the product fields provided in the request.',
    tags=['Products'],
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


    @extend_schema(
    summary='Delete a product',
    description='Delete a specific product by its ID.',
    tags=['Products'],
    )

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @extend_schema(
    summary='Increase product stock',
    description='Increase the stock quantity of a product.',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'quantity': {
                    'type': 'integer',
                    'example': 10,
                },
            },
            'required': ['quantity'],
        }
    },
    responses={
        200: OpenApiResponse(
            description='Stock increased successfully.'
        ),
        400: OpenApiResponse(
            description='Invalid quantity.'
        ),
        404: OpenApiResponse(
            description='Product not found.'
        ),
    },
    tags=['Products'],
    )
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

    @extend_schema(
    summary='Decrease product stock',
    description='Decrease stock after validating the requested quantity.',
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'quantity': {
                    'type': 'integer',
                    'example': 5,
                },
            },
            'required': ['quantity'],
        }
    },
    responses={
        200: OpenApiResponse(
            description='Stock decreased successfully.'
        ),
        400: OpenApiResponse(
            description='Invalid quantity or insufficient stock.'
        ),
        404: OpenApiResponse(
            description='Product not found.'
        ),
    },
    tags=['Products'],
    )    
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