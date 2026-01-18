# Pengrow - Employee Appraisal System

A comprehensive employee appraisal system built with Django REST Framework and React TypeScript. Pengrow enables bi-yearly performance reviews with multi-reviewer support, digital signatures, and role-based access control.

## Features

- **Multi-Reviewer System**: Employees can be reviewed by multiple reporters (one per project)
- **Role-Based Access**: REPORTER and MEMBER roles with permission-based workflows
- **Digital Signatures**: Freehand signature capture using HTML5 canvas
- **Competency Rating**: 10 criteria across 3 categories (Work Efficiency, Productivity, Personal Attributes)
- **Automated Averaging**: Overall ratings calculated from multiple reviewer scores
- **Project-Based Appraisals**: Reviews tied to specific projects and appraisal cycles
- **Secure Authentication**: JWT-based auth with automatic token refresh

## Tech Stack

**Backend:**
- Django 5.2.6
- Django REST Framework 3.15.2
- PostgreSQL (Supabase)
- JWT Authentication

**Frontend:**
- React 19 with TypeScript
- React Router v6
- Axios for API calls
- react-signature-canvas

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL database (or Supabase account)

## Backend Setup

### 1. Create Virtual Environment

```bash
cd backend
virtualenv -p python3.11 venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the `backend/` directory:

```env
# Django settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Supabase PostgreSQL Database (Connection Pooler)
DATABASE_URL=postgresql://username:password@host:port/database

# CORS Settings (for React frontend)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Getting Supabase Database URL:**
1. Create a project at [supabase.com](https://supabase.com)
2. Go to Project Settings > Database
3. Use the "Connection Pooler" URL (port 6543) for better performance
4. Format: `postgresql://postgres.user:password@aws-x-region.pooler.supabase.com:6543/postgres`

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
# Username: admin
# Password: admin123 (or your choice)
```

### 6. Load Demo Data

```bash
python manage.py create_demo_data
```

This creates:
- 1 company (Acme Corporation)
- 3 projects (Alpha, Beta, Gamma)
- 5 users with roles
- Sample appraisals with ratings

**Demo Credentials:**
- `john_reporter / demo123` (Team Lead, can create appraisals)
- `jane_reporter / demo123` (Project Manager, can create appraisals)
- `alice_member / demo123` (Software Engineer)
- `bob_member / demo123` (Marketing Specialist)
- `charlie_member / demo123` (DevOps Engineer)

### 7. Run Development Server

```bash
python manage.py runserver
```

Backend will be available at `http://localhost:8000`

### 8. Test Admin Interface

Visit `http://localhost:8000/admin` and login with superuser credentials.

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Environment Configuration

Create a `.env` file in the `frontend/` directory:

```env
REACT_APP_API_URL=http://localhost:8000/api
```

### 3. Run Development Server

```bash
npm start
```

Frontend will be available at `http://localhost:3000`

## API Documentation

### Authentication Endpoints

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "john_reporter",
  "password": "demo123"
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "john_reporter",
    "email": "john@acme.com",
    "first_name": "John",
    "last_name": "Doe",
    "company": 1,
    "position": "Team Lead",
    "division": "Engineering"
  }
}
```

#### Logout
```http
POST /api/auth/logout/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Current User
```http
GET /api/auth/me/
Authorization: Bearer <access_token>
```

