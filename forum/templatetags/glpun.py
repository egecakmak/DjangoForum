from django import template
from forum.models import Post

register = template.Library()

@register.simple_tag
def get_last_posts_users_name(thread_arg):
    if Post.objects.all().filter(thread=thread_arg).last() is not None:
        return Post.objects.all().filter(thread=thread_arg).last().user.username
