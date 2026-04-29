CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO groups (name)
VALUES ('Family'), ('Work'), ('Friend'), ('Other')
ON CONFLICT (name) DO NOTHING;

CREATE TABLE IF NOT EXISTS contacts (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL DEFAULT '',
    email VARCHAR(100),
    birthday DATE,
    group_id INTEGER REFERENCES groups(id),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

ALTER TABLE contacts ADD COLUMN IF NOT EXISTS email VARCHAR(100);
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS birthday DATE;
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS group_id INTEGER REFERENCES groups(id);
ALTER TABLE contacts ADD COLUMN IF NOT EXISTS created_at TIMESTAMP NOT NULL DEFAULT NOW();

CREATE TABLE IF NOT EXISTS phones (
    id SERIAL PRIMARY KEY,
    contact_id INTEGER NOT NULL REFERENCES contacts(id) ON DELETE CASCADE,
    phone VARCHAR(20) NOT NULL,
    type VARCHAR(10) NOT NULL CHECK (type IN ('home', 'work', 'mobile'))
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_phones_contact_phone_type
ON phones(contact_id, phone, type);

DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'contacts' AND column_name = 'phone'
    ) THEN
        INSERT INTO phones (contact_id, phone, type)
        SELECT c.id, c.phone, 'mobile'
        FROM contacts c
        WHERE c.phone IS NOT NULL
          AND trim(c.phone) <> ''
          AND NOT EXISTS (
              SELECT 1
              FROM phones p
              WHERE p.contact_id = c.id
                AND p.phone = c.phone
                AND p.type = 'mobile'
          );
    END IF;
END;
$$;
