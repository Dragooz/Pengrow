from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import date, timedelta
from core.models import (
    Company, Project, ProjectMembership,
    AppraisalCycle, Appraisal, AppraisalReview,
    CompetencyRating, OverallEvaluation
)

User = get_user_model()


class Command(BaseCommand):
    help = 'Create demo data for Pengrow appraisal system'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Creating demo data...'))

        # Create Company
        company, created = Company.objects.get_or_create(
            name='Acme Corporation',
            defaults={'is_active': True}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created company: {company.name}'))
        else:
            self.stdout.write(f'  Company already exists: {company.name}')

        # Create Projects
        projects_data = [
            {'name': 'Project Alpha', 'description': 'Main product development'},
            {'name': 'Project Beta', 'description': 'Marketing initiatives'},
            {'name': 'Project Gamma', 'description': 'Internal tools and automation'},
        ]

        projects = []
        for proj_data in projects_data:
            project, created = Project.objects.get_or_create(
                company=company,
                name=proj_data['name'],
                defaults={'description': proj_data['description'], 'is_active': True}
            )
            projects.append(project)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created project: {project.name}'))

        # Create Users
        users_data = [
            {'username': 'john_reporter', 'email': 'john@acme.com', 'first_name': 'John', 'last_name': 'Doe', 'position': 'Team Lead', 'division': 'Engineering'},
            {'username': 'jane_reporter', 'email': 'jane@acme.com', 'first_name': 'Jane', 'last_name': 'Smith', 'position': 'Project Manager', 'division': 'Marketing'},
            {'username': 'alice_member', 'email': 'alice@acme.com', 'first_name': 'Alice', 'last_name': 'Johnson', 'position': 'Software Engineer', 'division': 'Engineering'},
            {'username': 'bob_member', 'email': 'bob@acme.com', 'first_name': 'Bob', 'last_name': 'Brown', 'position': 'Marketing Specialist', 'division': 'Marketing'},
            {'username': 'charlie_member', 'email': 'charlie@acme.com', 'first_name': 'Charlie', 'last_name': 'Wilson', 'position': 'DevOps Engineer', 'division': 'Engineering'},
        ]

        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'company': company,
                    'position': user_data['position'],
                    'division': user_data['division'],
                    'is_active': True,
                }
            )
            if created:
                user.set_password('demo123')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Created user: {user.username} (password: demo123)'))
            users.append(user)

        # Assign users to projects with roles
        # Project Alpha: john (reporter), alice (member), charlie (member)
        memberships_data = [
            (projects[0], users[0], 'REPORTER'),  # John - Project Alpha - Reporter
            (projects[0], users[2], 'MEMBER'),    # Alice - Project Alpha - Member
            (projects[0], users[4], 'MEMBER'),    # Charlie - Project Alpha - Member
            (projects[1], users[1], 'REPORTER'),  # Jane - Project Beta - Reporter
            (projects[1], users[3], 'MEMBER'),    # Bob - Project Beta - Member
            (projects[2], users[0], 'REPORTER'),  # John - Project Gamma - Reporter
            (projects[2], users[2], 'MEMBER'),    # Alice - Project Gamma - Member
        ]

        for project, user, role in memberships_data:
            membership, created = ProjectMembership.objects.get_or_create(
                project=project,
                user=user,
                defaults={'role': role}
            )
            if created:
                self.stdout.write(f'  ✓ Added {user.username} to {project.name} as {role}')

        # Create Appraisal Cycle
        cycle, created = AppraisalCycle.objects.get_or_create(
            company=company,
            period_start=date(2025, 10, 1),
            period_end=date(2026, 3, 31),
            defaults={'status': 'ACTIVE'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created appraisal cycle: {cycle.period_start} to {cycle.period_end}'))

        # Create Appraisals
        # Appraisal for Alice in Project Alpha by John
        appraisal1, created = Appraisal.objects.get_or_create(
            cycle=cycle,
            appraisee=users[2],  # Alice
            project=projects[0],  # Project Alpha
            defaults={
                'discussion_date': date.today() + timedelta(days=7),
                'status': 'IN_PROGRESS'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created appraisal for {appraisal1.appraisee.get_full_name()}'))

            # Create AppraisalReview
            review1 = AppraisalReview.objects.create(
                appraisal=appraisal1,
                reviewer=users[0],  # John
                is_completed=False
            )
            self.stdout.write(f'  ✓ Created review by {review1.reviewer.get_full_name()}')

            # Create some sample ratings
            criteria_data = [
                ('WORK_EFFICIENCY', 'Ability to work without supervision', 5),
                ('WORK_EFFICIENCY', 'Knowledge of roles and responsibilities', 4),
                ('WORK_EFFICIENCY', 'Work accuracy and correctness', 5),
                ('WORK_EFFICIENCY', 'Resourcefulness and creativity', 4),
                ('PRODUCTIVITY', 'Completes tasks according to instructions', 5),
                ('PRODUCTIVITY', 'Takes responsibility for work', 5),
                ('PRODUCTIVITY', 'Sustains productive work', 4),
                ('PRODUCTIVITY', 'Meets reasonable time estimates', 4),
                ('PERSONAL', 'Initiative and ambition', 5),
                ('PERSONAL', 'Manner and appearance', 4),
            ]

            for category, criterion, rating in criteria_data:
                CompetencyRating.objects.create(
                    appraisal_review=review1,
                    category=category,
                    criterion_name=criterion,
                    rating=rating,
                    comments=f'Excellent performance in {criterion.lower()}'
                )

            # Create OverallEvaluation
            overall = OverallEvaluation.objects.create(
                appraisal=appraisal1,
                ready_for_advanced_work=True,
                ready_for_promotion=False,
                summary_comment='Great performance overall, showing strong technical skills and reliability.'
            )
            overall.save()  # This triggers the calculate_average_rating
            self.stdout.write(f'  ✓ Created overall evaluation (avg: {overall.overall_rating_avg})')

        # Appraisal for Bob in Project Beta by Jane
        appraisal2, created = Appraisal.objects.get_or_create(
            cycle=cycle,
            appraisee=users[3],  # Bob
            project=projects[1],  # Project Beta
            defaults={
                'discussion_date': date.today() + timedelta(days=14),
                'status': 'PENDING'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Created appraisal for {appraisal2.appraisee.get_full_name()}'))

            # Create AppraisalReview (empty, for testing)
            review2 = AppraisalReview.objects.create(
                appraisal=appraisal2,
                reviewer=users[1],  # Jane
                is_completed=False
            )
            self.stdout.write(f'  ✓ Created empty review by {review2.reviewer.get_full_name()}')

            # Create OverallEvaluation
            OverallEvaluation.objects.create(appraisal=appraisal2)

        self.stdout.write(self.style.SUCCESS('\n✅ Demo data created successfully!'))
        self.stdout.write(self.style.SUCCESS('\nDemo credentials:'))
        self.stdout.write('  Admin:        admin / admin123')
        self.stdout.write('  Reporter 1:   john_reporter / demo123')
        self.stdout.write('  Reporter 2:   jane_reporter / demo123')
        self.stdout.write('  Member 1:     alice_member / demo123')
        self.stdout.write('  Member 2:     bob_member / demo123')
        self.stdout.write('  Member 3:     charlie_member / demo123')
