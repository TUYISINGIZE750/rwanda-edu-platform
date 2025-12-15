# Deployment Guide - Rwanda Education Platform

## Phase 1: Free-Tier Pilot (10 Schools)

### Database: Supabase (Free Tier)
1. Create account at https://supabase.com
2. Create new project
3. Copy connection string from Settings → Database
4. Enable Row Level Security (RLS) for production
5. Free tier: 500MB database, 1GB file storage, 2GB bandwidth

### Cache/Queue: Upstash Redis (Free Tier)
1. Create account at https://upstash.com
2. Create Redis database
3. Copy connection string
4. Free tier: 10K commands/day, 256MB storage

### Backend: Render (Free Tier)
1. Create account at https://render.com
2. Create new Web Service
3. Connect GitHub repository
4. Build command: `pip install -r requirements.txt`
5. Start command: `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000`
6. Add environment variables:
   - `DATABASE_URL`
   - `REDIS_URL`
   - `SECRET_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
7. Free tier: 750 hours/month, auto-sleep after 15min inactivity

### Frontend: Cloudflare Pages (Free Tier)
1. Create account at https://pages.cloudflare.com
2. Connect GitHub repository
3. Build command: `npm run build`
4. Build output: `dist`
5. Add environment variables:
   - `VITE_API_URL`
   - `VITE_WS_URL`
6. Free tier: Unlimited bandwidth, unlimited requests

### File Storage: Supabase Storage
1. In Supabase dashboard, go to Storage
2. Create bucket named `resources`
3. Set public access for read
4. Configure CORS for your domain

## Phase 2: District Scale (100 Schools)

### Upgrade Path
- **Database**: Supabase Pro ($25/month) - 8GB database, 100GB storage
- **Redis**: Upstash Pro ($10/month) - 1M commands/day, 1GB storage
- **Backend**: Render Standard ($7/month per instance) - 2 instances with load balancer
- **CDN**: Cloudflare Pro ($20/month) - Advanced caching, image optimization

### Estimated Cost: ~$70/month for 100 schools

## Phase 3: National Scale (1000+ Schools)

### Government Cloud Migration
- **AWS/Azure**: Government cloud regions
- **Database**: RDS PostgreSQL Multi-AZ
- **Cache**: ElastiCache Redis Cluster
- **Backend**: ECS/EKS with auto-scaling
- **Storage**: S3/Blob Storage with CDN
- **Monitoring**: CloudWatch/Azure Monitor

### Estimated Cost: $500-1000/month for 1000+ schools

## Monitoring & Observability

### Free Tier Options
1. **Grafana Cloud** (Free tier: 10K metrics, 50GB logs)
2. **Sentry** (Free tier: 5K errors/month)
3. **UptimeRobot** (Free tier: 50 monitors)

### Setup
```bash
# Install monitoring dependencies
pip install sentry-sdk prometheus-client

# Add to main.py
import sentry_sdk
sentry_sdk.init(dsn="your-sentry-dsn")
```

## Database Migrations

### Initial Setup
```bash
# Run migrations
alembic upgrade head

# Seed pilot data
python seed_data.py
```

### Production Updates
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Review migration file
# Apply to production
alembic upgrade head
```

## Backup Strategy

### Supabase Automatic Backups
- Free tier: Daily backups, 7-day retention
- Pro tier: Point-in-time recovery

### Manual Backups
```bash
# Backup database
pg_dump $DATABASE_URL > backup.sql

# Restore database
psql $DATABASE_URL < backup.sql
```

## Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Enable HTTPS only
- [ ] Configure CORS properly
- [ ] Enable rate limiting
- [ ] Set up WAF (Cloudflare)
- [ ] Enable Supabase RLS
- [ ] Rotate credentials quarterly
- [ ] Enable audit logging
- [ ] Set up intrusion detection
- [ ] Regular security scans

## Performance Optimization

### Backend
- Enable GZip compression (already configured)
- Use connection pooling (SQLAlchemy)
- Implement Redis caching for frequent queries
- Add database indexes on foreign keys

### Frontend
- Enable Cloudflare caching
- Use lazy loading for routes
- Compress images before upload
- Enable service worker caching

## Rollout Plan

### Week 1-2: Infrastructure Setup
- Set up Supabase, Upstash, Render, Cloudflare
- Deploy backend and frontend
- Run migrations and seed data
- Configure monitoring

### Week 3-4: Pilot Testing
- Onboard 2 schools (100 users)
- Collect feedback
- Fix critical bugs
- Optimize performance

### Week 5-6: Full Pilot
- Onboard remaining 8 schools (500 users)
- Monitor metrics
- Prepare sponsorship proposal
- Document lessons learned

## Success Metrics

### Technical KPIs
- Page load time: <3s on 3G
- API response time: <500ms p95
- Uptime: >99.5%
- Error rate: <1%

### Engagement KPIs
- Daily active users: >60%
- Messages per day: >1000
- Resources shared: >100/week
- Office hours attendance: >50%

## Support & Maintenance

### Daily Tasks
- Monitor error logs
- Check uptime status
- Review flagged content

### Weekly Tasks
- Analyze engagement metrics
- Review incident reports
- Update documentation

### Monthly Tasks
- Security updates
- Performance optimization
- User feedback review
- Cost analysis

## Disaster Recovery

### RTO (Recovery Time Objective): 4 hours
### RPO (Recovery Point Objective): 24 hours

### Recovery Steps
1. Restore database from backup
2. Redeploy backend from GitHub
3. Clear Redis cache
4. Verify functionality
5. Notify users

## Contact

**Technical Lead**: tech@rwandaedu.rw  
**Support**: support@rwandaedu.rw  
**Emergency**: +250-XXX-XXXXXX
