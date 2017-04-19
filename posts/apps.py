from __future__ import unicode_literals

from django.apps import AppConfig


class PostsConfig(AppConfig):
    name = 'posts'


    def ready(self):
        from django_fsm.signals import post_transition
        post_transition.connect(order_event_notification)


def order_event_notification(sender, instance=None, target=None, **kwargs):
    if target == 'payment confirmed':
