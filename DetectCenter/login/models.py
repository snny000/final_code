from django.db import models
from django.contrib.auth.models import AbstractUser, Group


class User(AbstractUser):
    last_update_time = models.DateTimeField(auto_now_add=True)

    class Meta(AbstractUser.Meta):
        pass


# class Group(Group):
#     remarks = models.TextField()
#
#     class Meta:
#         db_table = 'auth_group'
