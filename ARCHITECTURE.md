# Architecture Documentation

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Rwanda Edu Platform                      │
│                        Vision 2050                           │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Students   │         │   Teachers   │         │    Admins    │
│  (Mobile/Web)│         │  (Mobile/Web)│         │     (Web)    │
└──────┬───────┘         └──────┬───────┘         └──────┬───────┘
       │                        │                        │
       └────────────────────────┴────────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │   Cloudflare Pages    │
                    │   (Vue 3 PWA)         │
                    │   - Offline-first     │
                    │   - IndexedDB cache   │
                    │   - Service Worker    │
                    └───────────┬───────────┘
                                │
                    ┌───────────▼───────────┐
                    │   FastAPI Backend     │
                    │   (Render/Fly.io)     │
                    │   - REST API          │
                    │   - WebSockets        │
                    │   - JWT Auth          │
                    └───────────┬───────────┘
                                │
                ┌───────────────┼───────────────┐
                │               │               │
        ┌───────▼──────┐ ┌─────▼─────┐ ┌──────▼──────┐
        │  PostgreSQL  │ │   Redis   │ │  Supabase   │
        │  (Supabase)  │ │ (Upstash) │ │   Storage   │
        │  - Users     │ │ - Cache   │ │  - Files    │
        │  - Messages  │ │ - Pub/Sub │ │  - Images   │
        │  - Groups    │ │ - Queue   │ │  - Docs     │
        └──────────────┘ └───────────┘ └─────────────┘
```

## Data Flow

### 1. Authentication Flow
```
User → Login Form → POST /auth/login → Verify Password
                                      → Generate JWT
                                      → Return Token + User
                                      → Store in localStorage
                                      → Set Authorization Header
```

### 2. Message Flow (Realtime)
```
Student → Type Message → POST /messages/ → Check Role
                                         → Status = PENDING (student)
                                         → Save to PostgreSQL
                                         → Notify Teacher

Teacher → Moderation Queue → POST /messages/approve → Update Status
                                                    → Publish to Redis
                                                    → WebSocket Broadcast
                                                    → All Clients Receive
```

### 3. DM Request Flow
```
Student → Request DM → POST /dm-requests/ → Save Request
                                           → Notify Teacher

Teacher → Review → POST /dm-requests/{id}/approve → Set Time Window
                                                   → Create DM Channel
                                                   → Notify Student

[48 hours later] → Cron Job → Expire Window → Close DM Channel
```

### 4. Offline Sync Flow
```
User Offline → Type Message → Save to IndexedDB
                            → Queue for Sync

User Online → Service Worker → Detect Connection
                             → POST /messages/ (retry)
                             → Clear Queue
                             → Sync Latest Messages
