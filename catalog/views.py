from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from .models import Author,Language,Genre,Book,BookInstance
from django.views import generic
from django.views.generic import CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse,reverse_lazy
from .forms import RenewBookForm
import datetime

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
    return render(request,"index.html",context)

class BookListView(generic.ListView):
    model =Book
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10

class AuthorDetailView(generic.DetailView):
    model = Author

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    paginate_by = 10
    template_name = 'bookinstance_list_borrowed_user.html'

    def get_queryset(self) -> QuerySet[Any]:
        return (BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='o')
            .order_by('due_back'))


class StaffView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    paginate_by = 10
    template_name = 'staff_view.html'

    def get_queryset(self) -> QuerySet[Any]:
        return (BookInstance.objects.filter(status__exact='o').order_by('due_back'))
    

def renew_book_librarian(request,pk):
    book_instance = get_object_or_404(BookInstance,pk=pk)
    if request.method == 'POST':
        form =RenewBookForm(request.Post)
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['Renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('staff'))
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'book_renew_librarian.html', context)

class AuthorCreate(CreateView,PermissionRequiredMixin):
    model=Author
    fields = '__all__'
    permission_required = 'catalog.add_author'

class AuthorUpdate(UpdateView,PermissionRequiredMixin):
    model = Author
    fields = '__all__'
    permission_required = 'catalog.change_author'

class AuthorDelete(PermissionRequiredMixin,DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'
    def form_valid(self,form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e: 
            return HttpResponseRedirect(reverse('author-delete',kwargs={'pk':self.object.pk}))
        
class BookCreate(CreateView,PermissionRequiredMixin):
    model= Book
    fields = '__all__'
    permission_required = 'catalog.add_book'

class BookUpdate(UpdateView,PermissionRequiredMixin):
    model = Book
    fields = "__all__"
    permission_required = 'catalog.change_book'

class BookDelete(DeleteView,PermissionRequiredMixin):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.delete_book'
    def form_vaild(self,form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(reverse('author-delete',kwargs={'pk':self.object.pk}))

from catalog.forms import RenewBookForm

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        book_renewal_form = RenewBookForm(request.POST)
        if book_renewal_form.is_valid():
            book_instance.due_back = book_renewal_form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'book_renewal_form': book_renewal_form,
        'book_instance': book_instance,
    }

    return render(request, 'book_renew_librarian.html', context)