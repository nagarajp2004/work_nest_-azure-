from rest_framework import serializers

from .models import User, Task, Permission


class PermissionSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Permission # The model to serialize
        fields = '__all__' # This special value means "include all fields from the model".

# A serializer for our custom User model.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
      
        fields = ['id', 'username', 'email', 'designation_level']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
