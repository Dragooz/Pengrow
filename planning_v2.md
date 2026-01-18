# Pengrow - Appraisal System (v2)

## Overview
Bi-yearly employee appraisal system with multi-reviewer support, freehand signatures, and role-based access control.

## System Requirements

### Organizational Structure
- **Company** → **Projects** → **Users** (with project-specific roles)
- Users can participate in multiple projects with different roles per project
- "Reporter" role enables users to appraise other members within the same project

### Appraisal Workflow
- **Cycle:** Bi-yearly reviews
  - Period 1: October - March
  - Period 2: April - September
- **Multi-reviewer:** Multiple reporters can appraise the same user; ratings are averaged/combined
- **Evaluation Template:** Fixed structure (same for all users/roles)

### Appraisal Form Structure

**1. Administrative Data**
- Appraisee Details: Name, Position, Division, Date Joined, Last Promotion Date
- Reviewer Details: Name, Position
- Discussion Session Date
- Review Period (From/To dates)

**2. Competency Evaluation**
Scale: Exceptional | Good | As Expected | Weak | Not Observed

*Work Efficiency*
- Ability to work without supervision
- Knowledge of roles and responsibilities
- Work accuracy and correctness
- Resourcefulness and creativity
- Open comments section

*Productivity, Administrative & Supervisory*
- Completes tasks according to instructions
- Takes responsibility for work
- Sustains productive work
- Meets reasonable time estimates
- Open comments section

*Personal Attributes*
- Initiative and ambition
- Manner and appearance
- Open comments section

**3. Overall Evaluation**
- Rating: Poor | Below Expectation | Satisfactory | Above Expectations | Excellent
- Ready for advanced work? (Yes/No)
- Ready for promotion? (Yes/No)
- Summary comment

**4. Signatures** (Freehand canvas-based)
- Appraisee signature + timestamp
- Reviewer signature + timestamp
- HR/PIC signature + timestamp

## Tech Stack
- **Backend:** Django 6.x + Django REST Framework
- **Database:** Do your research and find the latest stable database version in Postgres
- **Frontend:** Do your research and find the latest stable database version in React
- **Signature Canvas:** react-signature-canvas or signature_pad
- **API:** RESTful endpoints

## Data Model 

**Base Model - Inherited by other models**
created_at, updated_at, created_by, updated_by

**Company**
- name

**Project**
- company (FK), name, description

**User**
- company (FK), email (unique), first_name, last_name, position, division
- date_joined, last_promotion_date, is_active, password (hashed)

**ProjectMembership**
- project (FK), user (FK), role (REPORTER | MEMBER), joined_at
- Unique: (project, user)

**AppraisalCycle**
- company (FK), period_start, period_end, status (DRAFT | ACTIVE | CLOSED)

**Appraisal**
- cycle (FK), appraisee (FK), project (FK), discussion_date
- status (PENDING | IN_PROGRESS | COMPLETED), created_at, updated_at

**AppraisalReview** (one per reviewer)
- appraisal (FK), reviewer (FK), completed (bool)
- reviewer_signature (base64), reviewer_signed_at, created_at, updated_at

**CompetencyRating**
- review (FK), category (WORK_EFFICIENCY | PRODUCTIVITY | PERSONAL)
- criterion (text), rating (scale), comments (optional)

**OverallEvaluation**
- appraisal (FK, one-to-one), overall_rating (calculated average)
- ready_for_advanced_work (bool), ready_for_promotion (bool)
- summary_comment, appraisee_signature, appraisee_signed_at
- hr_signature, hr_signed_at, finalized_at

## Implementation Phases

**Phase 1: Project Setup**
- Initialize Django + PostgreSQL + DRF
- Initialize React + Router
- Configure CORS, authentication (JWT)

**Phase 2: Backend Core**
- Implement all Django models
- Create migrations + admin interface
- Add model managers for averaging

**Phase 3: Backend API**
- Serializers for all models
- API endpoints: auth, companies, projects, users, appraisals, reviews
- Permissions (role-based)
- Multi-reviewer averaging logic

**Phase 4: Frontend Core**
- Authentication flow + protected routes
- Layout, navigation, dashboard
- Project selection interface

**Phase 5: Frontend Appraisal Forms**
- Appraisal creation + review forms
- Competency rating interface (5-point scale)
- Signature canvas component
- Display averaged results

**Phase 6: Admin & Management**
- Cycle management (create, activate, close)
- User/project management
- Reports and analytics
- HR finalization workflow

**Phase 7: Testing & Deployment**
- Backend + frontend tests
- Docker configuration
- Deployment scripts
- Documentation

## Key Technical Decisions

1. **Multi-reviewer averaging:** Calculate in `OverallEvaluation.save()` by aggregating completed `AppraisalReview` ratings
2. **Signature storage:** Base64-encoded PNG in TextField
3. **Role checking:** Django permissions + custom classes checking `ProjectMembership.role == REPORTER`
4. **Frontend state:** React Context for auth
5. **Date handling:** Django timezone-aware dates, ISO format for API

## Next Steps
1. Set up dev environment (Python venv, Node.js)
2. Initialize Django project and React app
3. Begin Phase 1 implementation