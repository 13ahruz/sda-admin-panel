# SDA Admin Panel Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        SDA Consulting System                      │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   Next.js        │    │   FastAPI        │    │   Django         │
│   Frontend       │    │   Backend        │    │   Admin Panel    │
│                  │    │                  │    │                  │
│   Port: 3000     │    │   Port: 8000     │    │   Port: 8001     │
│                  │    │                  │    │                  │
│  - Public Site   │    │  - REST API      │    │  - Management    │
│  - User Views    │    │  - File Upload   │    │  - CRUD Ops      │
│  - Multilingual  │    │  - Business Logic│    │  - Content Edit  │
└────────┬─────────┘    └────────┬─────────┘    └────────┬─────────┘
         │                       │                       │
         │ Fetch Data            │ Read/Write            │ Read/Write
         │ via API               │ via SQLAlchemy        │ via Django ORM
         │                       │                       │
         └───────────────────────┴───────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   PostgreSQL Database  │
                    │                        │
                    │   Database: sda_db     │
                    │   Port: 5432           │
                    │                        │
                    │   Tables:              │
                    │   - projects           │
                    │   - news               │
                    │   - team_members       │
                    │   - services           │
                    │   - contact_messages   │
                    │   - ... and more       │
                    └────────────────────────┘
                                 │
                                 │ Files stored at
                                 ▼
                    ┌────────────────────────┐
                    │   File System          │
                    │                        │
                    │   /uploads/            │
                    │   ├── projects/        │
                    │   ├── team/            │
                    │   ├── services/        │
                    │   └── ...              │
                    └────────────────────────┘
```

## Data Flow

### 1. Content Creation Flow
```
Admin Panel → Database → Frontend
    │
    └─→ 1. Admin creates/edits content
        2. Django ORM saves to PostgreSQL
        3. FastAPI serves via API
        4. Next.js displays to users
```

### 2. File Upload Flow
```
FastAPI → File System → Database → Admin Panel
    │
    └─→ 1. User uploads via FastAPI
        2. File saved to /uploads/
        3. URL stored in database
        4. Admin panel displays preview
```

### 3. User Request Flow
```
Browser → Next.js → FastAPI → Database → FastAPI → Next.js → Browser
    │
    └─→ 1. User visits website
        2. Next.js requests data from FastAPI
        3. FastAPI queries PostgreSQL
        4. Data returned as JSON
        5. Next.js renders page
        6. User sees content
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
├─────────────────────────────────────────────────────────────┤
│  Next.js 14 + React + TypeScript + Tailwind CSS             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Application Layer                       │
├──────────────────────┬──────────────────────────────────────┤
│   FastAPI Backend    │        Django Admin Panel            │
│  - Python 3.11       │       - Python 3.11                  │
│  - SQLAlchemy ORM    │       - Django 4.2                   │
│  - Pydantic          │       - Django Admin                 │
│  - Alembic           │       - PostgreSQL Adapter           │
│  - FastAPI Cache     │                                      │
└──────────────────────┴──────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       Database Layer                         │
├─────────────────────────────────────────────────────────────┤
│  PostgreSQL 15 with Multilingual Support                    │
│  - JSONB fields                                              │
│  - Array fields (tags)                                       │
│  - Full-text search indexes                                  │
│  - Foreign key constraints                                   │
└─────────────────────────────────────────────────────────────┘
```

## Django Admin Panel Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Django Admin Panel                       │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐     ┌──────────────┐
│   Settings   │    │    Models    │     │    Admin     │
│              │    │              │     │              │
│ - Database   │    │ - Project    │     │ - List View  │
│ - Security   │    │ - News       │     │ - Edit Form  │
│ - Media      │    │ - Team       │     │ - Inline     │
│ - Static     │    │ - Services   │     │ - Filters    │
│              │    │ - Contact    │     │ - Search     │
│              │    │ - ... more   │     │ - Actions    │
└──────────────┘    └──────────────┘     └──────────────┘
```

## Model Relationships

```
PropertySector
    │
    ├──< SectorInn (many)
    │
    └──< Project (many)
            │
            └──< ProjectPhoto (many)

News
    │
    └──< NewsSection (many)

TeamSection
    │
    └──< TeamSectionItem (many)

About
    │
    └──< AboutLogo (many)

Partner
    │
    └──< PartnerLogo (many)
```

## Admin Panel Features Map

