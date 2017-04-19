from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.forms import ModelForm, Textarea, forms

# Create your models here.
class PostManager(models.Manager):
    def all(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    # filename, extension = filename.split(".")
    # return "%s/%s.%s" %(instance.id, instance.id, extension)
    return "%s/%s" % (instance.id, filename)




class Post(models.Model):
    STATUS_CHOICES =(
        ('b', 'buy'),
        ('k', 'booked'),
        ('s', 'sold'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, null=True)
    title = models.CharField(max_length=120)
    status = models.CharField(max_length=1, default=STATUS_CHOICES[2][1], choices=STATUS_CHOICES)
    product = models.ForeignKey('product', default=1, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=100, default=0)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
                              null=True,
                              blank=True,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    Quantity = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    active = models.BooleanField(default=True)


    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title



    def get_absolute_url(self):
        #return reverse("posts:detail", kwargs={"id": self.id})
        return "/posts/%s/" %(self.id)

class Product(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.product

    class Meta:
        ordering = ('first_name',)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(auto_now_add=True)
    url = models.URLField(max_length=200, blank=True)
    company = models.TextField(max_length=200, blank=True)
    #user_posts = models.ForeignKey(Post, blank=True, null=True)


    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
        #profile.save()
#User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u) [0])


    # objects = PostManager()

    #class Meta:
        #ordering = ["-timestamp", "-updated"]


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)




class EventHandler(object):
    #def __init__(self, user=None):
        #self.user = user

    def handle_shipping_event(self, order, event_type, lines, line_quantities, **kwargs):
        self.validate_shipping_event(
            order, event_type, lines, line_quantities, **kwargs)
        return self.create_shipping_event(
            order, event_type, lines, line_quantities, **kwargs)

        self.validate_shipping_event(
            order, event_type, lines, line_quantities, **kwargs
        )

    def handle_payment_event(self, order, event_type, amount, lines=None, line_quantities=None, **kwargs):

        self.validate_payment_event(
            order, event_type, amount, lines, line_quantities, **kwargs)
        return self.create_payment_event(order, event_type, amount, lines, line_quantities, **kwargs)

    def handle_order_status_change(self, order, new_status, note_msg=None):
        order.set_status(new_status)
        if note_msg:
            self.create_note(order, note_msg)

    def validate_shipping_event(self, order, event_type, lines, line_quantities, **kwargs):
        erors = []
        for line, qty in zip(lines, line_quantities):
            if not lines.is_shipping_event_permitted(event_type, qty):
                msg = _("the selected quantity for line #%(line_id)s is too large")% {'line_id': line.id}
                errors.appending(msg)
        if errors:
            raise exceptions.InvalidShippingEvent(",".join(errors))
    def create_shipping_event(self, order, event_type, lines, line_quantities, **kwargs):
        reference = kwargs.get('reference', '')
        event = order.shipping_events.create( event_type=event_type, notes=reference)
        try:
            for line, quantities in zip(lines, line_quantities):
                event.line._quantites.create( line=line, quantity=quantity)
        except exceptions.InvalidShippingEvent:
            event.delete()
            raise
        return event

    def create_payment_event(self, order, event_type, amount, lines=None, line_quantites=None, **kwargs):
        reference = kwargs.get('reference', "")
        event = order.payment_events.create(
            event_type=event_type, amount=amount, reference=reference)
        if lines and line_quantites:
            for line, quantity in zip(lines, line_quantites):
                event.line_quantites.create(
                    line=line, quantity=quantity)
                return event

    def submit(self, user, basket, order):
        if order_kwargs is None:
            order_kwargs = {}






#class Order(models.model):
