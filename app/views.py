from cart.cart import Cart
from django.contrib.sites import requests
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from drf_yasg.utils import swagger_auto_schema
from rest_framework import parsers

# class ProductApiView(APIView):
#     permission_classes = [IsAuthenticated, ]
#
#     def get(self, request):
#         products = Product.objects.all()
#         data = {
#             'products': ProductSerializer(products, many=True).data
#         }
#         # many = True ставится если нужно сериализовать несколько объектов
#         return Response(data=data, status=status.HTTP_200_OK)
#
#     @swagger_auto_schema(
#         request_body=ProductSerializer,
#         # query_serializer=ProductSerializer,
#         responses={
#             201: 'Product is added to DB',
#             400: 'Serializer error. For more info watch response'
#         },
#         security=[],
#         operation_id='Create Product',
#         operation_description='This API for creating new product into database',
#     )
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()  # save() -> Сохранить объект их сериалайзера в БД
#             # return Response(data={'msg': 'Product Created successfully!'}, status=status.HTTP_201_CREATED)
#             return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class ProductDetailApiView(APIView):
#     permission_classes = []
#     parser_classes = [parsers.FormParser, parsers.JSONParser]
#
#     def get(self, request, pk):
#         from django.shortcuts import get_object_or_404
#         product = get_object_or_404(Product, id=pk)
#         data = {
#             'product': ProductSerializer(product, many=False).data
#         }
#         return Response(data=data, status=status.HTTP_200_OK)
#
#
#     def patch(self, request, pk):
#         from django.shortcuts import get_object_or_404
#         product = get_object_or_404(Product, id=pk)
#         serializer = ProductSerializer(product, data=request.data, partial=True)
#         # partial=True - Означает что обновляются не все поля, а только часть из них
#         if serializer.is_valid():
#             serializer.save()
#             return Response(data=serializer.data, status=status.HTTP_200_OK)
#         return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         from django.shortcuts import get_object_or_404
#         product = get_object_or_404(Product, id=pk)
#         product.delete()
#         return Response(data={'msg': 'Product deleted!'}, status=status.HTTP_204_NO_CONTENT)

