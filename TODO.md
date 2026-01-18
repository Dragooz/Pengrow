# Pengrow MVP - Development TODO List

**Project:** Employee Appraisal System
**Goal:** Working MVP with core features
**Timeline:** 7 days estimated

---

## Phase 1: Environment Setup (Day 1)

### Backend Setup
- [x] 1. Create project folder structure (backend/ and frontend/)
- [x] 2. Create Python virtual environment in backend/
- [x] 3. Install Django and dependencies (django, djangorestframework, djangorestframework-simplejwt, psycopg2-binary, python-dotenv)
- [x] 4. Initialize Django project with `django-admin startproject config .`
- [x] 5. Create Django app `core` with `python manage.py startapp core`

### Frontend Setup
- [x] 6. Initialize React app with TypeScript template
- [x] 7. Install frontend dependencies (react-router-dom, axios, react-signature-canvas, @types/react-signature-canvas)

### Database Setup
- [x] 8. Install PostgreSQL 17+ locally (or use existing installation) - Using Supabase instead
- [x] 9. Create PostgreSQL database `pengrow_db` - Using Supabase database
- [x] 10. Configure database credentials in Django settings.py
- [x] 11. Create .env file for environment variables

---

## Phase 2: Django Models (Day 1-2)

### Model Creation
- [x] 12. Create BaseModel abstract class (id, created_at, updated_at, created_by, updated_by)
- [x] 13. Create Company model (name, is_active)
- [x] 14. Create Project model (company_id FK, name, description, is_active)
- [x] 15. Create custom User model extending AbstractUser (company_id FK, position, division, date_joined, last_promotion_date)
- [x] 16. Create ProjectMembership model (project_id FK, user_id FK, role, joined_at) with unique constraint
- [x] 17. Create AppraisalCycle model (company_id FK, period_start, period_end, status)
- [x] 18. Create Appraisal model (cycle_id FK, appraisee_id FK, project_id FK, discussion_date, status)
- [x] 19. Create AppraisalReview model (appraisal_id FK, reviewer_id FK, is_completed, reviewer_signature_base64, reviewer_signed_at)
- [x] 20. Create CompetencyRating model (appraisal_review_id FK, category, criterion_name, rating, comments)
- [x] 21. Create OverallEvaluation model (appraisal_id FK one-to-one, overall_rating_avg, ready_for_advanced_work, ready_for_promotion, summary_comment, signatures)

### Migrations & Admin
- [x] 22. Update AUTH_USER_MODEL in settings.py
- [x] 23. Run `python manage.py makemigrations`
- [x] 24. Run `python manage.py migrate`
- [x] 25. Create superuser with `python manage.py createsuperuser` (admin / admin123)
- [x] 26. Register all models in core/admin.py
- [ ] 27. Test admin interface by logging in to /admin

---

## Phase 3: Backend API (Day 2-3)

### Serializers
- [x] 28. Create UserSerializer in core/serializers.py
- [x] 29. Create CompanySerializer and ProjectSerializer
- [x] 30. Create ProjectMembershipSerializer
- [x] 31. Create AppraisalCycleSerializer
- [x] 32. Create AppraisalSerializer and AppraisalReviewSerializer
- [x] 33. Create CompetencyRatingSerializer
- [x] 34. Create OverallEvaluationSerializer

### ViewSets & Permissions
- [x] 35. Create custom permission class IsReporter
- [x] 36. Create custom permission class IsSameProject
- [x] 37. Create AuthViewSet (login, logout, current user)
- [x] 38. Create CompanyViewSet (list, retrieve)
- [x] 39. Create ProjectViewSet (list, retrieve, members)
- [x] 40. Create AppraisalViewSet (CRUD with permissions)
- [x] 41. Create AppraisalReviewViewSet (nested under appraisals)
- [x] 42. Implement multi-reviewer averaging logic in OverallEvaluation.save() or signals

### API Configuration
- [x] 43. Create core/urls.py and configure API routes
- [x] 44. Add core.urls to main urls.py
- [x] 45. Configure REST_FRAMEWORK settings in settings.py
- [x] 46. Configure SIMPLE_JWT settings (access/refresh token lifetimes)
- [x] 47. Configure CORS settings (django-cors-headers)
- [ ] 48. Test API endpoints with Django REST Framework browsable API

---

## Phase 4: Frontend Core (Day 3-4)

### Project Structure
- [ ] 49. Create folder structure (components/, pages/, services/, context/, utils/)
- [ ] 50. Configure React Router in App.tsx
- [ ] 51. Create route definitions (/, /login, /dashboard, /projects, /appraisals, /appraisals/:id)

### Authentication
- [ ] 52. Create AuthContext with login/logout/user state
- [ ] 53. Create ProtectedRoute component
- [ ] 54. Create api.ts service with axios instance (base URL, JWT interceptor)
- [ ] 55. Create auth service functions (login, logout, getCurrentUser)

