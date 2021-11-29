from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy

from is_core.generic_views.inlines.inline_objects_views import TabularInlineObjectsView

from user_comments.models import Comment

from is_core.forms.models import SmartModelForm
from is_core.generic_views.detail_views import DjangoDetailFormView


class CommentUiForm(SmartModelForm):

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


class DetailCommentFormView(DjangoDetailFormView):

    def get_readonly_fields(self):
        return (
            tuple(field for field in super().get_fields() if field != 'comment')
            if self.core.get_can_update_only_comment(self.request, obj=self.get_obj())
            else super().get_readonly_fields()
        )


class CommentCoreMixin:

    form_class = CommentUiForm
    ui_detail_view = DetailCommentFormView

    notes_fieldset = (
        (ugettext_lazy('Comments'), {
            'fieldsets': (
                (None, {'inline_view': CommentObjectsView}),
                (None, {'fields': ('comment',)}),
            )
        }),
    )

    def get_can_update_only_comment(self, request, obj=None):
        return hasattr(self, 'can_update_only_comment') and self.can_update_only_comment