```

## Database Schema

### Core Tables

**users**
- id (PK)
- email (unique)
- hashed_password
- full_name
- role (student/teacher/admin)
- school_id (FK)
- grade (nullable)
- attributes (JSON: clubs, teams)
- locale (rw/en/fr)

**groups**
- id (PK)
- school_id
- name
- type (class/club/team/special)
- roster_source (auto/manual)
- grade (nullable)

**channels**
- id (PK)
- group_id (FK)
- name
- type (announcements/discussion/resources/office_hours)

**messages**
- id (PK)
- channel_id (FK)
- user_id (FK)
- content (text)
- status (pending/approved/rejected/hidden)
- attachments (JSON)
- scheduled_at (nullable)
- approved_by (FK, nullable)

**dm_requests**
- id (PK)
- student_id (FK)
- teacher_id (FK)
- topic
- reason
- status (pending/approved/rejected/expired)
- window_start (nullable)
- window_end (nullable)

**resources**
- id (PK)
- owner_id (FK)
- title
- type (file/link)
- url
- size
- checksum
- metadata (JSON)

**incidents**
- id (PK)
- message_id (FK)
- reporter_id (FK)
- reason
- severity (low/medium/high/critical)
- status (pending/reviewed/resolved/dismissed)
- decision (nullable)

## API Design

### RESTful Endpoints

**Authentication**
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT

**Directory**
- `GET /directory/groups` - Get user's groups
- `GET /directory/groups/{id}/channels` - Get group channels

**Messages**
- `POST /messages/` - Send message
- `GET /messages/channel/{id}` - Get channel messages
- `POST /messages/approve` - Approve/reject message

**DM Requests**
- `POST /dm-requests/` - Create DM request
- `GET /dm-requests/pending` - Get pending requests (teacher)
- `POST /dm-requests/{id}/approve` - Approve/reject request

**Resources**
- `POST /resources/` - Upload resource
- `GET /resources/` - List resources

**Incidents**
- `POST /flags/` - Flag message
- `GET /flags/pending` - Get pending incidents (teacher)

**Sessions**
- `POST /sessions/` - Create Jitsi session
- `GET /sessions/channel/{id}` - Get channel sessions

**WebSocket**
- `WS /ws/channels/{id}` - Realtime chat

## Security Architecture

### Authentication & Authorization
- JWT tokens with 7-day expiration
- Role-based access control (RBAC)
- Attribute-based access control (ABAC)
- Password hashing with bcrypt

### Data Protection
- TLS/HTTPS only
- Environment variables for secrets
- SQL injection prevention (SQLAlchemy ORM)
- XSS prevention (Vue sanitization)
- CSRF protection (SameSite cookies)

### Child Protection
- DM approval workflow
- Teacher moderation queue
- Content flagging system
- Audit trails for all actions
- Time-limited communication windows

## Performance Optimization

### Backend
- GZip compression (FastAPI middleware)
- Database connection pooling (SQLAlchemy)
- Redis caching for frequent queries
- Async I/O (FastAPI + asyncio)
- Database indexes on foreign keys

### Frontend
- Code splitting (Vite)
- Lazy loading routes
- Service Worker caching
- IndexedDB for offline data
- Lite Mode (minimal CSS/images)

### Network
- CDN for static assets (Cloudflare)
- Image compression
- Text-first payloads <10KB
- WebSocket for realtime (vs polling)

## Scalability Strategy

### Horizontal Scaling
- Stateless backend (JWT auth)
- Redis for session sharing
- Load balancer (Cloudflare/Nginx)
- Database read replicas

### Vertical Scaling
- Increase instance size
- More database connections
- Larger Redis cache

### Caching Strategy
- L1: Browser cache (Service Worker)
- L2: CDN cache (Cloudflare)
- L3: Redis cache (API responses)
- L4: Database query cache

## Monitoring & Observability

### Metrics
- Request rate (req/s)
- Response time (p50, p95, p99)
- Error rate (%)
- Database connections
- Redis memory usage

### Logs
- Application logs (FastAPI)
- Access logs (Nginx)
- Error logs (Sentry)
- Audit logs (database)

### Alerts
- High error rate (>5%)
- Slow response time (>2s)
- Database connection exhaustion
- Disk space low (<10%)

## Disaster Recovery

### Backup Strategy
- Database: Daily automated backups (Supabase)
- Files: Replicated storage (Supabase)
- Code: Version control (GitHub)

### Recovery Procedures
1. Restore database from backup
2. Redeploy backend from GitHub
3. Clear Redis cache
4. Verify functionality
5. Notify users

### RTO/RPO
- Recovery Time Objective: 4 hours
- Recovery Point Objective: 24 hours

## Future Enhancements

### Phase 2 (District Scale)
- Mobile apps (React Native)
- Push notifications
- Advanced analytics dashboard
- AI-powered content moderation
- Video transcription

### Phase 3 (National Scale)
- Multi-region deployment
- Advanced caching (CDN edge)
- Machine learning recommendations
- Integration with national ID system
- Government cloud migration

### Vision 2050
- Full digital transformation
- AI tutoring assistants
- VR/AR learning experiences
- Blockchain credentials
- IoT classroom integration
