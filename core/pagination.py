from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination

class ProductPagination2(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10

class ProductPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10