from rest_framework import viewsets, permissions, serializers
from .models import User, Task, Permission
from .serializers import UserSerializer, TaskSerializer, PermissionSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        
        assigned_to_user = serializer.validated_data.get('assigned_to')
       
        creator = self.request.user

        # --- THE CORE LOGIC STARTS HERE ---
        try:
            # Find the permission rule for the person creating the task.
            creator_permission = Permission.objects.get(designation_level=creator.designation_level)
        except Permission.DoesNotExist:
            # If no rule exists for this user's level, they can't assign tasks.
            raise serializers.ValidationError("You do not have a permission level set and cannot assign tasks.")

        # 1. Check the master switch: Can this user assign tasks at all?
        if not creator_permission.can_assign:
            raise serializers.ValidationError("Your permission level does not allow you to assign tasks.")

        # 2. Check the hierarchy rule: Can they assign to this specific user?
        if creator.designation_level < assigned_to_user.designation_level:
            # Creator is a lower level than the assignee. This is never allowed.
            raise serializers.ValidationError("You cannot assign tasks to a user with a higher designation level.")

        # 3. Check the same-level rule.
        if creator.designation_level == assigned_to_user.designation_level:
            if not creator_permission.can_assign_to_same_level:
                # If they are the same level, check the specific permission for that.
                raise serializers.ValidationError("You do not have permission to assign tasks to users at the same level.")
        
        # If all checks pass, we proceed with the default behavior:
        # Save the task, but also ensure the 'created_by' field is correctly set to the current user.
        serializer.save(created_by=creator)

    # We also need to protect against updates.
    # This logic is very similar to perform_create.
    def perform_update(self, serializer):
        # This logic would be duplicated here. For a real-world app, you would refactor this
        # into a shared function to avoid repeating code. But for clarity, we show it here.
        assigned_to_user = serializer.validated_data.get('assigned_to', self.get_object().assigned_to)
        updater = self.request.user

        try:
            updater_permission = Permission.objects.get(designation_level=updater.designation_level)
        except Permission.DoesNotExist:
            raise serializers.ValidationError("You do not have a permission level set and cannot assign tasks.")

        if not updater_permission.can_assign:
            raise serializers.ValidationError("Your permission level does not allow you to re-assign tasks.")

        if updater.designation_level < assigned_to_user.designation_level:
            raise serializers.ValidationError("You cannot assign tasks to a user with a higher designation level.")

        if updater.designation_level == assigned_to_user.designation_level:
            if not updater_permission.can_assign_to_same_level:
                raise serializers.ValidationError("You do not have permission to assign tasks to users at the same level.")

        # If all checks pass, save the update.
        serializer.save()