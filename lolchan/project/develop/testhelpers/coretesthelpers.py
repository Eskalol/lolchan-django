import uuid
from django.db import IntegrityError
from django.contrib.auth import get_user_model

from lolchan.lolchan_core import models as coremodels


def create_user(email, password='test', **kwargs):
    """
    Create a user with the given ``email``.

    Parameters:
        email: The email of the user.
        password: Defaults to ``test``.
        kwargs: Extra kwargs to ``User.objects.create``.

    Examples::

        from lolchan.project.develop.testhelpers import coretesthelpers
        myuser = coretesthelpers.('myuser', fullname="My User")
    """
    user = get_user_model().objects.create(email=email, **kwargs)
    user.set_password(password)
    user.save()
    return user


def create_random_user():
    """
    Create a user with a random email. Perfect for tests where you just need to
    set a user on some data model, but the user is not used for anything.
    """
    try:
        user = get_user_model().objects.create(
            email='{}@example.com'.format(uuid.uuid4()))
    except IntegrityError:
        return create_random_user()
    else:
        user.set_password('test')
        user.save()
        return user

