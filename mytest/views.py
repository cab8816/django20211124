import datetime
import io


from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, FileResponse, Http404
from django.shortcuts import render, redirect
from django.contrib import auth
from django.views.generic import ListView
from paginator import Paginator

from mytest.forms import ContactForm
from mytest.models import Book, Publisher, Author

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView


# Create your views here.
def hello(request, dd=1):
    return HttpResponse("hello xam = %s" % dd)


def current_datetime(request):
    current_date = datetime.datetime.now()
    # return render(request, 'current_datetime.html', locals())
    return render(request, 'current_datetime.html', {'current_date': current_date})


def display_meta(request):
    values = request.META.items()
    # values = request.POST.values()

    return render(request, 'displaymeta.html', {'meta': values})


def search_form(request):
    return render(request, 'search_form.html')


def search(request):
    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            books = Book.objects.filter(title__icontains=q)
            return render(request, 'search_results.html', {'books': books, 'query': q})
    return render(request, 'search_form.html', {'error': error})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'),
                ['siteowner@example.com'],
            )
            return redirect('/contact/thanks/')
    else:
        form = ContactForm(initial={'subject': '我爱你的网站'})

    return render(request, 'contact_form.html', {'form': form})


def searchxie(request):
    xie = Author.author.all()
    cherry = Author.cherryforxie(xie.first())
    # assert False
    return render(request, 'search_xiePublisher.html', {'xies': xie, 'cherry': cherry})


def hellopdf(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 10, "hello world,xam.")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')


# Cookie 使用方法
def show_color(request):
    if request.session.test_cookie_worked():
        # request.session.delete_test_cookie()
        if "favorite_color" in request.COOKIES:

            return HttpResponse('your favorite color is %s' % request.COOKIES["favorite_color"])

        else:
            return HttpResponse("you don't have a favorite color.")
    else:
        return HttpResponse("your ieexplorer not accept COOKIE.")


# @login_required(login_url='/login/')
def set_color(request, favorite_color):
    request.session.set_test_cookie()
    if 'favorite_color' in request.GET:
        response = HttpResponse('your favorite color is now %s' % request.GET['favorite_color'])
        response.set_cookie("favorite_color", favorite_color)
        # response.set_cookie("favorite_color", request.GET['favorite_color'])
        return response
    else:
        return HttpResponse("you don't give a favorite color.")


# session 使用方法

# def post_comment(request):
#     if request.method != 'POST':
#         raise  Http404('only posts are allowed.')
#
#     if 'comment' not in request.POST:
#         raise Http404('comment not submitten.')
#     if request.session.get('has_commented',False):
#         return HttpResponse('You are already commentted.')
#     c=comments.Comment(comment=request.POST['comment'])
#     c.save()
#     request.session['has_commented'] = True
#     return HttpResponse('thanks for your comment.')

def login_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        # return redirect('/loginok/')
        return render(request, 'loginok.html')
    else:
        # return redirect('/loginfail/')
        return render(request, 'loginok.html')


def logout_view(request):
    auth.logout(request)
    return redirect('/logout/')


# user_passes_test 使用一个必需的参数： 一个可调用的方法，当存在 User 对象并当此用户允许查看该页面时返回True 。 注意 user_passes_test 不会自动检查 User
def login(request):
    if request.method != 'POST':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            # return redirect('/loginok/')
            return render(request, 'loginok.html')
        else:
            # return redirect('/loginfail/')
            # return render(request, 'loginok.html')
            return HttpResponse('login fail')


class PublisherCreateView(CreateView):
    model = Publisher
    fields = ['name']
    success_url = reverse_lazy('publisher-list')


class PublisherUpdateView(UpdateView):
    model = Publisher
    fields = ['name']
    success_url = reverse_lazy('publisher-list')


class PublisherDeleteView(DeleteView):
    model = Publisher
    success_url = reverse_lazy('publisher-list')


def publisherListView(request):
    publisher = Publisher.objects.all()
    paginator = Paginator(publisher, 5)
    return render(request, 'publisher_list.html', {'publisher': publisher, 'paginator': paginator})
