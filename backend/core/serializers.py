from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Company, User, Project, ProjectMembership,
    AppraisalCycle, Appraisal, AppraisalReview,
    CompetencyRating, OverallEvaluation
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'company', 'position', 'division', 'date_joined', 'last_promotion_date',
            'is_active', 'is_staff'
        ]
        read_only_fields = ['id', 'is_staff']

    def get_full_name(self, obj):
        return obj.get_full_name()


class CompanySerializer(serializers.ModelSerializer):
    """Company serializer"""
    class Meta:
        model = Company
        fields = ['id', 'name', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProjectSerializer(serializers.ModelSerializer):
    """Project serializer"""
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'company', 'company_name', 'name', 'description',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProjectMembershipSerializer(serializers.ModelSerializer):
    """Project membership serializer"""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)

    class Meta:
        model = ProjectMembership
        fields = [
            'id', 'project', 'project_name', 'user', 'user_name', 'user_email',
            'role', 'joined_at', 'created_at'
        ]
        read_only_fields = ['id', 'joined_at', 'created_at']


class AppraisalCycleSerializer(serializers.ModelSerializer):
    """Appraisal cycle serializer"""
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = AppraisalCycle
        fields = [
            'id', 'company', 'company_name', 'period_start', 'period_end',
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CompetencyRatingSerializer(serializers.ModelSerializer):
    """Competency rating serializer"""
    rating_display = serializers.CharField(source='get_rating_display', read_only=True)

    class Meta:
        model = CompetencyRating
        fields = [
            'id', 'appraisal_review', 'category', 'criterion_name',
            'rating', 'rating_display', 'comments', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class AppraisalReviewSerializer(serializers.ModelSerializer):
    """Appraisal review serializer"""
    reviewer_name = serializers.CharField(source='reviewer.get_full_name', read_only=True)
    competency_ratings = CompetencyRatingSerializer(many=True, read_only=True)

    class Meta:
        model = AppraisalReview
        fields = [
            'id', 'appraisal', 'reviewer', 'reviewer_name', 'is_completed',
            'reviewer_signature_base64', 'reviewer_signed_at',
            'competency_ratings', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class OverallEvaluationSerializer(serializers.ModelSerializer):
    """Overall evaluation serializer"""
    class Meta:
        model = OverallEvaluation
        fields = [
            'id', 'appraisal', 'overall_rating_avg',
            'ready_for_advanced_work', 'ready_for_promotion', 'summary_comment',
            'appraisee_signature_base64', 'appraisee_signed_at',
            'hr_signature_base64', 'hr_signed_at', 'finalized_at',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'overall_rating_avg', 'created_at', 'updated_at']


class AppraisalSerializer(serializers.ModelSerializer):
    """Appraisal serializer"""
    appraisee_name = serializers.CharField(source='appraisee.get_full_name', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    cycle_info = serializers.SerializerMethodField()
    reviews = AppraisalReviewSerializer(many=True, read_only=True)
    overall_evaluation = OverallEvaluationSerializer(read_only=True)

    class Meta:
        model = Appraisal
        fields = [
            'id', 'cycle', 'cycle_info', 'appraisee', 'appraisee_name',
            'project', 'project_name', 'discussion_date', 'status',
            'reviews', 'overall_evaluation', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_cycle_info(self, obj):
        return {
            'period_start': obj.cycle.period_start,
            'period_end': obj.cycle.period_end,
            'status': obj.cycle.status
        }


class AppraisalCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating appraisals"""
    class Meta:
        model = Appraisal
        fields = ['id', 'cycle', 'appraisee', 'project', 'discussion_date', 'status']
        read_only_fields = ['id']
