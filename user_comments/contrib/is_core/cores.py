from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy

from is_core.generic_views.inlines.inline_objects_views import TabularInlineObjectsView

from user_comments.models import Comment

from is_core.forms.models import SmartModelForm


class CommentUIForm(SmartModelForm):

    comment = forms.CharField(label=ugettext_lazy('add comment'), required=False, widget=forms.Textarea())

    def _post_save(self, obj):
        super()._post_save(obj)
        comment = self.cleaned_data.get('comment')
        if comment:
            Comment.objects.create(
                content_object=obj,
                author=self._request.user,
                comment=comment
            )


class CommentObjectsView(TabularInlineObjectsView):

    model = Comment
    fields = (
        ('author', ugettext_lazy('Author')),
        ('created_at', ugettext_lazy('Created at')),
        ('comment', ugettext_lazy('Comment')),
    )

    def get_objects(self):
        return self.model.objects.filter(
            content_type=ContentType.objects.get_for_model(self.parent_instance),
            object_pk=self.parent_instance.pk
        )


class CommentISCoreMixin:

    form_class = CommentUIForm

    notes_form_fieldset = (
        (ugettext_lazy('Comments'), {
            'fieldsets': (
                (None, {'inline_view': CommentObjectsView}),
                (None, {'fields': ('comment',)}),
            )
        }),
    )
