from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Author,Language,Genre,Book,BookInstance
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

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
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    paginate_by = 10
    template_name = 'catalog/bookinstance_list_borrowed_user.html'

    def get_queryset(self) -> QuerySet[Any]:
        return (BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back'))


class StaffView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    paginate_by = 10
    template_name = 'catalog/staff_view.html'

    def get_queryset(self) -> QuerySet[Any]:
        return (BookInstance.objects.filter(status__exact='o').order_by('due_back'))