#### Token Refresh
```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}

Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Company & Project Endpoints

#### List Companies
```http
GET /api/companies/
Authorization: Bearer <access_token>
```

#### List Projects
```http
GET /api/projects/
Authorization: Bearer <access_token>
```

#### Project Members
```http
GET /api/projects/{id}/members/
Authorization: Bearer <access_token>
```

### Appraisal Endpoints

#### Create Appraisal
```http
POST /api/appraisals/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "cycle": 1,
  "appraisee": 3,
  "project": 1,
  "discussion_date": "2026-02-15",
  "status": "IN_PROGRESS"
}
```

**Validation Rules:**
- Only REPORTERs can create appraisals
- Reporter must be in the same project as appraisee
- One appraisal per appraisee per project per cycle

#### List Appraisals
```http
GET /api/appraisals/
Authorization: Bearer <access_token>
```

Returns appraisals where user is either appraisee or reviewer.

#### Get Appraisal Details
```http
GET /api/appraisals/{id}/
Authorization: Bearer <access_token>
```

#### Submit Competency Ratings
```http
POST /api/appraisals/{appraisal_id}/reviews/{review_id}/ratings/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "category": "WORK_EFFICIENCY",
  "criterion_name": "Ability to work without supervision",
  "rating": 5,
  "comments": "Excellent independent worker"
}
```

**Rating Scale:** 1 (Not Observed) to 5 (Exceptional)

**Categories:**
- `WORK_EFFICIENCY`: 4 criteria
- `PRODUCTIVITY`: 4 criteria
- `PERSONAL`: 2 criteria

#### Submit Signature
```http
PATCH /api/appraisals/{appraisal_id}/reviews/{review_id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "reviewer_signature_base64": "data:image/png;base64,iVBORw0KGgoAAAA...",
  "is_completed": true
}
```

### Overall Evaluation

The system automatically calculates overall ratings when reviews are marked as completed:

```http
GET /api/appraisals/{id}/overall/
Authorization: Bearer <access_token>

Response:
{
  "id": 1,
  "appraisal": 1,
  "overall_rating_avg": 4.5,
  "ready_for_advanced_work": true,
  "ready_for_promotion": false,
  "summary_comment": "Great performance overall...",
  "hr_signature_base64": null,
  "supervisor_signature_base64": null,
  "employee_signature_base64": null
}
```

## User Guide

### For Reporters (Team Leads, Project Managers)

1. **Login** with your reporter credentials
2. **Navigate to Dashboard** to see your projects
3. **Create Appraisal:**
   - Select active appraisal cycle
   - Choose project
   - Select appraisee from project members
4. **Fill Competency Ratings:**
   - Rate 10 criteria on 1-5 scale
   - Add comments for each category
5. **Sign Review:**
   - Draw signature on canvas
   - Submit to complete review
6. **View Results:**
   - See averaged ratings from all reviewers
   - Review overall evaluation

### For Members (Regular Employees)

1. **Login** with your member credentials
2. **View Appraisals:**
   - See appraisals where you're the appraisee
   - View ratings and feedback
   - Check signatures from reviewers

### Multi-Reviewer Logic

- A user in **5 projects** can have up to **5 reporters** (one per project)
- Each reporter can only appraise users in their **shared project**
- Overall ratings are **averaged** from all completed reviews
- Example: Alice in Project Alpha and Project Gamma
  - Can be reviewed by John (Alpha's reporter) and Sarah (Gamma's reporter)
  - Final rating = average of both reviews

## Deployment

### Backend (Railway)

1. **Install Railway CLI:**
```bash
npm install -g @railway/cli
```

2. **Initialize Railway Project:**
```bash
cd backend
railway init
```

3. **Add Environment Variables in Railway Dashboard:**
   - `SECRET_KEY`: Generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `your-app.railway.app`
   - `DATABASE_URL`: Provided by Railway PostgreSQL or Supabase
   - `CORS_ALLOWED_ORIGINS`: `https://your-github-pages-url`

4. **Deploy:**
```bash
railway up
```

5. **Run Migrations:**
```bash
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py create_demo_data
```

### Frontend (GitHub Pages)

1. **Install gh-pages:**
```bash
npm install --save-dev gh-pages
```

2. **Update package.json:**
```json
{
  "homepage": "https://yourusername.github.io/pengrow",
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  }
}
```

3. **Update Frontend .env for Production:**
```env
REACT_APP_API_URL=https://your-app.railway.app/api
```

4. **Deploy:**
```bash
npm run deploy
```

