from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy

from chamber.models import SmartModel


class CommentQuerySet(models.QuerySet):

    def filter_for_object(self, obj):
        return self.filter(
            content_type=ContentType.objects.get_for_model(obj),
            object_pk=obj.id
        )


class Comment(SmartModel):

    objects = CommentQuerySet.as_manager()

    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=ugettext_lazy('author'), on_delete=models.CASCADE,
                               null=False, blank=False, db_index=True)
    comment = models.TextField(verbose_name=ugettext_lazy('comment'), null=False, blank=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_pk = models.TextField(db_index=True)
    content_object = GenericForeignKey('content_type', 'object_pk')
    content_object.verbose_name = ugettext_lazy('object')

    class Meta:
        verbose_name = ugettext_lazy('comment')
        verbose_name_plural = ugettext_lazy('comments')
        ordering = ('-created_at',)
