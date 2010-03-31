# django imports
from django.utils.translation import ugettext_lazy as _

# lfc imports
from lfc.utils.registration import register_content_type
from lfc.utils.registration import unregister_content_type
from lfc.utils.registration import register_sub_type
from lfc.utils.registration import register_template
from lfc.utils.registration import unregister_template

# portlets imports
from portlets.utils import register_portlet
from portlets.utils import unregister_portlet

# lfc_blog imports
from lfc_blog.models import Blog
from lfc_blog.models import BlogPortlet
from lfc_blog.models import BlogEntry

name = "Blog"
description = _(u"A simple blog")

def install():
    """Installs the blog application.
    """
    # Register Portlets
    register_portlet(BlogPortlet, "Blog")

    # Register Templates
    register_template(name = "Blog", path="lfc/templates/blog.html")
    register_template(name = "Blog Entry", path="lfc/templates/blog_entry.html")

    # Register objects
    register_content_type(BlogEntry, name = "Blog Entry", templates=["Blog Entry"], default_template="Blog Entry", global_addable=False)
    register_content_type(Blog, name = "Blog", sub_types = ["BlogEntry"], templates=["Blog"], default_template="Blog")

    # Register Blog as a sub type of Page
    register_sub_type(Blog, "Page")

def uninstall():
    """Uninstalls the blog application.
    """
    # Unregister content type
    unregister_content_type("Blog")
    unregister_content_type("Blog Entry")

    # Unregister template
    unregister_template("Blog")
    unregister_template("Blog Entry")

    # Unregister portlet
    unregister_portlet(BlogPortlet)