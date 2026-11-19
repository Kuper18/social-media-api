from rest_framework.pagination import (
    PageNumberPagination as DRFPageNumberPagination,
)


class PageNumberPagination(DRFPageNumberPagination):
    max_page_size = 100
    page_size = 10
    page_size_query_param = "page_size"
