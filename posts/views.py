from urllib import quote_plus

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from .models import Post

from django.core.urlresolvers import reverse
# Create your views here.


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_detail(request, detail_id=None):  # retrieve
    instance = get_object_or_404(Post, id=detail_id)

    # if instance.publish > timezone.now().date() or instance.draft:
    # if not request.user.is_staff or not request.user.is_superuser:
    # raise HTTP404

<<<<<<< HEAD
    share_string = quote_plus(instance.content)
=======
def post_detail(request, id=None):  #retrieve
    instance = get_object_or_404(Post, id=id)
    #if instance.publish > timezone.now().date() or instance.draft:
        #if not request.user.is_staff or not request.user.is_superuser:
            #raise HTTP404
    share_string = quote_plus(instance.description)
>>>>>>> First commit
    context = {
        "title": instance.title,
        "instance": instance,
        "share_string": share_string,
    }
    return render(request, "post_detail.html", context)


def post_list(request):
    queryset_list = Post.objects.all()  # .order_by("-timestamp")

    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
                )
        #return HttpResponseRedirect(reverse('posts'))
        return render(request, '/post_list.html', {'posts': post})


    paginator = Paginator(queryset_list, 8)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        "object_list": queryset,
        "title": "List"
    }
    # if request.user.is_authenticated():
    #    context = {
    #        "title": "my User list"
    #  }
    # else:
    #    context = {
    #        "title": "List"
    #   }
    return render(request, "post_list.html", context)


def post_update(request, update_id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=update_id)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "<a href='#'>Item</a> Saved", extra_tags='html_safe')

        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": instance.title,
        "instance": instance,
        "form": form,
    }
    return render(request, "post_form.html", context)


def post_delete(request, delete_id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, id=delete_id)
    instance.deleted()
    messages.success(request, "Successfully deleted")
    return redirect("post:list")
