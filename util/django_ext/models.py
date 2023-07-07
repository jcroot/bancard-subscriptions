from django.db import models
from django.forms.models import model_to_dict


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ModelDiffMixin:
    """
    A model mixin that tracks model fields' values and provide some useful api
    to know what fields have been changed.
    """
    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self._original_values = self.get_fields_as_dict()

    @property
    def diff(self):
        d1 = self._original_values
        d2 = self.get_fields_as_dict()
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return list(self.diff.keys())

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        super(ModelDiffMixin, self).save(*args, **kwargs)
        self._original_values = self.get_fields_as_dict()

    def get_fields_as_dict(self):
        d = self.__dict__
        return model_to_dict(
            self,
            # In attempting to speed up the natixis report, I used some Django ORM features defer (to not load some
            # fields https://docs.djangoproject.com/en/3.0/ref/models/querysets/#defer) and only (to only load some
            # fields https://docs.djangoproject.com/en/3.0/ref/models/querysets/#only). In particular, I wanted to
            # use defer to not load credit reports, which is one of the most expensive operations we do, since they
            # end up parsing large XML documents. The ModelDiffMixin at the time didn't work with defer or only, but
            # that change fixed it.
            #
            # was: fields = [f.name for f in u._meta.fields]

            # fields=[field.name for field in self._meta.fields if hasattr(self, field.name)]
            fields=[field.name for field in self._meta.fields if field.name in d or '{}_id'.format(field.name) in d]
        )