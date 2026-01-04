# How to Run Database Migration

## Option 1: With Environment Variable (Recommended)

1. Set your DATABASE_URL environment variable:
```bash
set DATABASE_URL=your_render_database_url_here
```

2. Run migration:
```bash
python migrations/migrate_notifications.py
```

## Option 2: Interactive (Paste URL when prompted)

1. Run migration:
```bash
python migrations/migrate_notifications.py
```

2. When prompted, paste your Render database URL

## Where to Find Your Database URL

1. Go to Render Dashboard: https://dashboard.render.com
2. Click on your PostgreSQL database
3. Copy the "External Database URL"
4. It looks like: `postgres://user:pass@host/database`

## Expected Output

```
============================================================
  TSSANYWHERE - Notifications Table Migration
============================================================

🔗 Connecting to database...
📝 Creating notifications table...
📊 Creating indexes...

✅ Notifications table created successfully!
✅ Indexes created successfully!

🎉 Migration completed! Your notification system is ready.
```

## Troubleshooting

If you get connection errors:
- Make sure you're using the EXTERNAL database URL (not internal)
- Check that your IP is whitelisted on Render
- Verify the URL format is correct
