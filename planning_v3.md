# Pengrow - Employee Appraisal System

## Overview
Bi-yearly employee appraisal system with role-based access control and digital signatures.

**Deployment:** Internal company servers (secured) + public demo version

## Core Concepts

### Organizational Structure
Company → Projects → Users (with roles per project)

### User Roles (per project)
- **REPORTER:** Can appraise other members in the same project
- **MEMBER:** Regular project member (gets appraised)

### Multi-Reviewer Logic
- A user in 5 projects = can have up to 5 reporters (one per project)
- Each reporter can only appraise users in their shared project
- Final ratings = average of all reporters' ratings

### Appraisal Cycle
- Bi-yearly: Oct-Mar, Apr-Sep
- Fixed evaluation template for all users

### Appraisal Form Sections

**1. Administrative Info**
- Appraisee: name, position, division, join date, last promotion
- Reviewer: name, position
- Discussion date, review period

**2. Competency Ratings** (5-point scale)
- Work Efficiency (4 criteria + comments)
- Productivity & Supervisory (4 criteria + comments)
- Personal Attributes (2 criteria + comments)

**3. Overall Summary**
- Final rating (averaged from all reporters)
- Ready for advanced work? (Y/N)
- Ready for promotion? (Y/N)
- Summary comments

**4. Digital Signatures** (canvas-based)
- Appraisee, Reviewer, HR (each with timestamp)

## Tech Stack
- **Backend:** Django 5.1+ (latest stable) + Django REST Framework + JWT auth
- **Database:** PostgreSQL 17+ (latest stable)
- **Frontend:** React 19+ (latest stable) + React Router
- **Signature:** react-signature-canvas
- **Security:** HTTPS only, CORS configured for internal network

## Deployment
- Frontend - Github pages
- Backend - Railway. 

## Database Schema

**BaseModel** (abstract - inherited by all models)
- id, created_at, updated_at, created_by, updated_by

**Company**
- name, is_active

**Project**
- company_id (FK), name, description, is_active

**User**
- company_id (FK), email (unique), first_name, last_name
- position, division, date_joined, last_promotion_date
- is_active, password_hash

**ProjectMembership**
- project_id (FK), user_id (FK), role (REPORTER|MEMBER), joined_at
- Constraint: unique(project_id, user_id)
- Business rule: Users can only appraise others in same project

**AppraisalCycle**
- company_id (FK), period_start, period_end
- status (DRAFT|ACTIVE|CLOSED)

**Appraisal** (one per appraisee per cycle per project)
- cycle_id (FK), appraisee_id (FK to User), project_id (FK)
- discussion_date, status (PENDING|IN_PROGRESS|COMPLETED)

**AppraisalReview** (one per reporter per appraisal)
- appraisal_id (FK to Appraisal), reviewer_id (FK to User)
- is_completed (bool), reviewer_signature_base64, reviewer_signed_at

**CompetencyRating** (multiple per review)
- appraisal_review_id (FK to AppraisalReview)
- category (WORK_EFFICIENCY|PRODUCTIVITY|PERSONAL)
- criterion_name, rating (1-5 scale), comments

**OverallEvaluation** (one per appraisal - aggregates all reviews)
- appraisal_id (FK to Appraisal, one-to-one)
- overall_rating_avg (calculated from all reviews)
- ready_for_advanced_work (bool), ready_for_promotion (bool)
- summary_comment, appraisee_signature_base64, appraisee_signed_at
- hr_signature_base64, hr_signed_at, finalized_at

## MVP Scope (Build This First)

**Core Features Only:**
1. User authentication (login/logout)
2. Single company, multiple projects
3. Users with REPORTER or MEMBER roles per project
4. Create/view appraisals
5. Fill competency ratings (simple form)
6. Basic signature capture
7. View averaged results

**Defer to Later:**
- Multi-company support
- Advanced analytics/reports
- File uploads
- Email notifications
- Audit logs

## Step-by-Step Build Guide

### STEP 1: Environment Setup (Day 1)

**1.1 Backend Setup**
```bash
# Create project folder
mkdir pengrow && cd pengrow
mkdir backend frontend

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary python-dotenv
django-admin startproject config .
python manage.py startapp core
```

**1.2 Frontend Setup**
```bash
cd ../frontend
npx create-react-app . --template typescript
npm install react-router-dom axios react-signature-canvas
```

**1.3 Database Setup**
- Install PostgreSQL 17+
- Create database: `createdb pengrow_db`
- Update Django `settings.py` with DB credentials

---

