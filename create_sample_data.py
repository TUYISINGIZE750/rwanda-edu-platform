import sqlite3
from datetime import datetime, timedelta
import random

# Connect to database
conn = sqlite3.connect('backend/app.db')
cursor = conn.cursor()

# Create sample groups
groups_data = [
    (1, 'Electronics Level 2', 'class', 1, 2, 'manual', datetime.now()),
    (2, 'Welding Basics', 'class', 1, 1, 'manual', datetime.now()),
    (3, 'Automotive Repair', 'class', 1, 3, 'manual', datetime.now()),
    (4, 'General Announcements', 'announcement', 1, None, 'manual', datetime.now())
]

for group in groups_data:
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO groups (id, name, type, school_id, grade, roster_source, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, group)
        print(f"Created group: {group[1]}")
    except Exception as e:
        print(f"Error creating group {group[1]}: {e}")

# Create sample channels
channels_data = [
    (1, 'general', 'General Discussion', 'Main discussion channel', 1, datetime.now()),
    (2, 'assignments', 'Assignments', 'Submit your assignments here', 1, datetime.now()),
    (3, 'resources', 'Resources', 'Learning materials and resources', 1, datetime.now()),
    (4, 'practice', 'Practice Sessions', 'Hands-on practice discussions', 2, datetime.now()),
    (5, 'safety', 'Safety Guidelines', 'Important safety information', 2, datetime.now()),
    (6, 'repairs', 'Repair Techniques', 'Discuss repair methods', 3, datetime.now()),
    (7, 'announcements', 'School News', 'Important school announcements', 4, datetime.now())
]

for channel in channels_data:
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO channels (id, name, description, type, group_id, created_at)
            VALUES (?, ?, ?, 'text', ?, ?)
        """, (channel[0], channel[1], channel[2], channel[4], channel[5]))
        print(f"Created channel: {channel[1]} in group {channel[4]}")
    except Exception as e:
        print(f"Error creating channel {channel[1]}: {e}")

# Create sample messages
messages_data = [
    (1, 'Welcome to Electronics Level 2! Please introduce yourselves.', 1, 1, 'approved', datetime.now() - timedelta(days=2)),
    (2, 'Assignment 1 is now available. Please check the resources channel.', 2, 2, 'approved', datetime.now() - timedelta(days=1)),
    (3, 'Remember to wear safety equipment during all practical sessions.', 5, 2, 'approved', datetime.now() - timedelta(hours=6)),
    (4, 'New learning materials uploaded for automotive diagnostics.', 6, 2, 'approved', datetime.now() - timedelta(hours=3)),
    (5, 'School will be closed tomorrow for maintenance.', 7, 3, 'approved', datetime.now() - timedelta(hours=1))
]

for msg in messages_data:
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO messages (id, content, channel_id, author_id, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, msg)
        print(f"Created message in channel {msg[2]}")
    except Exception as e:
        print(f"Error creating message: {e}")

# Create sample resources
resources_data = [
    (1, 'Electronics Fundamentals PDF', 'Basic electronics theory and principles', 'document', 'electronics_basics.pdf', 1, 2, datetime.now()),
    (2, 'Welding Safety Video', 'Essential safety procedures for welding', 'video', 'welding_safety.mp4', 2, 2, datetime.now()),
    (3, 'Engine Diagnostic Guide', 'Step-by-step engine troubleshooting', 'document', 'engine_diagnostics.pdf', 3, 2, datetime.now())
]

for resource in resources_data:
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO resources (id, title, description, type, filename, group_id, uploaded_by, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, resource)
        print(f"Created resource: {resource[1]}")
    except Exception as e:
        print(f"Error creating resource {resource[1]}: {e}")

# Create sample sessions
sessions_data = [
    (1, 'Electronics Lab Session', 'Hands-on circuit building', 1, 2, datetime.now() + timedelta(hours=2), datetime.now() + timedelta(hours=4), 'scheduled'),
    (2, 'Welding Practice', 'Basic welding techniques practice', 2, 2, datetime.now() + timedelta(days=1), datetime.now() + timedelta(days=1, hours=2), 'scheduled'),
    (3, 'Engine Repair Workshop', 'Practical engine maintenance', 3, 2, datetime.now() + timedelta(days=2), datetime.now() + timedelta(days=2, hours=3), 'scheduled')
]

for session in sessions_data:
    try:
        cursor.execute("""
            INSERT OR REPLACE INTO sessions (id, title, description, group_id, instructor_id, start_time, end_time, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, session)
        print(f"Created session: {session[1]}")
    except Exception as e:
        print(f"Error creating session {session[1]}: {e}")

conn.commit()
conn.close()

print("\n✅ Sample data created successfully!")
print("\nAvailable groups:")
print("1. Electronics Level 2 (with channels: general, assignments, resources)")
print("2. Welding Basics (with channels: practice, safety)")
print("3. Automotive Repair (with channel: repairs)")
print("4. General Announcements (with channel: announcements)")
print("\nSample resources, messages, and sessions have been created.")