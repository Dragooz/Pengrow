from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    AuthViewSet, CompanyViewSet, UserViewSet, ProjectViewSet,
    ProjectMembershipViewSet, AppraisalCycleViewSet, AppraisalViewSet,
    AppraisalReviewViewSet, CompetencyRatingViewSet, OverallEvaluationViewSet
)

router = DefaultRouter()

# Auth endpoints
router.register(r'auth', AuthViewSet, basename='auth')

# Core endpoints
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'project-memberships', ProjectMembershipViewSet, basename='project-membership')

# Appraisal endpoints
router.register(r'appraisal-cycles', AppraisalCycleViewSet, basename='appraisal-cycle')
router.register(r'appraisals', AppraisalViewSet, basename='appraisal')
router.register(r'appraisal-reviews', AppraisalReviewViewSet, basename='appraisal-review')
router.register(r'competency-ratings', CompetencyRatingViewSet, basename='competency-rating')
router.register(r'overall-evaluations', OverallEvaluationViewSet, basename='overall-evaluation')

urlpatterns = [
    path('', include(router.urls)),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
