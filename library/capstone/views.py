from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required   
from django.utils import timezone
from django.http import HttpResponse
from . import forms
from .models import Book, User, Author,Rented
from datetime import datetime, timedelta
from .forms import BookForm, AuthorForm
from django.contrib.auth.decorators import user_passes_test


# Create your views here.

def is_staff(user):
    return user.is_staff




# user
@login_required
def returnBook(request, pk):
    rented_book = get_object_or_404(Rented, pk=pk)
    rented_book.book.isRented = False
    rented_book.book.save()
    rented_book.returned_date = datetime.now()
    rented_book.save()
    return redirect('home')

@login_required
def myRentedBook(request):
    rented_books = Rented.objects.filter(user=request.user)  
    now = timezone.now()
    today = now.date()
    return render(request, 'my_rented_books.html', {'rented_books': rented_books, 'now':today})

@login_required
def rentBook(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.isRented = True
    book.save()

    user = request.user

    rented_date = datetime.now()
    return_date = rented_date + timedelta(days=7)

    rented_book = Rented(book=book, user=user, rented_date=rented_date, return_date=return_date)
    rented_book.save()
    return redirect('home')




# staff

@user_passes_test(is_staff)
def editBook(request, pk):
    book = get_object_or_404(Book, pk=pk)  # Obtém o livro do banco
    form = BookForm(request.POST, instance=book) 
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)  # Preenche com os novos dados
        if form.is_valid():  # Valida o formulário
            form.save()  # Salva as alterações
            return redirect('home')  # Redireciona para a página do livro
        else:
            form = BookForm(instance=book)  # Preenche o formulário com os dados atuais do livro

    return render(request, 'edit_book.html', {'form': form, 'book':book})

@user_passes_test(is_staff)
def deleteAuthor(request,pk):
        author = get_object_or_404(Author, pk=pk)
        author.delete()
        return redirect('authorList')


@user_passes_test(is_staff)
def editAuthor(request, pk):
    author = get_object_or_404(Author, pk=pk)  
    form = AuthorForm(instance=author)
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('authorList')#!!!!!!!!!!!!!!!!!!!!!!!!!!!
        else:
            form = AuthorForm(instance=author)
    return render(request, 'edit_author.html', {'form': form, 'author':author})

@user_passes_test(is_staff)
def addBook(request):
    author = Author.objects.all()
    if request.method == 'POST':
        
        title = request.POST.get('title')
        author_name = request.POST.get('author')  # Nome do autor enviado pelo formulário
        pub_date = request.POST.get('pub_date')  # Data de publicação
        description = request.POST.get('description')  # Descrição do livro
        genre = request.POST.get('genre')  # Gênero do livro
        isRented = False  # Livro não está alugado

        # Buscar o autor na base de dados
        try:
            author = Author.objects.get(name=author_name)
        except Author.DoesNotExist:
            # Caso o autor não exista, retorne uma mensagem de erro
            return HttpResponse(f"Author '{author_name}' not found.")

        # Converter a data de publicação para o formato adequado (YYYY-MM-DD)
        try:
            pub_date = datetime.strptime(pub_date, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse("Invalid date format for publication date. Please use YYYY-MM-DD format.")

        # Cria o livro e associa o autor
        book = Book(title=title, author=author, publication_date=pub_date, description=description, genre=genre, isRented= isRented)
        book.save()

        return redirect('home')  # Redireciona para a página inicial após salvar o livro

    return render(request, 'add_book.html',{'authors':author})

# view to add an author
@user_passes_test(is_staff)
def addAuthor(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        birth_date = request.POST.get('birth_date')
        death_date = request.POST.get('death_date')
        country_of_birth = request.POST.get('birth_country')

        if not death_date:
            death_date = None

        author = Author(name= name, date_of_birth = birth_date, country_of_birth = country_of_birth, date_of_death = death_date) 
        author.save()
        return redirect('authorList')
    return render(request, 'add_author.html')

#       view to delete book
@user_passes_test(is_staff)
def deleteBook(request,pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return redirect('home')












# both user and staff
def historie(request):
    rented_book = Rented.objects.all()
    user_rented = Rented.objects.filter(user = request.user)
    query = request.GET.get('q')  # Captura o valor da pesquisa
    if query:
        rented_book = rented_book.filter(user__username__icontains=query)
    return render(request, 'historie.html', {'rented_book': rented_book,'user_rented':user_rented, 'query': query})

#        view to see book writen by certain author
def AuthorBooks(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.filter(author=author)
    return render(request, 'author_books.html', {'books': books, 'author': author})


#       view for the book detail page
@login_required
def bookDetail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book_detail.html', {'book': book})

#       view for the author List
@login_required
def authorList(request):
    authors = Author.objects.all()
    return render(request, 'authors_list.html', {'authors': authors})

#       view for the login
def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Invalid username or password")
        
    return render(request, 'login.html')

#       the view for the logout function
@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

#       creating the view for the signup page
def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    return render(request, "signup.html", context={'form':form})

#       view for the book list
@login_required
def Home(request):
    Books = Book.objects.all()
    rented_book = Rented.objects.all()
    unavailable_books = rented_book.filter(returned_date__isnull=True)
    return render(request, 'book_list.html', {'books': Books, 'rented_book':rented_book, 'unavailable_books':unavailable_books})  



