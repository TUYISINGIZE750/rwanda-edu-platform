-- Add format_data column to messages table for storing text formatting
ALTER TABLE messages ADD COLUMN format_data JSON;
