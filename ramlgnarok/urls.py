from django.conf.urls import url

from ramlgnarok.views import RAMLDocs


urlpatterns = [
    url(r'docs/(?P<raml_file>\w+)/$', RAMLDocs.as_view()),
    url(
        r'docs/(?P<raml_file>\w+)/(?P<override_file>\w+)/$',
        RAMLDocs.as_view()
    ),
]
