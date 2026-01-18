from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class BaseModel(models.Model):
    """Abstract base model with audit fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated'
    )

    class Meta:
        abstract = True


class Company(BaseModel):
    """Company model"""
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractUser, BaseModel):
    """Custom User model extending AbstractUser"""
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True
    )
    position = models.CharField(max_length=255, blank=True)
    division = models.CharField(max_length=255, blank=True)
    date_joined = models.DateField(null=True, blank=True)
    last_promotion_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"


class Project(BaseModel):
    """Project model"""
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['company', 'name']

    def __str__(self):
        return f"{self.company.name} - {self.name}"


class ProjectMembership(BaseModel):
    """Project membership with role"""
    ROLE_CHOICES = [
        ('REPORTER', 'Reporter'),
        ('MEMBER', 'Member'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='project_memberships'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='MEMBER')
    joined_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['project', 'user']
        ordering = ['project', 'user']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.project.name} ({self.role})"


class AppraisalCycle(BaseModel):
    """Appraisal cycle model"""
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('ACTIVE', 'Active'),
        ('CLOSED', 'Closed'),
    ]

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='appraisal_cycles'
    )
    period_start = models.DateField()
    period_end = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')

    class Meta:
        ordering = ['-period_start']

    def __str__(self):
        return f"{self.company.name} - {self.period_start} to {self.period_end} ({self.status})"


class Appraisal(BaseModel):
    """Appraisal model - one per appraisee per cycle per project"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    cycle = models.ForeignKey(
        AppraisalCycle,
        on_delete=models.CASCADE,
        related_name='appraisals'
    )
    appraisee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appraisals_received'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='appraisals'
    )
    discussion_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')

    class Meta:
        ordering = ['-cycle__period_start', 'appraisee']

    def __str__(self):
        return f"Appraisal for {self.appraisee.get_full_name()} - {self.project.name}"


class AppraisalReview(BaseModel):
    """Appraisal Review - one per reporter per appraisal"""
    appraisal = models.ForeignKey(
        Appraisal,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_given'
    )
    is_completed = models.BooleanField(default=False)
    reviewer_signature_base64 = models.TextField(blank=True)
    reviewer_signed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['appraisal', 'reviewer']
        ordering = ['appraisal', 'reviewer']

    def __str__(self):
        return f"Review by {self.reviewer.get_full_name()} for {self.appraisal.appraisee.get_full_name()}"


class CompetencyRating(BaseModel):
    """Competency rating - multiple per review"""
    CATEGORY_CHOICES = [
        ('WORK_EFFICIENCY', 'Work Efficiency'),
        ('PRODUCTIVITY', 'Productivity & Supervisory'),
        ('PERSONAL', 'Personal Attributes'),
    ]

    RATING_CHOICES = [
        (1, 'Not Observed'),
        (2, 'Weak'),
        (3, 'As Expected'),
        (4, 'Good'),
        (5, 'Exceptional'),
    ]

    appraisal_review = models.ForeignKey(
        AppraisalReview,
        on_delete=models.CASCADE,
        related_name='competency_ratings'
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    criterion_name = models.CharField(max_length=255)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comments = models.TextField(blank=True)

    class Meta:
        ordering = ['appraisal_review', 'category', 'criterion_name']

    def __str__(self):
        return f"{self.criterion_name} - {self.get_rating_display()}"


class OverallEvaluation(BaseModel):
    """Overall evaluation - one per appraisal (aggregates all reviews)"""
    OVERALL_RATING_CHOICES = [
        (1, 'Poor'),
        (2, 'Below Expectation'),
        (3, 'Satisfactory'),
        (4, 'Above Expectations'),
        (5, 'Excellent'),
    ]

    appraisal = models.OneToOneField(
        Appraisal,
        on_delete=models.CASCADE,
        related_name='overall_evaluation'
    )
    overall_rating_avg = models.FloatField(null=True, blank=True)
    ready_for_advanced_work = models.BooleanField(default=False)
    ready_for_promotion = models.BooleanField(default=False)
    summary_comment = models.TextField(blank=True)
    appraisee_signature_base64 = models.TextField(blank=True)
    appraisee_signed_at = models.DateTimeField(null=True, blank=True)
    hr_signature_base64 = models.TextField(blank=True)
    hr_signed_at = models.DateTimeField(null=True, blank=True)
    finalized_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['appraisal']

    def __str__(self):
        return f"Overall Evaluation for {self.appraisal.appraisee.get_full_name()}"

    def calculate_average_rating(self):
        """Calculate average rating from all completed reviews"""
        completed_reviews = self.appraisal.reviews.filter(is_completed=True)
        if not completed_reviews.exists():
            return None

        all_ratings = CompetencyRating.objects.filter(
            appraisal_review__in=completed_reviews
        )

        if not all_ratings.exists():
            return None

        total = sum(rating.rating for rating in all_ratings)
        count = all_ratings.count()

        return total / count if count > 0 else None

    def save(self, *args, **kwargs):
        """Override save to auto-calculate average rating"""
        if self.pk:  # Only if already exists
            self.overall_rating_avg = self.calculate_average_rating()
        super().save(*args, **kwargs)
