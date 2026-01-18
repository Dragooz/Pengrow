from rest_framework import permissions
from .models import ProjectMembership


class IsReporter(permissions.BasePermission):
    """
    Permission to check if user is a REPORTER in the project.
    Used for creating appraisals and reviews.
    """

    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True

        # For write operations, check if user is a reporter in any project
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow safe methods for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if user is a reporter in the related project
        user = request.user

        # Handle different object types
        if hasattr(obj, 'project'):
            project = obj.project
        elif hasattr(obj, 'appraisal'):
            project = obj.appraisal.project
        else:
            return False

        # Check if user is a REPORTER in this project
        is_reporter = ProjectMembership.objects.filter(
            project=project,
            user=user,
            role='REPORTER'
        ).exists()

        return is_reporter or user.is_staff


class IsSameProject(permissions.BasePermission):
    """
    Permission to ensure reviewer can only appraise users in the same project.
    Business rule: Users can only be appraised by reporters in projects they both belong to.
    """

    message = "You can only appraise users in projects where you are both members."

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Staff can access everything
        if user.is_staff:
            return True

        # For appraisals, check if reviewer and appraisee are in same project
        if hasattr(obj, 'appraisee') and hasattr(obj, 'project'):
            # Check if reviewer is in the project
            reviewer_in_project = ProjectMembership.objects.filter(
                project=obj.project,
                user=user
            ).exists()

            # Check if appraisee is in the project
            appraisee_in_project = ProjectMembership.objects.filter(
                project=obj.project,
                user=obj.appraisee
            ).exists()

            return reviewer_in_project and appraisee_in_project

        # For reviews, check the appraisal's project
        if hasattr(obj, 'appraisal'):
            return self.has_object_permission(request, view, obj.appraisal)

        return False


class CanCreateAppraisal(permissions.BasePermission):
    """
    Permission to check if user can create an appraisal.
    Validates that:
    1. User is a REPORTER in the specified project
    2. Appraisee is a member of the specified project
    """

    message = "You must be a REPORTER in the project and the appraisee must be a member of that project."

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # For creation, check the data being submitted
        if request.method == 'POST':
            project_id = request.data.get('project')
            appraisee_id = request.data.get('appraisee')

            if not project_id or not appraisee_id:
                return False

            # Check if user is a REPORTER in the project
            is_reporter = ProjectMembership.objects.filter(
                project_id=project_id,
                user=request.user,
                role='REPORTER'
            ).exists()

            # Check if appraisee is a member of the project
            appraisee_in_project = ProjectMembership.objects.filter(
                project_id=project_id,
                user_id=appraisee_id
            ).exists()

            return (is_reporter and appraisee_in_project) or request.user.is_staff

        return True
