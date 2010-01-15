# python imports
import datetime

# django imports
from django import forms
from django.db import models
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

# tagging imports
import tagging.models
from tagging.forms import TagField

# portlets imports
from portlets.models import Portlet
from portlets.utils import register_portlet

# lfc imports
from lfc.utils.registration import register_content_type
from lfc.utils.registration import register_sub_type_to
from lfc.utils.registration import register_template
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
        from lfc_blog.models import BlogEntry
        obj = context.get("lfc_context")
        request = context.get("request")

        # Urgh! Ugly hack.
        if isinstance(obj, BlogEntry):
            obj = obj.parent

        now = datetime.datetime.now()

        entries = obj.sub_objects.restricted(request)[:self.limit]

        months = []
        for i in range(12, 0, -1):
            month = (now.month+i) % 12
            if month == 0:
                month = 12
            temp = obj.sub_objects.restricted(request).filter(
                language__in = (translation.get_language(), "0"),
                creation_date__month=month)
            amount = temp.count()
            if amount:
                months.append({
                    "name" : _(datetime.date(now.year, month, 1).strftime('%B')),
                    "amount" : amount,
                    "number" : month,
                })
        
        # TODO: Use restricted manager here
        cloud = tagging.models.Tag.objects.cloud_for_model(
            BlogEntry, filters={
                "parent" : obj,
                "active" : True,
            })

        return render_to_string("lfc_blog/blog_portlet.html", {
            "page" : obj,
            "title" : self.title,
            "entries" : entries,
            "months" : months,
            "year" : now.year,
            "cloud" : cloud,
        })

    def form(self, **kwargs):
        """
        """
        return BlogPortletForm(instance=self, **kwargs)

class BlogPortletForm(forms.ModelForm):
    """Form for the BlogPortlet.
    """
    class Meta:
        model = BlogPortlet

from django.db.models.signals import post_syncdb

def register(sender, **kwargs):

    # Register Portlets
    register_portlet(BlogPortlet, "Blog")
    
    # Register Templates
    register_template(name = _(u"Blog"), file_name="blog.html")
    register_template(name = _(u"Blog Entry"), file_name="blog_entry.html")

    # Register objects
    register_content_type(obj = Blog, name = "Blog", sub_types = ["BlogEntry"], templates=["Blog"], default_template="Blog")
    register_content_type(obj = BlogEntry, name = "Blog Entry", templates=["Blog Entry"], default_template="Blog Entry")

    # Register Blog as a sub type of Page
    register_sub_type_to("Page", obj=Blog)

post_syncdb.connect(register)