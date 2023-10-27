from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Кастомный пагинатор с лимитом для страницы."""
    page_size_query_param = 'limit'
