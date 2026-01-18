from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import (
    Company, User, Project, ProjectMembership,
    AppraisalCycle, Appraisal, AppraisalReview,
    CompetencyRating, OverallEvaluation
)
from .serializers import (
    CompanySerializer, UserSerializer, ProjectSerializer,
    ProjectMembershipSerializer, AppraisalCycleSerializer,
    AppraisalSerializer, AppraisalCreateSerializer,
    AppraisalReviewSerializer, CompetencyRatingSerializer,
    OverallEvaluationSerializer
)
from .permissions import IsReporter, IsSameProject, CanCreateAppraisal


class AuthViewSet(viewsets.GenericViewSet):
    """
    Authentication ViewSet for login, logout, and current user
    """
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login user and return JWT tokens"""
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {'error': 'Please provide both username and password'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        })

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """Logout user (blacklist refresh token)"""
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Get current user"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CompanyViewSet(viewsets.ReadOnlyModelViewSet):
    """Company ViewSet - read-only for now"""
    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """User ViewSet - read-only"""
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """Project ViewSet"""
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter projects by user's company"""
        user = self.request.user
        if user.is_staff:
            return Project.objects.filter(is_active=True)
        return Project.objects.filter(company=user.company, is_active=True)

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of a project"""
        project = self.get_object()
        memberships = ProjectMembership.objects.filter(project=project)
        serializer = ProjectMembershipSerializer(memberships, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reporters(self, request, pk=None):
        """Get all reporters of a project"""
        project = self.get_object()
        memberships = ProjectMembership.objects.filter(
            project=project,
            role='REPORTER'
        )
        serializer = ProjectMembershipSerializer(memberships, many=True)
        return Response(serializer.data)


class ProjectMembershipViewSet(viewsets.ModelViewSet):
    """Project Membership ViewSet"""
    queryset = ProjectMembership.objects.all()
    serializer_class = ProjectMembershipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter memberships by user's projects"""
        user = self.request.user
        if user.is_staff:
            return ProjectMembership.objects.all()
        return ProjectMembership.objects.filter(user=user)


class AppraisalCycleViewSet(viewsets.ModelViewSet):
    """Appraisal Cycle ViewSet"""
    queryset = AppraisalCycle.objects.all()
    serializer_class = AppraisalCycleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter cycles by user's company"""
        user = self.request.user
        if user.is_staff:
            return AppraisalCycle.objects.all()
        return AppraisalCycle.objects.filter(company=user.company)


class AppraisalViewSet(viewsets.ModelViewSet):
    """Appraisal ViewSet with permissions"""
    queryset = Appraisal.objects.all()
    permission_classes = [permissions.IsAuthenticated, CanCreateAppraisal, IsSameProject]

    def get_serializer_class(self):
        """Use different serializers for create vs list/retrieve"""
        if self.action == 'create':
            return AppraisalCreateSerializer
        return AppraisalSerializer

    def get_queryset(self):
        """Filter appraisals based on user's role"""
        user = self.request.user

        if user.is_staff:
            return Appraisal.objects.all()

        # Get projects where user is a member
        user_projects = ProjectMembership.objects.filter(user=user).values_list('project', flat=True)

        # Return appraisals for those projects
        return Appraisal.objects.filter(project__in=user_projects)

    def perform_create(self, serializer):
        """Create appraisal and associated review for the creator"""
        appraisal = serializer.save()

        # Create AppraisalReview for the creator (reporter)
        AppraisalReview.objects.create(
            appraisal=appraisal,
            reviewer=self.request.user
        )

        # Create OverallEvaluation
        OverallEvaluation.objects.create(appraisal=appraisal)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for an appraisal"""
        appraisal = self.get_object()
        reviews = AppraisalReview.objects.filter(appraisal=appraisal)
        serializer = AppraisalReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class AppraisalReviewViewSet(viewsets.ModelViewSet):
    """Appraisal Review ViewSet"""
    queryset = AppraisalReview.objects.all()
    serializer_class = AppraisalReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsReporter]

    def get_queryset(self):
        """Filter reviews by user"""
        user = self.request.user
        if user.is_staff:
            return AppraisalReview.objects.all()

        # Return reviews where user is the reviewer or appraisee
        return AppraisalReview.objects.filter(reviewer=user) | \
               AppraisalReview.objects.filter(appraisal__appraisee=user)

    def perform_update(self, serializer):
        """Update review and recalculate overall evaluation"""
        review = serializer.save()

        # Recalculate and update overall evaluation
        if hasattr(review.appraisal, 'overall_evaluation'):
            overall_eval = review.appraisal.overall_evaluation
            overall_eval.save()  # This triggers the calculate_average_rating

    @action(detail=True, methods=['get'])
    def ratings(self, request, pk=None):
        """Get all competency ratings for a review"""
        review = self.get_object()
        ratings = CompetencyRating.objects.filter(appraisal_review=review)
        serializer = CompetencyRatingSerializer(ratings, many=True)
        return Response(serializer.data)


class CompetencyRatingViewSet(viewsets.ModelViewSet):
    """Competency Rating ViewSet"""
    queryset = CompetencyRating.objects.all()
    serializer_class = CompetencyRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter ratings by user's reviews"""
        user = self.request.user
        if user.is_staff:
            return CompetencyRating.objects.all()

        # Get user's reviews
        user_reviews = AppraisalReview.objects.filter(reviewer=user)
        return CompetencyRating.objects.filter(appraisal_review__in=user_reviews)

    def perform_create(self, serializer):
        """Create rating and recalculate overall evaluation"""
        rating = serializer.save()

        # Recalculate overall evaluation
        if hasattr(rating.appraisal_review.appraisal, 'overall_evaluation'):
            overall_eval = rating.appraisal_review.appraisal.overall_evaluation
            overall_eval.save()


class OverallEvaluationViewSet(viewsets.ModelViewSet):
    """Overall Evaluation ViewSet"""
    queryset = OverallEvaluation.objects.all()
    serializer_class = OverallEvaluationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter evaluations based on user access"""
        user = self.request.user
        if user.is_staff:
            return OverallEvaluation.objects.all()

        # Get user's projects
        user_projects = ProjectMembership.objects.filter(user=user).values_list('project', flat=True)

        # Return evaluations for appraisals in those projects
        return OverallEvaluation.objects.filter(appraisal__project__in=user_projects)
