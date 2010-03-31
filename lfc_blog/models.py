# python imports
import datetime

# django imports
from django import forms
from django.core.cache import cache
from django.db import models
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

# tagging imports
import tagging.models
from tagging.forms import TagField

# portlets imports
from portlets.models import Portlet

# lfc imports
import lfc.utils
from lfc.fields.autocomplete import AutoCompleteTagInput
from lfc.models import BaseContent

class Blog(BaseContent):
    """A simple blog for LFC.
    """
    text = models.TextField(_(u"Text"), blank=True)

    def get_searchable_text(self):
        searchable_text = super(Blog, self).get_searchable_text()
        return searchable_text + " " + self.text

    def form(self, **kwargs):
        """Returns the add/edit form of the Blog
        """
        return BlogForm(**kwargs)

class BlogForm(forms.ModelForm):
    """The add/edit form of the Blog content object
    """
    class Meta:
        model = Blog
        fields = ("title", "display_title", "slug", "description", "text")

class BlogEntry(BaseContent):
    """An entry of an blog
    """
    text = models.TextField(_(u"Text"), blank=True)

    def get_searchable_text(self):
        searchable_text = super(BlogEntry, self).get_searchable_text()
        return searchable_text + " " + self.text

    def form(self, **kwargs):
        """Returns the add/edit form of the BlogEntry
        """
        return BlogEntryForm(**kwargs)

class BlogEntryForm(forms.ModelForm):
    """The add/edit form of the Blog content object
    """
    tags = TagField(widget=AutoCompleteTagInput(), required=False)
    class Meta:
        model = BlogEntry
        fields = ("title", "display_title", "slug", "description", "text", "tags")

class BlogPortlet(Portlet):
    """A portlet, which displays recent entries, archive and tag cloud.
    """
    limit = models.IntegerField(default=5)

    def __unicode__(self):
        return "%s" % self.id

    def render(self, context):
        """Renders the portlet as html.
        """
        cache_key = "portlet-blog"
        result = cache.get(cache_key)
        if result:
            return result

        from lfc_blog.models import BlogEntry
        obj = context.get("lfc_context")
        request = context.get("request")

        # Urgh! Ugly hack.
        if isinstance(obj, BlogEntry):
            obj = obj.parent

        now = datetime.datetime.now()
        entries = obj.get_children()[:self.limit]

        months = []
        for i in range(12, 0, -1):
            month = (now.month+i) % 12
            if month == 0:
                month = 12

            amount = 0
            for t in obj.children.all().filter(
                language__in = (translation.get_language(), "0"),
                publication_date__month=month):
                if t.has_permission(request.user, "view"):
                    amount += 1

            if amount:
                months.append({
                    "name" : _(datetime.date(now.year, month, 1).strftime('%B')),
                    "amount" : amount,
                    "number" : month,
                })

        cloud = tagging.models.Tag.objects.cloud_for_model(
            BlogEntry, filters = {
                "parent" : obj,
            })

        result = render_to_string("lfc_blog/blog_portlet.html", {
            "page" : obj,
            "title" : self.title,
            "entries" : entries,
            "months" : months,
            "year" : now.year,
            "cloud" : cloud,
        })

        cache.set(cache_key, result)
        return result

    def form(self, **kwargs):
        """
        """
        return BlogPortletForm(instance=self, **kwargs)

class BlogPortletForm(forms.ModelForm):
    """Form for the BlogPortlet.
    """
    class Meta:
        model = BlogPortlet