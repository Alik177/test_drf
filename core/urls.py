"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path


from app.views import *

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import *

SchemaView = get_schema_view(
    info=openapi.Info(
        title='E_comm_shop_drf Project',
        default_version='1.0',
        description='This is my first project',
        terms_of_service='',
        contact=openapi.Contact(name='RoboCop', url='', email='robocop@gmail.com'),
        license=openapi.License(name='License', url='')
    ),
    patterns=[
        # path('api/products', ProductApiView.as_view(), name='products_api_url'),
        # path('api/products/<int:pk>', ProductDetailApiView.as_view(), name='products_detail_api_url'),
        path('api/books', BookApiView.as_view(), name='books_api'),
        path('api/books/<int:pk>', BookDetailApiView.as_view(), name='books_detail_api_url'),
        path('api/authors', AuthorApiView.as_view(), name='authors_api'),
        path('api/authors/<int:pk>', AuthorDetailApiView.as_view(), name='author_detail_api_url'),
        path('api/currencies', CurrencyApiView.as_view(), name='currencies_api'),
        path('api/currencies/<int:pk>', CurrencyDetailApiView.as_view(), name='currency_detail_api_url'),
        path('api/genres', GenreApiView.as_view(), name='genres_url'),
        path('api/genres/<int:pk>', GenreDetailApiView.as_view(), name='genres_detail_url'),
        path('api/reviews', ReviewApiView.as_view(), name='review_url'),
        path('api/reviews/<int:pk>', ReviewDetailApiView.as_view(), name='reviews_detail_url'),
        path('api/login', AuthApiView.as_view(), name='login_url'),
        path('api/profile', ProfileApiView.as_view(), name='profile_url'),
        path('api/fav_genre', FavoriteGenreApiView.as_view(), name='fav_genre_url'),
        path('api/logout', LogOutApiView.as_view(), name='logout_url'),
        path('api/my_history', HistoryApiView.as_view(), name='history_url'),
    ],
    # public=True,
    # permission_classes=[AllowAny],
    permission_classes=[IsAuthenticated]

)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/products', ProductApiView.as_view(), name='products_api_url'),
    # path('api/products/<int:pk>', ProductDetailApiView.as_view(), name='products_detail_api_url'),
    path('api/books', BookApiView.as_view(), name='books_api'),
    path('api/books/<int:pk>', BookDetailApiView.as_view(), name='books_detail_api_url'),
    path('api/authors', AuthorApiView.as_view(), name='authors_api'),
    path('api/authors/<int:pk>', AuthorDetailApiView.as_view(), name='author_detail_api_url'),
    path('api/currencies', CurrencyApiView.as_view(), name='currencies_api'),
    path('api/currencies/<int:pk>', CurrencyDetailApiView.as_view(), name='currency_detail_api_url'),
    path('api/genres', GenreApiView.as_view(), name='genres_url'),
    path('api/genres/<int:pk>', GenreDetailApiView.as_view(), name='genres_detail_url'),
    path('api/reviews', ReviewApiView.as_view(), name='review_url'),
    path('api/reviews/<int:pk>', ReviewDetailApiView.as_view(), name='reviews_detail_url'),
    path('api/login', AuthApiView.as_view(), name='login_url'),
    path('api/profile', ProfileApiView.as_view(), name='profile_url'),
    path('api/fav_genre', FavoriteGenreApiView.as_view(), name='fav_genre_url'),
    path('api/logout', LogOutApiView.as_view(), name='logout_url'),
    path('api/my_history', HistoryApiView.as_view(), name='history_url'),
    # path('api/test_login', TestApiView.as_view(), name='test_login_url'),

    path('swagger', SchemaView.with_ui()),
]

urlpatterns += [
    path('cart/add/<int:id>/', cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', item_decrement, name='item_decrement'),
    path('cart/cart_clear/', cart_clear, name='cart_clear'),
    path('cart/cart-detail/', cart_detail, name='cart_detail'),

    path('checkout', CheckOutApiView.as_view(), name='checkout_url'),
    path('api/paginated_books', BookPaginatorApiView.as_view(), name='paginator_url'),
    path('api/book_search', BookSearchApiView.as_view(), name='book_search_url'),
    path('api/book_price', BookPriceApiView.as_view(), name='book_price_url'),


]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)