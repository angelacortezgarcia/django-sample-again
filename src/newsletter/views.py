from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ContactForm, PostForm
from .models import Post
# Create your views here.

# @login_required(login_url="/newsletter/login")
def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    if not request.user.is_authenticated:
        raise Http404
    form = PostForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request,"Successfully created")
        return HttpResponseRedirect(instance.get_absolute_url())


    context= {
        "form": form,
    }
    return render(request,"post_form.html", context)

def post_detail(request,id=None): #retrienve
    instance=get_object_or_404(Post, id=id)
    context = {
        "title": instance.title,
        "instance": instance,
    }
    return render(request,"post_detail.html", context)

def post_list(request): #list items
    form_contact = ContactForm(request.POST or None)
    if form_contact.is_valid():
        form_email = form_contact.cleaned_data.get("email")
        form_message = form_contact.cleaned_data.get("message")
        form_full_name = form_contact.cleaned_data.get("full_name")

        subject = "ACOMSS Newsletter"
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email]
        contact_message = "FROM: %s MESSAGE: %s  EMAIL ADDRESS: %s"%(form_full_name,form_message,form_email)

        send_mail(subject, contact_message, from_email, to_email, fail_silently=True)

    queryset = Post.objects.all().order_by('-timestamp')[0:3]
    context = {
        "object_list": queryset,
        "title": "List",
        "form": form_contact,
    }
    return render(request,"post_list0.html", context)
    # return render(request,"index.html", context)

def post_articles(request): #list items
    queryset_list = Post.objects.all()

    query = request.GET.get("q")
    if query:
        queryset_list= queryset_list.filter(
                Q(title__icontains=query)|
                Q(content__icontains=query)|
                Q(user__first_name__icontains=query)|
                Q(user__last_name__icontains=query)
                ).distinct()
    paginator = Paginator(queryset_list, 6) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list": queryset,
        "title": "List",
    }
    return render(request,"articels.html", context)
    # return render(request,"post_list.html", context)

# @login_required(login_url="login/")
def post_update(request,id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance=get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None,instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"Saved",extra_tags='html_safe')
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request,"post_form.html", context)

# @login_required(login_url="/")
def post_delete(request,id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance=get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request,"successfully deleted")
    # return redirect("newsletter:list")
    return redirect("/newsletter/articles")

def order_by_title(request):
    queryset_list = Post.objects.all().order_by('title')
    paginator = Paginator(queryset_list, 6) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        "object_list": queryset,
        "title": "List",
    }
    return render(request,"articels.html", context)

def old_post(request):
    queryset_list = Post.objects.all().order_by('timestamp')
    paginator = Paginator(queryset_list, 6) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        "object_list": queryset,
        "title": "List",
    }
    return render(request,"articels.html", context)
def new_post(request):
    queryset_list = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(queryset_list, 6) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        "object_list": queryset,
        "title": "List",
    }
    return render(request,"articels.html", context)

def author_post(request):
    queryset_list = Post.objects.all().order_by('user')
    paginator = Paginator(queryset_list, 6) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        "object_list": queryset,
        "title": "List",
    }
    return render(request,"articels.html", context)

# def contact(request):
#     form_contact = ContactForm(request.POST or None)
#     if form_contact.is_valid():
#         form_email = form.cleaned_data.get("email")
#         form_message = form.cleaned_data.get("message")
#         form_full_name = form.cleaned_data.get("full_name")
#
#         subject = "ACOMSS Newsletter"
#         from_email = settings.EMAIL_HOST_USER
#         to_email = [from_email]
#         contact_message = "%s: %s via %s"%(form_full_name,form_message,form_email)
#
#         send_mail(subject, contact_message, from_email, to_email, fail_silently=True)
#     context = {
#         "form": form_contact,
#     }
#     return render(request,"post_list0.html",context)
    # return render(request,"forms.html",context)
