# python imports
import datetime

# django imports
from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

# tagging imports
from tagging.models import TaggedItem
from tagging.utils import get_tag

# lfc_blog imports
from lfc_blog.models import Blog
from lfc_blog.models import BlogEntry

def archive(request, slug, month, year, template_name="lfc_blog/archive.html"):
    """Display blog entries for given month, year and language.
    """
    entries = BlogEntry.objects.filter(
        parent__slug=slug,
        active=True,
        language__in=(translation.get_language(), "0"),
        creation_date__month=month,
        creation_date__year=year,
    )

    return render_to_response(template_name, RequestContext(request, {
        "blog" : Blog.objects.get(slug=slug),
        "month" : _(datetime.date(int(year), int(month), 1).strftime('%B')),
        "year" : year,
        "entries" : entries
    }))

def lfc_tagged_object_list(request, slug, tag, template_name="lfc_blog/tag.html"):
    """
    """
    if tag is None:
        raise AttributeError(_('tagged_object_list must be called with a tag.'))

    tag_instance = get_tag(tag)
    if tag_instance is None:
        raise Http404(_('No Tag found matching "%s".') % tag)

    try:
        blog = Blog.objects.get(slug=slug)
    except Blog.DoesNotExist:
        raise Http404()
    else:
        queryset = BlogEntry.objects.filter(parent=blog)
        entries = TaggedItem.objects.get_by_model(queryset, tag_instance)

    return render_to_response(template_name, RequestContext(request, {
        "slug"    : slug,
        "blog"   : blog,
        "entries" : entries,
        "tag"     : tag,
    }));