```
┌─────────────────────────────────────────────────────────────┐
│                    Admin Panel Features                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ List Views  │  │ Edit Forms  │  │  Inlines    │  │   Filters   │
├─────────────┤  ├─────────────┤  ├─────────────┤  ├─────────────┤
│ - Columns   │  │ - Fieldsets │  │ - Photos    │  │ - Sector    │
│ - Sorting   │  │ - Widgets   │  │ - Sections  │  │ - Year      │
│ - Preview   │  │ - Validation│  │ - Logos     │  │ - Status    │
│ - Actions   │  │ - Help Text │  │ - Items     │  │ - Date      │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘

┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Search    │  │  Ordering   │  │   Images    │  │ Multilingual│
├─────────────┤  ├─────────────┤  ├─────────────┤  ├─────────────┤
│ - All langs │  │ - Drag/drop │  │ - Previews  │  │ - EN fields │
│ - Email     │  │ - Order num │  │ - Upload    │  │ - AZ fields │
│ - Name      │  │ - Auto-save │  │ - Display   │  │ - RU fields │
│ - Content   │  │ - Priority  │  │ - Optimize  │  │ - Fallback  │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Security Layers                         │
└─────────────────────────────────────────────────────────────┘

Layer 1: Network Security
    │
    ├─→ Firewall (UFW)
    ├─→ IP Whitelisting (Optional)
    └─→ HTTPS/SSL (Let's Encrypt)

Layer 2: Application Security
    │
    ├─→ Django Authentication
    ├─→ Superuser Permissions
    ├─→ CSRF Protection
    └─→ SQL Injection Prevention (ORM)

Layer 3: Database Security
    │
    ├─→ User Permissions
    ├─→ Connection Encryption
    ├─→ Password Hashing
    └─→ Prepared Statements

Layer 4: Data Security
    │
    ├─→ Input Validation
    ├─→ Output Escaping
    ├─→ XSS Prevention
    └─→ Content Security Policy
```

## Deployment Options

```
┌─────────────────────────────────────────────────────────────┐
│                    Deployment Options                        │
└─────────────────────────────────────────────────────────────┘

Option 1: Docker (Recommended)
    │
    ├─→ docker-compose.yml (Full stack)
    └─→ docker-compose.standalone.yml (Existing DB)

Option 2: Manual Deployment
    │
    ├─→ Virtual Environment (venv)
    ├─→ Gunicorn (WSGI Server)
    ├─→ Nginx (Reverse Proxy)
    └─→ Systemd (Service Manager)

Option 3: Cloud Platforms
    │
    ├─→ AWS (EC2 + RDS)
    ├─→ DigitalOcean (Droplet + Managed DB)
    ├─→ Heroku (Dynos + PostgreSQL)
    └─→ Azure (App Service + PostgreSQL)
```

## File Organization

```
admin-panel/
│
├── Core Configuration
│   ├── admin_panel/settings.py     ← Main config
│   ├── admin_panel/urls.py         ← URL routing
│   └── .env                        ← Environment vars
│
├── Application Code
│   ├── sda_backend/models.py       ← Database models
│   └── sda_backend/admin.py        ← Admin config
│
├── Deployment
│   ├── Dockerfile                  ← Container image
│   ├── docker-compose.yml          ← Orchestration
│   ├── requirements.txt            ← Dependencies
│   └── setup scripts               ← Automation
│
└── Documentation
    ├── README.md                   ← Main docs
    ├── QUICKSTART.md               ← Quick start
    ├── DEPLOYMENT.md               ← Production guide
    └── START_HERE.md               ← Overview
```

## Workflow Diagrams

### Content Management Workflow
```
1. Login to Admin
         │
         ▼
2. Navigate to Model (e.g., Projects)
         │
         ▼
3. Click "Add" or Edit existing
         │
         ▼
4. Fill multilingual fields
         │
         ▼
5. Add related items (photos, sections)
         │
         ▼
6. Save changes
         │
         ▼
7. Changes immediately available via API
         │
         ▼
8. Frontend displays updated content
```

### Contact Message Management
```
1. New message arrives (via FastAPI)
         │
         ▼
2. Appears in Admin → Contact Messages
         │
         ▼
3. Filter by "new" status
         │
         ▼
4. Open message and review
         │
         ▼
5. Update status to "in progress"
         │
         ▼
6. Process the request
         │
         ▼
7. Update status to "resolved"
         │
         ▼
8. Mark as read
```

## Performance Characteristics

```
Metric                  Value
────────────────────────────────────────
Response Time          < 100ms (local)
                       < 500ms (prod)

Database Queries       Optimized with
                       select_related()

Connection Pool        600s max age

Static Cache           30 days

Concurrent Users       Up to 50 (default)
                       Scalable with workers

Memory Usage           ~100MB base
                       ~50MB per worker

Disk Space             ~500MB total
```

## Integration Points

```
┌──────────────────────────────────────────────────────────┐
│                  Integration Points                       │
└──────────────────────────────────────────────────────────┘

1. Database
   ├─→ PostgreSQL direct connection
   └─→ Same database as FastAPI

2. File System
   ├─→ Reads from FastAPI uploads
   └─→ Displays image previews

3. Authentication
   ├─→ Separate from FastAPI
   └─→ Django user system

4. API (Optional)
   ├─→ Can expose Django REST API
   └─→ For advanced integrations
```

---

This architecture provides:
✅ **Separation of Concerns** - Each layer has clear responsibility
✅ **Scalability** - Can scale each component independently  
✅ **Maintainability** - Clean, organized structure
✅ **Security** - Multiple security layers
✅ **Performance** - Optimized queries and caching
✅ **Flexibility** - Easy to extend and customize