### Core Components
- [ ] 56. Create LoginPage with form and validation
- [ ] 57. Create Navbar component with logout button
- [ ] 58. Create Dashboard page (show user info and project list)
- [ ] 59. Create ProjectList component
- [ ] 60. Create ProjectDetail page

---

## Phase 5: Appraisal Forms (Day 4-5)

### Appraisal Creation
- [ ] 61. Create AppraisalCreatePage with appraisee selection
- [ ] 62. Create form to select appraisee from project members
- [ ] 63. Create discussion date picker
- [ ] 64. Implement POST to /api/appraisals/ to create appraisal

### Competency Rating Form
- [ ] 65. Create CompetencyRatingForm component
- [ ] 66. Add Work Efficiency section (4 criteria with 5-point scale)
- [ ] 67. Add Productivity & Supervisory section (4 criteria)
- [ ] 68. Add Personal Attributes section (2 criteria)
- [ ] 69. Add comment textareas for each category
- [ ] 70. Implement save functionality to POST CompetencyRating records

### Signature Component
- [ ] 71. Create SignatureCanvas component using react-signature-canvas
- [ ] 72. Add clear/undo functionality
- [ ] 73. Implement toDataURL() to convert canvas to base64
- [ ] 74. Save signature to AppraisalReview.reviewer_signature_base64

### Results Display
- [ ] 75. Create AppraisalDetailPage to view completed appraisal
- [ ] 76. Display averaged ratings from multiple reviewers
- [ ] 77. Show all reviewers' signatures with timestamps
- [ ] 78. Add HR signature section (if user has HR role)

---

## Phase 6: Validation & Security (Day 6)

### Backend Validation
- [ ] 79. Add validation: reviewer can only appraise users in same project
- [ ] 80. Add validation: user can only be appraised once per project per cycle
- [ ] 81. Add validation: only REPORTER role can create reviews
- [ ] 82. Test permissions with different user roles

### Frontend Validation
- [ ] 83. Add form validation (required fields, date validation)
- [ ] 84. Add error messages for failed API calls
- [ ] 85. Add loading states for async operations
- [ ] 86. Add confirmation dialogs for important actions

### Security Configuration
- [ ] 87. Create .env file with SECRET_KEY, DATABASE_URL, ALLOWED_HOSTS
- [ ] 88. Set DEBUG=False for production
- [ ] 89. Configure ALLOWED_HOSTS for deployment
- [ ] 90. Configure CORS_ALLOWED_ORIGINS
- [ ] 91. Add CSRF protection configuration
- [ ] 92. Review and remove any hardcoded credentials

---

## Phase 7: Testing & Deployment (Day 7)

### Demo Data
- [ ] 93. Create management command `create_demo_data.py`
- [ ] 94. Generate sample company, projects, users with different roles
- [ ] 95. Generate sample appraisals with reviews
- [ ] 96. Run command and verify data in admin

### Manual Testing
- [ ] 97. Test user login/logout flow
- [ ] 98. Test creating appraisal as REPORTER
- [ ] 99. Test filling competency ratings
- [ ] 100. Test signature capture and save
- [ ] 101. Test multi-reviewer scenario (user in multiple projects)
- [ ] 102. Test averaging logic with multiple reviews
- [ ] 103. Test permission restrictions (MEMBER cannot create appraisals)

### Documentation
- [ ] 104. Create README.md with project overview
- [ ] 105. Add setup instructions for backend
- [ ] 106. Add setup instructions for frontend
- [ ] 107. Document API endpoints (routes, methods, request/response)
- [ ] 108. Create user guide for demo (how to use the system)

### Deployment Preparation
- [ ] 109. Create requirements.txt for backend
- [ ] 110. Create railway.json for Railway deployment
- [ ] 111. Configure static files for Django in production
- [ ] 112. Build React production bundle
- [ ] 113. Configure GitHub Pages deployment (gh-pages package)
- [ ] 114. Update frontend API base URL for production
- [ ] 115. Test production build locally

### Deployment
- [ ] 116. Deploy backend to Railway
- [ ] 117. Run migrations on Railway database
- [ ] 118. Create superuser on production
- [ ] 119. Load demo data on production
- [ ] 120. Deploy frontend to GitHub Pages
- [ ] 121. Test end-to-end on production

---

## Post-MVP Enhancements (Future)

- [ ] Multi-company support
- [ ] Advanced analytics and reports
- [ ] Email notifications for appraisal reminders
- [ ] File upload for supporting documents
- [ ] Audit logs for all changes
- [ ] Export appraisals to PDF
- [ ] Appraisal cycle automation
- [ ] Mobile responsive improvements
- [ ] LDAP/AD integration for internal deployment

---

## Notes

- **Current Status:** Not started
- **Next Task:** Task 1 - Create project folder structure
- **Blockers:** None
- **Decisions Needed:** None

---

**Last Updated:** 2026-01-18
