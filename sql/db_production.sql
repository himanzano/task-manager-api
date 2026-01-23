-- Enable UUID extension (usually enabled by default in Supabase, but good practice)
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create ENUM type
DO $$ BEGIN
    CREATE TYPE taskstatus AS ENUM ('TODO', 'IN_PROGRESS', 'DONE');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Function to automatically update 'updated_at'
CREATE OR REPLACE FUNCTION handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ,
    CONSTRAINT uq_users_email UNIQUE (email)
);

-- Trigger for users
CREATE TRIGGER set_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION handle_updated_at();

-- Create tasks table
CREATE TABLE IF NOT EXISTS tasks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status taskstatus NOT NULL DEFAULT 'TODO',
    owner_id UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ,
    CONSTRAINT fk_tasks_owner
        FOREIGN KEY(owner_id) 
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- Indexes for performance
-- PK indexes are automatic.
-- Email unique index is created by CONSTRAINT uq_users_email.
CREATE INDEX IF NOT EXISTS idx_tasks_owner_id ON tasks(owner_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
-- Title index only if search feature is planned, strictly speaking redundant for simple list, 
-- but kept per original schema intent, changed to gin/trigram if advanced search, 
-- staying simple btree for exact match/sorting.
CREATE INDEX IF NOT EXISTS idx_tasks_title ON tasks(title);

-- Trigger for tasks
CREATE TRIGGER set_tasks_updated_at
BEFORE UPDATE ON tasks
FOR EACH ROW
EXECUTE FUNCTION handle_updated_at();
