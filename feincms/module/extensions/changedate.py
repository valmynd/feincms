# ------------------------------------------------------------------------
# coding=utf-8
# ------------------------------------------------------------------------
"""
Track the modification date for pages.
"""

from django.db import models
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _

def pre_save_handler(sender, instance, **kwargs):
    """
    Intercept attempts to save and insert the current date and time into
    creation and modification date fields.
    """
    from datetime import datetime

    now = datetime.now()
    if instance.id is None:
        instance.creation_date = now
    instance.modification_date = now

# ------------------------------------------------------------------------
def register(cls, admin_cls):
    cls.add_to_class('creation_date',     models.DateTimeField(_('creation date'),     null=True, editable=False))
    cls.add_to_class('modification_date', models.DateTimeField(_('modification date'), null=True, editable=False))

    if hasattr(cls, 'cache_key_components'):
        cls.cache_key_components.append(lambda page: page.modification_date and page.modification_date.strftime('%s'))

    if hasattr(cls, 'last_modified'):
        cls.last_modified = lambda p: p.modification_date

    pre_save.connect(pre_save_handler, sender=cls)

# ------------------------------------------------------------------------
def last_modified_response_processor(self, request, response):
    from time import mktime
    from django.utils.http import http_date

    response['Last-Modified'] = http_date(mktime(self.modification_date.timetuple()))

# ------------------------------------------------------------------------
