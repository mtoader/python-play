from django.conf.urls import patterns, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'python_play.views.home', name='home'),
    # url(r'^python_play/', include('python_play.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

    url(r'^accounts/login/?$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/?$', 'django.contrib.auth.views.logout'),
    url(r'^lists/?$', 'todo.views.lists'),
    url(r'^lists/new?$', 'todo.views.list_new'),
    url(r'^lists/(?P<list_id>\d+)/?$', 'todo.views.list'),
    url(r'^lists/delete', 'todo.views.list_delete'),
    url(r'^lists/rename', 'todo.views.list_rename'),
    url(r'^$', 'todo.views.lists'),
)

