# -*- coding: utf-8 -*-

from plone.app.contentlisting.interfaces import IContentListingObject
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.summary import BLACKLISTED_ATTRIBUTES
from plone.restapi.serializer.summary import DefaultJSONSummarySerializer
from plone.restapi.serializer.summary import FIELD_ACCESSORS
from zope.interface import implementer


@implementer(ISerializeToJsonSummary)
class OOSummarySerializer(DefaultJSONSummarySerializer):
    def __call__(self):
        obj = IContentListingObject(self.context)

        summary = {}
        for field in self.metadata_fields():
            if field.startswith("_") or field in BLACKLISTED_ATTRIBUTES:
                continue
            accessor = FIELD_ACCESSORS.get(field, field)
            if field in ("Title", "title"):
                # This condition is necessary because of the way the PST generate title
                value = getattr(self.context, accessor, None)
            else:
                value = getattr(obj, accessor, None)
            if callable(value):
                value = value()
            summary[field] = json_compatible(value)
        summary["original_title"] = getattr(self.context, "title", "")
        return summary
