from datetime import datetime, timezone, timedelta

# Rwanda timezone: Central Africa Time (CAT) = UTC+2
RWANDA_TZ = timezone(timedelta(hours=2))

def get_rwanda_time():
    """Get current time in Rwanda timezone (CAT/UTC+2)"""
    return datetime.now(RWANDA_TZ)

def to_rwanda_time(dt: datetime):
    """Convert datetime to Rwanda timezone"""
    if dt.tzinfo is None:
        # Assume UTC if no timezone
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(RWANDA_TZ)

def rwanda_now_iso():
    """Get current Rwanda time as ISO string"""
    return get_rwanda_time().isoformat()