### STEP 2: Django Models (Day 1-2)

**2.1 Create models in `core/models.py`**
- BaseModel (abstract)
- Company, Project, User (extend AbstractUser)
- ProjectMembership
- AppraisalCycle, Appraisal, AppraisalReview
- CompetencyRating, OverallEvaluation

**2.2 Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

**2.3 Register models in `core/admin.py`**
- Add all models to Django admin for easy data management

---

### STEP 3: Backend API (Day 2-3)

**3.1 Create serializers in `core/serializers.py`**
- UserSerializer, ProjectSerializer, AppraisalSerializer, etc.

**3.2 Create viewsets in `core/views.py`**
- Use Django REST Framework ViewSets
- Implement permissions (IsReporter, IsSameProject)

**3.3 Configure URLs in `core/urls.py`**
```python
# API endpoints
/api/auth/login/
/api/auth/logout/
/api/projects/
/api/appraisals/
/api/appraisals/{id}/reviews/
```

**3.4 Add JWT authentication**
- Configure `settings.py` with REST_FRAMEWORK and SIMPLE_JWT
- Add CORS settings for frontend

---

### STEP 4: Frontend Core (Day 3-4)

**4.1 Setup routing**
- Create routes: /login, /dashboard, /projects, /appraisals

**4.2 Auth context**
- Create AuthContext for managing login state and JWT tokens
- Add ProtectedRoute component

**4.3 Basic components**
- LoginForm, Navbar, ProjectList, Dashboard

**4.4 API service**
- Create `services/api.js` with axios instance (includes JWT header)

---

### STEP 5: Appraisal Forms (Day 4-5)

**5.1 Appraisal creation form**
- Select appraisee (from project members)
- Set discussion date
- Submit to create Appraisal + AppraisalReview

**5.2 Competency rating form**
- Display 10 criteria in 3 categories
- 5-point rating scale (radio buttons or dropdown)
- Comment textareas
- Save to CompetencyRating model

**5.3 Signature component**
- Use react-signature-canvas
- Convert to base64 PNG
- Save to AppraisalReview.reviewer_signature_base64

**5.4 View appraisal results**
- Display averaged ratings
- Show all reviewers' signatures
- HR can add final signature

---

### STEP 6: Polish & Security (Day 6)

**6.1 Validation**
- Backend: Ensure reviewers can only appraise users in same project
- Frontend: Form validation with error messages

**6.2 Security hardening**
- Enable HTTPS (use self-signed cert for internal demo)
- Set ALLOWED_HOSTS, CORS_ALLOWED_ORIGINS
- Add CSRF protection
- Use environment variables for secrets (.env file)

**6.3 Basic error handling**
- 404 pages, API error messages
- Loading states

---

### STEP 7: Testing & Demo Data (Day 7)

**7.1 Create demo data**
- Management command or admin to create sample company, projects, users
- Create test appraisals

**7.2 Manual testing**
- Test full appraisal workflow as reporter
- Test as appraisee (sign appraisal)
- Test multi-reviewer averaging

**7.3 Documentation**
- README with setup instructions
- API endpoint documentation
- User guide for demo

---

## Key Implementation Notes

**Multi-reviewer averaging logic:**
```python
# In OverallEvaluation.save() or a signal
def calculate_average_rating(appraisal):
    reviews = AppraisalReview.objects.filter(appraisal=appraisal, is_completed=True)
    all_ratings = CompetencyRating.objects.filter(appraisal_review__in=reviews)
    avg = all_ratings.aggregate(Avg('rating'))['rating__avg']
    return avg
```

**Permission check example:**
```python
# Can only appraise users in same project
def can_appraise(reviewer, appraisee, project):
    reviewer_membership = ProjectMembership.objects.filter(
        project=project, user=reviewer, role='REPORTER'
    ).exists()
    appraisee_membership = ProjectMembership.objects.filter(
        project=project, user=appraisee
    ).exists()
    return reviewer_membership and appraisee_membership
```

**Signature storage:**
- Canvas → `toDataURL('image/png')` → base64 string → TextField
- Display: `<img src={signatureBase64} />`

---

## Deployment Notes

**For Internal Server:**
- Use company's internal domain (e.g., http://appraisal.internal.company.com)
- HTTPS with company SSL cert
- Restrict CORS to internal IPs
- Use company's LDAP/AD for auth (future enhancement)

**For Public Demo:**
- Deploy on Heroku/Railway/DigitalOcean
- Use environment variables for config
- Add "DEMO MODE" banner
- Populate with dummy data
- Disable sensitive features if needed