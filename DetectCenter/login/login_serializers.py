from rest_framework import serializers
from models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'last_update_time', 'last_login', 'date_joined', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser')