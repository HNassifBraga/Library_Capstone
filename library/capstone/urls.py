from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index , name='index'),
    path('signup', views.signup_page, name='signup'),
    path('home', views.Home, name='home'),
    path('logout', views.logout_view, name="logout"),
    path('addBook', views.addBook, name="addBook"),
    path('delete_book/<int:pk>/', views.deleteBook, name='delete_book'),
    path('book_detail/<int:pk>', views.bookDetail, name='book_detail'),
    path('rent_book/<int:pk>/', views.rentBook, name='rent_book'),
    path('my_rented', views.myRentedBook, name='my_rented'),
    path('return_book/<int:pk>/', views.returnBook, name='return_book'),
    path('editBook/<int:pk>/', views.editBook, name='editBook'),
    path('authorBook/<int:pk>/', views.AuthorBooks,name='authorBook'),
    path('addAuthor', views.addAuthor, name='addAuthor'),
    path('authorList', views.authorList, name='authorList'),
    path('delete_author/<int:pk>/', views.deleteAuthor, name='delete_author'),
    path('editAuthor/<int:pk>/', views.editAuthor, name='editAuthor'),
    path('historie', views.historie, name='historie')
]
