User comments
=============

Prologue
--------

User comments adds model for commenting django model instances for example in the administration. It's simpler version of django-contrib-comments

Prerequisites
-------------

- skip-django-chamber~=0.6.16.3

Installation
------------

```python
pip install skip-django-user-comments
```

Configuration
-------------

For using django-user-comments you just add add ``user_comments`` to ``INSTALLED_APPS`` setting:

```python
INSTALLED_APPS = (
    ...
    'user_comments',
    ...
)
```

Django-is-core
--------------

You can use user comments with django-is-core framework:


```python
from is_core.main import UIRESTModelISCore
from user_comments.contrib.is_core.cores import CommentISCoreMixin


class UserCore(CommentISCoreMixin, DjangoUiRestCore):

    model = User
    form_fieldsets = (
         (None, {
            'fields': 'username', 'first_name', 'last_name'
         })
    ) + CommentCoreMixin.notes_form_fieldset

```

The CommentISCoreMixin only sets ``form_class`` attribute and contains ``notes_form_fieldset`` setting.

If you need change form of the core. You must extend from ``user_comments.contrib.is_core.cores.CommentUIForm``

```python
from user_comments.contrib.is_core.cores import CommentUiForm

e
class UserForm(CommentUiForm):
    ...


class UserCore(CommentCoreMixin, DjangoUiRestCore):

    model = User
    form_class = UserForm
    form_fieldsets = (
         (None, {
            'fields': 'username', 'first_name', 'last_name'
         })
    ) + CommentCoreMixin.notes_form_fieldset

```