class BookApiView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        books = Book.objects.all()
        data = {
            'books': BookSerializer(books, many=True).data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=BookSerializer,
        # query_serializer=ProductSerializer,
        responses={
            201: 'Book is added to DB',
            400: 'Serializer error. For more info watch response'
        },
        security=[],
        operation_id='Create Product',
        operation_description='This API for creating new book into database',
    )
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookDetailApiView(APIView):
    permission_classes = []
    def get(self, request, pk):
        from django.shortcuts import get_object_or_404
        book = get_object_or_404(Book, id=pk)
        data = {
            'book': BookSerializer(book, many=False).data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        from django.shortcuts import get_object_or_404
        if not request.user.is_authenticated:
            return Response(data={"msg": "You have to log in"},status=status.HTTP_400_BAD_REQUEST)
        else:
            book = get_object_or_404(Book, id=pk)
            serializer = BookSerializer(book, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        from django.shortcuts import get_object_or_404
        if not request.user.is_superuser:
            return Response(data={"msg": "You don't have permissions. Contact the administrator"},status=status.HTTP_400_BAD_REQUEST)
        else:
            book = get_object_or_404(Book, id=pk)
            book.delete()
            return Response(data={'msg': 'Book deleted!'}, status=status.HTTP_204_NO_CONTENT)

class AuthorApiView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        authors = Author.objects.all()
        data = {
            'authors': AuthorSerializer(authors, many=True).data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=AuthorSerializer,
        # query_serializer=ProductSerializer,
        responses={
            201: 'Author is added to DB',
            400: 'Serializer error. For more info watch response'
        },
        security=[],
        operation_id='Create new Author',
        operation_description='This API for creating new author into database',
    )
    def post(self, request):
        if not request.user.is_authenticated:
            return Response(data={"msg": "You have to log in"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = AuthorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class AuthorDetailApiView(APIView):
    permission_classes = []

    def get(self, request, pk):
        from django.shortcuts import get_object_or_404
        author = get_object_or_404(Author, id=pk)
        data = {
            'author': AuthorSerializer(author, many=False).data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        from django.shortcuts import get_object_or_404
        if not request.user.is_authenticated:
            return Response(data={"msg": "You have to log in"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            author = get_object_or_404(Author, id=pk)
            serializer = AuthorSerializer(author, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        from django.shortcuts import get_object_or_404
        if not request.user.is_superuser:
            return Response(data={"msg": "You don't have permissions. Contact the administrator"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            author = get_object_or_404(Author, id=pk)
            author.delete()
            return Response(data={'msg': 'Author deleted!'}, status=status.HTTP_204_NO_CONTENT)

class CurrencyApiView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        currencies = Currency.objects.all()
        data = {
            'currencies': CurrencySerializer(currencies, many=True).data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CurrencySerializer,
        # query_serializer=ProductSerializer,
        responses={
            201: 'Currency is added to DB',
            400: 'Serializer error. For more info watch response'
        },
        security=[],
        operation_id='Create new Currency',
        operation_description='This API for creating new currency into database',
    )
    def post(self, request):
        serializer = CurrencySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CurrencyDetailApiView(APIView):
    permission_classes = []

    def get(self, request, pk):
        from django.shortcuts import get_object_or_404
        currency = get_object_or_404(Currency, id=pk)
        data = {
            'currency': CurrencySerializer(currency, many=False).data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        from django.shortcuts import get_object_or_404
        if not request.user.is_authenticated:
            return Response(data={"msg": "You have to log in"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            currency = get_object_or_404(Currency, id=pk)
            serializer = CurrencySerializer(currency, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        from django.shortcuts import get_object_or_404
        if not request.user.is_superuser:
            return Response(data={"msg": "You don't have permissions. Contact the administrator"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            currency = get_object_or_404(Currency, id=pk)
            currency.delete()
            return Response(data={'msg': 'Currency deleted!'}, status=status.HTTP_204_NO_CONTENT)

class GenreApiView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        genres = Genre.objects.all()
        data = {
            'genres': GenreSerializer(genres, many=True).data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=GenreSerializer,
        # query_serializer=ProductSerializer,
        responses={
            201: 'Genre added to DB',
            400: 'Serializer error. For more info watch response'
        },
        security=[],
        operation_id='Create new Genre',
        operation_description='This API for creating new genre into database',
    )
    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GenreDetailApiView(APIView):
    permission_classes = []

    def get(self, request, pk):
        from django.shortcuts import get_object_or_404
        genre = get_object_or_404(Genre, id=pk)
        data = {
            'genre': GenreSerializer(genre, many=False).data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        from django.shortcuts import get_object_or_404
        if not request.user.is_authenticated:
            return Response(data={"msg": "You have to log in"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            genre = get_object_or_404(Genre, id=pk)
            serializer = GenreSerializer(genre, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        from django.shortcuts import get_object_or_404
        if not request.user.is_superuser:
            return Response(data={"msg": "You don't have permissions. Contact the administrator"},status=status.HTTP_400_BAD_REQUEST)
        else:
            genre = get_object_or_404(Genre, id=pk)
            genre.delete()
            return Response(data={'msg': 'Genre deleted!'}, status=status.HTTP_204_NO_CONTENT)

class ReviewApiView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        reviews = Review.objects.all()
        data = {
            'reviews': ReviewSerializer(reviews, many=True).data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ReviewSerializer,
        # query_serializer=ProductSerializer,
        responses={
            201: 'Review added to DB',
            400: 'Serializer error. For more info watch response'
        },
        security=[],
        operation_id='Create new Review',
        operation_description='This API for creating new review into database',
    )
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetailApiView(APIView):
    permission_classes = []

    def get(self, request, pk):
        from django.shortcuts import get_object_or_404
        review = get_object_or_404(Review, id=pk)
        data = {
            'review': ReviewSerializer(review, many=False).data
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        from django.shortcuts import get_object_or_404
        if not request.user.is_authenticated:
            return Response(data={"msg": "You have to log in"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            review = get_object_or_404(Review, id=pk)
            serializer = ReviewSerializer(review, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        from django.shortcuts import get_object_or_404
        if not request.user.is_superuser:
            return Response(data={"msg": "You don't have permissions. Contact the administrator"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            review = get_object_or_404(Review, id=pk)
            review.delete()
            return Response(data={'msg': 'Review deleted!'}, status=status.HTTP_204_NO_CONTENT)

class AuthApiView(APIView):
    permission_classes = []

    def post(self, request):
        from django.contrib.auth import authenticate, login
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(data={'msg': 'Login succesfully'}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)



class ProfileApiView(APIView):
    permission_classes = []
    def get(self, request): # READ USER
        if request.user.is_authenticated:
            data = UserSerializer(request.user, many=False).data
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(data={'msg': 'You must login!'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        from django.db.utils import IntegrityError
        username = request.data.get('username')
        fn = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')
        email = request.data.get('email')
        try:
            user = User.objects.create_user(username=username, first_name=fn, last_name=last_name, password=password,
                                            email=email)
            data = UserSerializer(user, many=False).data
            return Response(data=data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(data={'msg': 'This username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        if request.user.is_authenticated:
            serializer = UserUpdateSerializer(request.user, partial=True, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'msg': 'You must login!'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        if request.user.is_authenticated:
            request.user.is_active = False
            request.user.save()
            return Response(data={'msg': 'Your account successfully deactivated!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'msg': 'You must login!'}, status=status.HTTP_401_UNAUTHORIZED)

class FavoriteGenreApiView(APIView):
    permission_classes = []

    def get(self, request):
        if 'selected_genre' not in request.session.keys():
            return Response(data={'msg': 'First select Genre!'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'Selected Genre': request.session.get('selected_genre')}, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_authenticated:
            genre = request.data.get('genre')
            if genre:
                request.session.update({'selected_genre': genre})
                return Response(data={"msg": f"Selected genre {genre}!"}, status=status.HTTP_200_OK)
            else:
                request.session.update({'selected_genre': 'Detective'})
                return Response(data={'Selected Genre': request.session.get('selected_genre')}, status=status.HTTP_200_OK)
        else:
            return Response(data={'msg': 'You must login!'}, status=status.HTTP_401_UNAUTHORIZED)

class LogOutApiView(APIView):
    permission_classes = []

    def post(self, request):
        from django.contrib.auth import logout
        # 1) Проверить авторизован ли пользователь
        if request.user.is_authenticated:
            # 2) Импортировать logout из django.contrib.auth
            logout(request)
            # 3) Выполнить logout и вернуть response что logout прошел успешно
            return Response(data={'msg': 'Logout succesfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Пользователь не авторизован."}, status=status.HTTP_400_BAD_REQUEST)


def cart_add(request, id):
    if not request.user.is_authenticated:
        return JsonResponse(data={'msg': 'You have to log in!'}, status=status.HTTP_403_FORBIDDEN)
    cart = Cart(request)
    book = Book.objects.get(id=id)
    cart.add(book)
    return JsonResponse(data={'msg': 'Item added!'}, status=status.HTTP_200_OK)



def item_clear(request, id):
    if not request.user.is_authenticated:
        return JsonResponse(data={'msg': 'You have to log in!'}, status=status.HTTP_403_FORBIDDEN)
    cart = Cart(request)
    book = Book.objects.get(id=id)
    cart.remove(book)
    return JsonResponse(data={'msg': 'Item deleted!'}, status=status.HTTP_200_OK)



def item_increment(request, id):
    if not request.user.is_authenticated:
        return JsonResponse(data={'msg': 'You have to log in!'}, status=status.HTTP_403_FORBIDDEN)
    cart = Cart(request)
    book = Book.objects.get(id=id)
    cart.add(book)
    return JsonResponse(data={'msg': 'Item quantity incremented!'}, status=status.HTTP_200_OK)



def item_decrement(request, id):
    if not request.user.is_authenticated:
        return JsonResponse(data={'msg': 'You have to log in!'}, status=status.HTTP_403_FORBIDDEN)
    cart = Cart(request)
    book = Book.objects.get(id=id)
    cart.decrement(book)
    return JsonResponse(data={'msg': 'Item quantity decremented!'}, status=status.HTTP_200_OK)



def cart_clear(request):
    if not request.user.is_authenticated:
        return JsonResponse(data={'msg': 'You have to log in!'}, status=status.HTTP_403_FORBIDDEN)
    cart = Cart(request)
    cart.clear()
    return JsonResponse(data={'msg': 'Cart cleared!'}, status=status.HTTP_200_OK)



def cart_detail(request):
    if not request.user.is_authenticated:
        return JsonResponse(data={'msg': 'You have to log in!'}, status=status.HTTP_403_FORBIDDEN)
    cart = Cart(request)
    cart_items = []
    total = 0
    for key, value in cart.cart.items():
        subtotal = float(value.get('price')) * int(value.get('quantity'))
        value.update({'subtotal': subtotal})
        total += subtotal
        cart_items.append(value)

    data = {
        'items': cart_items,
        'total': total
    }
    return JsonResponse(data=data, status=status.HTTP_200_OK)

class CheckOutApiView(APIView):
    permission_classes = []

    def post(self, request):
        cart = Cart(request)
        total = 0
        if cart.cart:
            purchase = Purchase(total=0, customer=request.user)
            purchase.save()

            for key, value in cart.cart.items():
                subtotal = float(value.get('price')) * int(value.get('quantity'))
                total += subtotal

                try:
                    book = Book.objects.get(id=value.get('book_id'))
                except ObjectDoesNotExist:
                    return Response(data={'msg': 'Book with specified id does not exist!'}, status=status.HTTP_404_NOT_FOUND)

                # book = Book.objects.get(id=value.get('book_id'))
                item = PurchaseItem(quantity=value.get('quantity'), subtotal=subtotal) #book=book,
                item.save()

                purchase.items.add(item)
                purchase.save()

            purchase.total = total
            purchase.save()
            cart.clear()
            return Response(data={'msg': 'Check out!'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'msg': 'Cart empty!'}, status=status.HTTP_400_BAD_REQUEST)

class HistoryApiView(APIView):
    permission_classes = []

    # def get(self, request):
    #     if not request.user.is_authenticated:
    #         return Response(data={'msg': 'You have to log in!'}, status=status.HTTP_400_BAD_REQUEST)
    #     purchases = Purchase.objects.filter(customer=request.user)
    #     data = PurchaseSerializer(purchases, many=True).data
    #     return Response(data=data, status=status.HTTP_200_OK)

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(data={'msg': 'You have to log in!'}, status=status.HTTP_400_BAD_REQUEST)
        purchases = Purchase.objects.filter(customer=request.user)
        # purchases = Purchase.objects.filter(customer=request.user).order_by('-created_at')
        paginator = Paginator(purchases, 2)
        page = request.GET.get('page')
        if page is None:
            page = 1
        try:
            paginated_purchases = paginator.page(page)
        except EmptyPage:
            paginated_purchases = []

        data = {
            "purchases": PurchaseSerializer(paginated_purchases, many=True).data,
            "pages": paginator.num_pages
        }
        return Response(data=data, status=status.HTTP_200_OK)

class BookPaginatorApiView(APIView):
    permission_classes = []

    def get(self, request):
        books = Book.objects.all()
        paginator = Paginator(books, 2)
        page = request.GET.get('page')
        if page is None:
            page = 1
        try:
            paginated_books = paginator.page(page)
        except EmptyPage:
            paginated_books = paginator.page(1)
        data = {
            "books": BookSerializer(paginated_books, many=True).data,
            "pages": paginator.num_pages
        }
        return Response(data=data, status=status.HTTP_200_OK)

# class TestApiView(APIView): #Для возвращения пароля админу, закоментить/удалить после использования
#
#     def post(self, request):
#         user = User.objects.get(username='admin')
#         user.set_password('123')
#         user.save()
#         data = UserTestSerializer(user).data
#         return Response(data=data, status=status.HTTP_200_OK)

class BookSearchApiView(APIView):
    permission_classes = []

    def get(self, request):
        from django.db.models import Q
        q = request.GET.get('q')
        if q is None:
            return Response(data=[], status=status.HTTP_200_OK)
        books = Book.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))

        #  | = OR = или
        #  & = AND = и
        #  ~ = Negate = НЕ
        # products = Product.objects.filter(name__contains=q)
        # new = Product.objects.filter(description__contains=q)
        # products = products.union(new)
        # __contains - Ищет указанную часть в текст этого поля учитывая регистр
        # __icontains - То же самое что и contains, но игнорирует регистр

        data = BookSerializer(books, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)

class BookPriceApiView(APIView):
    permission_classes = []

    def get(self, request):
        from django.db.models import Q
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        if price_min is None or price_max is None:
            books = Book.objects.all()
        else:
            books = Book.objects.filter(Q(price__gte=price_min) & Q(price__lte=price_max))
            # products_min = Product.objects.filter(price__lte=price_max)
            # products_max = Product.objects.filter(price__gte=price_min)
            # products = products_min.union(products_max)
        data = BookSerializer(books, many=True).data
        return Response(data=data, status=status.HTTP_200_OK)



