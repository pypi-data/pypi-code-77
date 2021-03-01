# -*- coding: utf-8 -*-

from imio.restapi.serializer.base import SerializeToJson
from plone.app.contentlisting.interfaces import IContentListingObject
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.serializer.converters import json_compatible
from plone.restapi.serializer.summary import BLACKLISTED_ATTRIBUTES
from plone.restapi.serializer.summary import DefaultJSONSummarySerializer
from plone.restapi.serializer.summary import FIELD_ACCESSORS
from zope.component import queryMultiAdapter
from zope.interface import implementer


@implementer(ISerializeToJson)
class ActionSerializer(SerializeToJson):
    def __call__(self, *args, **kwargs):
        result = super(ActionSerializer, self).__call__(*args, **kwargs)
        result["operational_objective"] = self.get_oo()
        result["strategic_objective"] = self.get_os()
        return result

    def get_oo(self):
        """Return the serialized parent that is the Operational Objective"""
        return queryMultiAdapter(
            (self.context.aq_parent, self.request), ISerializeToJsonSummary,
        )()

    def get_os(self):
        """Return the serialized parent of the parent that is the Strategic Objective"""
        return queryMultiAdapter(
            (self.context.aq_parent.aq_parent, self.request), ISerializeToJsonSummary,
        )()


@implementer(ISerializeToJsonSummary)
class ActionSummarySerializer(DefaultJSONSummarySerializer):
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
