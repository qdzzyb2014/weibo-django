from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^login/$', views.login, name='login'),
    url(r'^signin/$', views.register, name='signin'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^user/(?P<username>\w+)/$', views.user, name='user'),
    url(r'^edit-profile/$',
        views.edit_profile, name='edit_profile'),
    url(r'^post/(?P<id>\d+)', views.post, name='post')
]