5. **Enable GitHub Pages:**
   - Go to repository Settings > Pages
   - Select `gh-pages` branch
   - Site will be live at `https://yourusername.github.io/pengrow`

## Project Structure

```
pengrow/
├── backend/
│   ├── config/              # Django project settings
│   ├── core/                # Main Django app
│   │   ├── models.py        # 8 models (User, Company, Project, etc.)
│   │   ├── serializers.py   # DRF serializers
│   │   ├── views.py         # ViewSets and API logic
│   │   ├── permissions.py   # Custom permission classes
│   │   ├── urls.py          # API routes
│   │   └── management/
│   │       └── commands/
│   │           └── create_demo_data.py
│   ├── requirements.txt
│   ├── manage.py
│   └── .env
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   │   ├── Navbar.tsx
│   │   │   ├── SignatureCanvas.tsx
│   │   │   └── ErrorBoundary.tsx
│   │   ├── pages/           # Page components
│   │   │   ├── LoginPage.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── AppraisalCreatePage.tsx
│   │   │   └── AppraisalDetailPage.tsx
│   │   ├── services/        # API services
│   │   │   ├── api.ts
│   │   │   ├── authService.ts
│   │   │   ├── projectService.ts
│   │   │   └── appraisalService.ts
│   │   ├── context/
│   │   │   └── AuthContext.tsx
│   │   ├── types/
│   │   │   └── index.ts     # TypeScript interfaces
│   │   └── App.tsx
│   ├── package.json
│   └── .env
└── README.md
```

## Security Considerations

- **JWT Tokens**: Access tokens expire in 60 minutes, refresh in 7 days
- **CORS**: Configured for specific origins only
- **Password Hashing**: Django's built-in PBKDF2 algorithm
- **Environment Variables**: Sensitive data in .env (gitignored)
- **Permission Checks**: Multi-layered (DRF permissions + custom validators)
- **HTTPS Required**: For production deployments

## Troubleshooting

### Database Connection Issues

**Problem:** "Connection to database not available"

**Solution:**
- Verify Supabase credentials in `.env`
- Use Connection Pooler URL (port 6543), not direct connection (port 5432)
- Check that database is not paused (free tier auto-pauses)

### CORS Errors in Frontend

**Problem:** "Access-Control-Allow-Origin" error

**Solution:**
- Add frontend URL to `CORS_ALLOWED_ORIGINS` in backend `.env`
- Restart Django server after changing CORS settings

### Token Expired

**Problem:** API returns 401 Unauthorized

**Solution:**
- Frontend automatically refreshes tokens via interceptor
- If refresh fails, user is redirected to login
- Check that `SIMPLE_JWT` settings match frontend token handling

### Demo Data Command Fails

**Problem:** Management command errors

**Solution:**
```bash
# Ensure migrations are up to date
python manage.py migrate

# Check database connection
python manage.py dbshell

# Run with verbose output
python manage.py create_demo_data --verbosity 2
```

## Development Roadmap

### Current Status: MVP Complete ✓

Completed features:
- Multi-reviewer appraisal system
- Digital signature capture
- Role-based permissions
- JWT authentication
- Competency rating forms
- Overall evaluation with averaging

### Future Enhancements

- [ ] Multi-company support with tenant isolation
- [ ] Advanced analytics and performance dashboards
- [ ] Email notifications for appraisal reminders
- [ ] File upload for supporting documents
- [ ] Audit logs for all changes
- [ ] Export appraisals to PDF
- [ ] Appraisal cycle automation
- [ ] Mobile responsive improvements
- [ ] LDAP/AD integration for enterprise deployment

## License

This project is developed as an MVP for internal use. All rights reserved.

## Support

For issues or questions:
1. Check this README and troubleshooting section
2. Review the code comments in `backend/core/models.py` for data model details
3. Test with demo credentials to verify expected behavior
4. Check browser console and Django server logs for errors

## Contributors

- Initial development: 2026-01-18
- Built with Django REST Framework and React TypeScript
- Database: PostgreSQL via Supabase
