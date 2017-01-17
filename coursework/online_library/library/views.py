from . import forms
from django.core.urlresolvers import reverse
from .models import Library
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import logout


# Create your views here.


class LibraryView(generic.ListView):
    template_name = 'library/index.html'
    paginate_by = 20
    context_object_name = 'library_list'

    def get_queryset(self):
        return Library.find(limit=0)


class Registration(generic.View):
    template_name = 'library/register.html'

    def post(self, request):
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            data = register_form.cleaned_data.copy()
            errors = ""

            try:
                if User.objects.get_by_natural_key(username=data['username']):
                    errors += "Sorry, username is in use.\n"
                    return render(request, self.template_name, {'form': register_form, 'errors': errors})

            except User.DoesNotExist:
                if data['password'] != data['password2']:
                    errors += "Passwords must match.\n"
                    return render(request, self.template_name, {'form': register_form, 'errors': errors})

            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )

            user.set_password(data['password'])
            user.save()

            return HttpResponseRedirect(reverse('library:login'))

    def get(self, request):
        register_form = forms.RegisterForm()

        return render(request, self.template_name, {'form': register_form})


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('library:index'))


class BookEdit(generic.View):

    def post(self, request,  book_id=None):
        upload_form = forms.UploadBookForm(request.POST, request.FILES)

        if upload_form.is_valid():
            data = upload_form.cleaned_data

            if  book_id is None:

                if request.FILES.get('image', False):
                    Library.handleUploadedImages(request.FILES['image'])
                if request.FILES.get('bookFile', False):
                    Library.handleUploadedFiles(request.FILES['bookFile'])

                book_id = Library.Insert_Book(request, upload_form)

                return HttpResponseRedirect(reverse('library:book_view', args={ book_id, }))
            else:

                Library.edit_Book(request, data, book_id)
                return HttpResponseRedirect(reverse('library:book_view', args={ book_id, }))

        return render(request, 'library/book_upload.html', {'form': upload_form, })

    def get(self, request, book_id=None):
        upload_form = forms.UploadBookForm()

        if  book_id is None:
            return render(request, 'library/book_upload.html', {'form': upload_form})
        else:
            data = Library.get_book(book_id)
            upload_form.fields['name'].initial = data['name']
            upload_form.fields['description'].initial = data['description']
            upload_form.fields['author'].initial = data['author']
            upload_form.fields['rate'].initial = data['rates'][request.user.username]

            return render(request, 'library/book_edit.html', {'form': upload_form, 'book_id': book_id})

class BookView(generic.View):  # #4 view book info, 5 read a book
    book_template = 'library/book_view.html'

    def get(self, request, book_id=None):
        if book_id is None:
            return Http404('Book not found')
        book = Library.get_book(book_id)

        if not book:
            return Http404('Book not found')

        return render(request, self.book_template, {'book': book})

    def post(self, request, book_id=None, rate= None):#add marks in here

        return Http404('Wat?')


class UserEdit(generic.View):

    def post(self, request, user_name):
        edit_form = forms.RegisterForm(request.POST)
        data = edit_form.cleaned_data()
        result = User.editUser(data, user_name)

        #add some checks to wrong edits
        return HttpResponseRedirect(reverse('library:view_user', {user_name, }))

    def get(self, request, user_name):
        edit_form = forms.RegisterForm()
        #put some user data
        return render(request, 'user_edit.html', {'form': edit_form})


class UserView(generic.View):
    def get(self, request, user_name=None):

        if not user_name:
            user = User.find_one(request.user.username)
            return render(request, 'user_view.html', {'data': user})
        else:
            user = User.find_one(user_name)
            return render(request, 'user_view.html', {'data': user})

        return render(request, 'user_view.html', {'data': user})