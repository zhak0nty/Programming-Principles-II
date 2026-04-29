DROP PROCEDURE IF EXISTS add_phone(varchar, varchar, varchar);
DROP PROCEDURE IF EXISTS move_to_group(varchar, varchar);
DROP PROCEDURE IF EXISTS upsert_contact_extended(varchar, varchar, varchar, date, varchar, varchar, varchar);
DROP PROCEDURE IF EXISTS delete_contact_by_name(varchar, varchar);

CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    SELECT c.id
    INTO v_contact_id
    FROM contacts c
    WHERE LOWER(trim(c.first_name || ' ' || c.last_name)) = LOWER(trim(p_contact_name))
    ORDER BY c.id
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;

    IF lower(p_type) NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Invalid phone type: %', p_type;
    END IF;

    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, lower(p_type))
    ON CONFLICT DO NOTHING;
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id INTEGER;
BEGIN
    INSERT INTO groups (name) VALUES (trim(p_group_name))
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO v_group_id FROM groups WHERE name = trim(p_group_name);

    SELECT c.id
    INTO v_contact_id
    FROM contacts c
    WHERE LOWER(trim(c.first_name || ' ' || c.last_name)) = LOWER(trim(p_contact_name))
    ORDER BY c.id
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found', p_contact_name;
    END IF;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE id = v_contact_id;
END;
$$;

CREATE OR REPLACE PROCEDURE upsert_contact_extended(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_email VARCHAR,
    p_birthday DATE,
    p_group_name VARCHAR,
    p_phone VARCHAR,
    p_phone_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id INTEGER;
BEGIN
    INSERT INTO groups (name) VALUES (COALESCE(NULLIF(trim(p_group_name), ''), 'Other'))
    ON CONFLICT (name) DO NOTHING;

    SELECT id
    INTO v_group_id
    FROM groups
    WHERE name = COALESCE(NULLIF(trim(p_group_name), ''), 'Other');

    SELECT c.id
    INTO v_contact_id
    FROM contacts c
    WHERE LOWER(c.first_name) = LOWER(trim(p_first_name))
      AND LOWER(COALESCE(c.last_name, '')) = LOWER(trim(COALESCE(p_last_name, '')))
    ORDER BY c.id
    LIMIT 1;

    IF v_contact_id IS NULL THEN
        INSERT INTO contacts (first_name, last_name, email, birthday, group_id)
        VALUES (
            trim(p_first_name),
            trim(COALESCE(p_last_name, '')),
            NULLIF(trim(COALESCE(p_email, '')), ''),
            p_birthday,
            v_group_id
        )
        RETURNING id INTO v_contact_id;
    ELSE
        UPDATE contacts
        SET email = NULLIF(trim(COALESCE(p_email, '')), ''),
            birthday = p_birthday,
            group_id = v_group_id
        WHERE id = v_contact_id;
    END IF;

    IF trim(COALESCE(p_phone, '')) <> '' THEN
        INSERT INTO phones (contact_id, phone, type)
        VALUES (
            v_contact_id,
            trim(p_phone),
            COALESCE(NULLIF(lower(trim(COALESCE(p_phone_type, ''))), ''), 'mobile')
        )
        ON CONFLICT DO NOTHING;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact_by_name(
    p_first_name VARCHAR,
    p_last_name VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE LOWER(first_name) = LOWER(trim(p_first_name))
      AND LOWER(COALESCE(last_name, '')) = LOWER(trim(COALESCE(p_last_name, '')));
END;
$$;
