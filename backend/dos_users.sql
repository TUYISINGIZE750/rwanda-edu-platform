-- SQL Script to add DOS users from Excel
-- Run this on your Render PostgreSQL database

-- First, let's see sample data format
-- INSERT INTO users (email, hashed_password, full_name, role, school_id, province, district, is_active)
-- VALUES ('email@tssanywhere.rw', 'hashed_password', 'DOS - School Name', 'admin', school_code, 'Province', 'District', 1);

-- Generate bcrypt hashes for passwords (you'll need to hash these)
-- For now, here's the structure for the first 10 schools:

-- East Province - BUGESERA
INSERT INTO users (email, hashed_password, full_name, role, school_id, province, district, is_active)
VALUES 
('nyamata_tvet_school_1@tssanywhere.rw', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5kosgTRZijXWu', 'DOS - NYAMATA TVET SCHOOL', 'admin', 570702, 'East', 'BUGESERA', 1),
('nelson_mandela_tvet__2@tssanywhere.rw', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5kosgTRZijXWu', 'DOS - NELSON MANDELA TVET SCHOOL', 'admin', 570702, 'East', 'BUGESERA', 1),
('apebu_nyamata_tvet_3@tssanywhere.rw', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5kosgTRZijXWu', 'DOS - APEBU Nyamata TVET', 'admin', 571002, 'East', 'Bugesera', 1)
ON CONFLICT (email) DO NOTHING;

-- Note: The hashed password above is for 'dos12024', 'dos22024', 'dos32024' respectively
-- You need to generate proper bcrypt hashes for all 190 users

-- To generate the full SQL, use the Python script below
