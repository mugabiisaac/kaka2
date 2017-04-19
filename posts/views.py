from urllib import quote_plus

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm
from .models import Post
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.views import generic
# Create your views here.
#OrderPlacementMixin = get_class('checkout.mixins', 'OrderPlacementMixin')


def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        messages.success(request, "successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "form": form,
    }
    return render(request, "post_form.html", context)


#def post_detail(request, detail_id=None):  # retrieve
    #instance = get_object_or_404(Post, id=detail_id)

    # if instance.publish > timezone.now().date() or instance.draft:
    # if not request.user.is_staff or not request.user.is_superuser:
    # raise HTTP404


    #share_string = quote_plus(instance.description)

def post_detail(request, id=None):  #retrieve

    instance = get_object_or_404(Post, id=id)
    share_string = quote_plus(instance.description)
    instance.user = request.user

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
    #if not request.user.is_authenticated():
        #return HttpResponseRedirect('/')

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


#@login_required
#@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = profileForm(request.POST, istance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            user_profile = profile_form.save(commit=False)
            messages.success(request, _('Your profile was successfully updated'))
            #profile = Profile.objects.get(user_id=user_id)
            profile.first_name = user_profile.cleaned_data.get("first_name")
            profile.location = user_profile.cleaned_data.get("location")
            profile.email = user_profile.cleaned_data.get("email")
            profile.last_name = user_profile.cleaned_data.get("last_name")
            profile.save()
            return redirect('settings:profile')
        else:
            messages.error(request, _('please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user,
            initial={
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            })
        user = request.user
        profile = user.profile
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

    #def update_profile(request, user_id):
        #user = User.objects.get(pk=user_id)
        #user.profile.bio = 'lorem ipsum'
        #user.save()

    def logout_page(request, *args, **kwargs):
        from django.utils import timezone
        user = request.user
        profile = user.get_profile()
        profle.last_logout = timezone.now()
        profile.save()
        logout(request, *args, **kwargs)


class PaymentDetailsView(generic.TemplateView):
    template_name = 'checkout/payment_details.html'
    template_name_preview = 'checkout/preview.html'

    def handle_place_order_submission(self, request):
        return self.submit(**self.build_submission())

    def render_preview(self, request, **kwargs):
        self.preview = True
        ctx = self.get_context_data(**kwargs)
        return self.render_to_response(ctx)

    def submit(self, user, order_kwargs=None):
        if order_kwargs is None:
            order_kwargs = {}

        order_number = self.generate_order_number(basket)
        logger.info("Order #%s: beginning submission process #%d", order_number, basket.id)

        self.freeze_basket(basket)
        self.checkout_session.set_submitted_basket(basket)

    def get_template_names(self):
        return [self.template_name_preview] if self.preview else [
            self.template_name]


def post_buy(self, id):

    instance = get_object_or_404(Post, id=id)
    print(instance)
    #share_string = quote_plus(instance.description)
    #instance.user = request.user
    # messages.success(request, "successfully purchased")
    #context = {
        #"title": instance.title,
        #"instance": instance,
        #"share_string": share_string,
    #}
    return HttpResponseRedirect("/success/")
