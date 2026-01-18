from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    Company, User, Project, ProjectMembership,
    AppraisalCycle, Appraisal, AppraisalReview,
    CompetencyRating, OverallEvaluation
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'company', 'position', 'is_staff']
    list_filter = ['is_staff', 'is_active', 'company']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Company Info', {'fields': ('company', 'position', 'division', 'last_promotion_date')}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Company Info', {'fields': ('company', 'position', 'division')}),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'is_active', 'created_at']
    list_filter = ['company', 'is_active', 'created_at']
    search_fields = ['name', 'company__name']


@admin.register(ProjectMembership)
class ProjectMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'role', 'joined_at']
    list_filter = ['role', 'project', 'joined_at']
    search_fields = ['user__username', 'user__email', 'project__name']


@admin.register(AppraisalCycle)
class AppraisalCycleAdmin(admin.ModelAdmin):
    list_display = ['company', 'period_start', 'period_end', 'status', 'created_at']
    list_filter = ['status', 'company', 'period_start']
    search_fields = ['company__name']
    date_hierarchy = 'period_start'


@admin.register(Appraisal)
class AppraisalAdmin(admin.ModelAdmin):
    list_display = ['appraisee', 'project', 'cycle', 'status', 'discussion_date']
    list_filter = ['status', 'project', 'cycle']
    search_fields = ['appraisee__username', 'appraisee__email', 'project__name']
    date_hierarchy = 'discussion_date'


@admin.register(AppraisalReview)
class AppraisalReviewAdmin(admin.ModelAdmin):
    list_display = ['appraisal', 'reviewer', 'is_completed', 'reviewer_signed_at']
    list_filter = ['is_completed', 'reviewer_signed_at']
    search_fields = ['appraisal__appraisee__username', 'reviewer__username']
    readonly_fields = ['reviewer_signature_base64']


@admin.register(CompetencyRating)
class CompetencyRatingAdmin(admin.ModelAdmin):
    list_display = ['appraisal_review', 'category', 'criterion_name', 'rating']
    list_filter = ['category', 'rating']
    search_fields = ['criterion_name', 'appraisal_review__appraisal__appraisee__username']


@admin.register(OverallEvaluation)
class OverallEvaluationAdmin(admin.ModelAdmin):
    list_display = [
        'appraisal', 'overall_rating_avg',
        'ready_for_advanced_work', 'ready_for_promotion', 'finalized_at'
    ]
    list_filter = ['ready_for_advanced_work', 'ready_for_promotion', 'finalized_at']
    search_fields = ['appraisal__appraisee__username']
    readonly_fields = ['overall_rating_avg', 'appraisee_signature_base64', 'hr_signature_base64']
