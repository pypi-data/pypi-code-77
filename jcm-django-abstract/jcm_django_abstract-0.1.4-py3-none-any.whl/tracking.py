from django.db import models
from django.utils import timezone
from django.conf import settings


class AbstractCreateUpdateTime(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractCreateUpdateUser(AbstractCreateUpdateTime):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name="%(app_label)s_%(class)s_created_by",
                                   related_query_name="%(app_label)s_%(class)ss",)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name="%(app_label)s_%(class)s_updated_by",
                                   related_query_name="%(app_label)s_%(class)ss",)

    class Meta:
        abstract = True


class AbstractDeleteTime(AbstractCreateUpdateTime):
    deleted_time = models.DateTimeField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        self.is_deleted_prior = self.is_deleted
        super().__init__(self, *args, **kwargs)

    def save(self, *args, **kwargs):

        # Toggle Deleted Time Based on Flag
        if self.is_deleted and not self.is_deleted_prior:
            self.deleted_time = timezone.now()
        elif not self.is_deleted and self.deleted_time:
            self.deleted_time = None

        super().save(self, *args, **kwargs)

    class Meta:
        abstract = True


class AbstractDeleteUser(AbstractDeleteTime, AbstractCreateUpdateTime):
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name="%(app_label)s_%(class)s_deleted_by",
                                   related_query_name="%(app_label)s_%(class)ss",)

    class Meta:
        abstract = True
