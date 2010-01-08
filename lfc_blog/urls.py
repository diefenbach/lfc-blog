# django imports
from django.conf.urls.defaults import *

urlpatterns = patterns("lfc_blog.views",
    url(r'tag/(?P<slug>[-\w]+)/(?P<tag>[^/]+)/$', "lfc_tagged_object_list", name="lfc_blog_tag_list"),
    url(r'^archive/(?P<slug>[-\w]+)/(?P<month>\d{1,2})/(?P<year>\d{4})/$', "archive", name="lfc_archive"),
)

    