from django.shortcuts import render
from .models import Author,Language,Genre,Book,BookInstance
from django.views import generic

def index(request):
    authors_num = Author.objects.count()
    books_num = Book.objects.count()
    books_instance = BookInstance.objects.count()
    avail_book_instance = BookInstance.objects.filter(status__exact="a").count()
    
    context = {
        'num_books': books_num,
        'num_instances': books_instance,
        'num_instances_available': avail_book_instance,
        'num_authors': authors_num,
    }
    return render(request,"catalog/index.html",context)

class BookListView(generic.ListView):
    model =Book
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author