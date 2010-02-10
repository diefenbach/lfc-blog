# django imports
from django.conf.urls.defaults import *

urlpatterns = patterns("lfc_blog.views",
    url(r'^(?P<language>[-\w]{2})/(?P<slug>.+)/tag/(?P<tag>[^/]+)$', "lfc_tagged_object_list", name="lfc_blog_tag_list"),
    url(r'^(?P<slug>.+)/tag/(?P<tag>[^/]+)$', "lfc_tagged_object_list", name="lfc_blog_tag_list"),
    url(r'^(?P<language>[-\w]{2})/(?P<slug>.+)/archive/(?P<month>\d{1,2})/(?P<year>\d{4})$', "archive", name="lfc_archive"),
    url(r'^(?P<slug>.+)/archive/(?P<month>\d{1,2})/(?P<year>\d{4})$', "archive", name="lfc_archive"),
)