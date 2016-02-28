from django import template
from ..models import Permission

register = template.Library()


@register.simple_tag
def user_can_follow(user):
    return user.can(Permission.FOLLOW)


@register.simple_tag
def is_following(current_user, user):
    return current_user.is_following(user)


@register.simple_tag
def follower_count(user):
    return user.follower.count()
