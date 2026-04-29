DROP FUNCTION IF EXISTS get_contacts_page(integer, integer, text);
DROP FUNCTION IF EXISTS search_contacts(text);
DROP FUNCTION IF EXISTS get_contacts_by_filters(text, text, text);
DROP FUNCTION IF EXISTS bulk_insert_contacts_extended(text[], text[], text[], text[], text[], text[], text[]);

CREATE OR REPLACE FUNCTION get_contacts_page(p_limit integer, p_offset integer, p_sort text DEFAULT 'name')
RETURNS TABLE(
    id integer,
    first_name varchar,
    last_name varchar,
    email varchar,
    birthday date,
    group_name varchar,
    created_at timestamp
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name, c.created_at
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    ORDER BY
        CASE WHEN p_sort = 'name' THEN lower(c.first_name || ' ' || c.last_name) END ASC,
        CASE WHEN p_sort = 'birthday' THEN c.birthday END ASC NULLS LAST,
        CASE WHEN p_sort = 'date' THEN c.created_at END DESC,
        c.id ASC
    LIMIT p_limit OFFSET p_offset;
END;
$$;

CREATE OR REPLACE FUNCTION search_contacts(p_query text)
RETURNS TABLE(
    id integer,
    first_name varchar,
    last_name varchar,
    email varchar,
    birthday date,
    group_name varchar
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.last_name ILIKE '%' || p_query || '%'
       OR COALESCE(c.email, '') ILIKE '%' || p_query || '%'
       OR COALESCE(p.phone, '') ILIKE '%' || p_query || '%'
    ORDER BY c.first_name, c.last_name;
END;
$$;

CREATE OR REPLACE FUNCTION get_contacts_by_filters(
    p_group_name text DEFAULT NULL,
    p_email_pattern text DEFAULT NULL,
    p_sort text DEFAULT 'name'
)
RETURNS TABLE(
    id integer,
    first_name varchar,
    last_name varchar,
    email varchar,
    birthday date,
    group_name varchar
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    WHERE (p_group_name IS NULL OR g.name = p_group_name)
      AND (p_email_pattern IS NULL OR COALESCE(c.email, '') ILIKE '%' || p_email_pattern || '%')
    ORDER BY
        CASE WHEN p_sort = 'name' THEN lower(c.first_name || ' ' || c.last_name) END ASC,
        CASE WHEN p_sort = 'birthday' THEN c.birthday END ASC NULLS LAST,
        CASE WHEN p_sort = 'date' THEN c.created_at END DESC,
        c.id ASC;
END;
$$;

CREATE OR REPLACE FUNCTION bulk_insert_contacts_extended(
    p_first_names text[],
    p_last_names text[],
    p_emails text[],
    p_birthdays text[],
    p_group_names text[],
    p_phones text[],
    p_phone_types text[]
)
RETURNS TABLE(
    bad_first text,
    bad_last text,
    bad_phone text,
    reason text
)
LANGUAGE plpgsql
AS $$
DECLARE
    i integer;
    n integer;
    fn text;
    ln text;
    em text;
    bd date;
    gn text;
    ph text;
    pt text;
    grp_id integer;
    c_id integer;
BEGIN
    n := COALESCE(array_length(p_first_names, 1), 0);
    IF n = 0 THEN
        RETURN;
    END IF;

    IF COALESCE(array_length(p_last_names, 1), 0) <> n
       OR COALESCE(array_length(p_emails, 1), 0) <> n
       OR COALESCE(array_length(p_birthdays, 1), 0) <> n
       OR COALESCE(array_length(p_group_names, 1), 0) <> n
       OR COALESCE(array_length(p_phones, 1), 0) <> n
       OR COALESCE(array_length(p_phone_types, 1), 0) <> n THEN
        bad_first := NULL;
        bad_last := NULL;
        bad_phone := NULL;
        reason := 'array length mismatch';
        RETURN NEXT;
        RETURN;
    END IF;

    FOR i IN 1..n LOOP
        fn := trim(COALESCE(p_first_names[i], ''));
        ln := trim(COALESCE(p_last_names[i], ''));
        em := NULLIF(trim(COALESCE(p_emails[i], '')), '');
        gn := COALESCE(NULLIF(trim(COALESCE(p_group_names[i], '')), ''), 'Other');
        ph := trim(COALESCE(p_phones[i], ''));
        pt := lower(COALESCE(NULLIF(trim(COALESCE(p_phone_types[i], '')), ''), 'mobile'));

        IF fn = '' THEN
            bad_first := fn;
            bad_last := ln;
            bad_phone := ph;
            reason := 'empty first name';
            RETURN NEXT;
            CONTINUE;
        END IF;

        IF ph = '' THEN
            bad_first := fn;
            bad_last := ln;
            bad_phone := ph;
            reason := 'empty phone';
            RETURN NEXT;
            CONTINUE;
        END IF;

        IF pt NOT IN ('home', 'work', 'mobile') THEN
            bad_first := fn;
            bad_last := ln;
            bad_phone := ph;
            reason := 'invalid phone type';
            RETURN NEXT;
            CONTINUE;
        END IF;

        IF NULLIF(trim(COALESCE(p_birthdays[i], '')), '') IS NULL THEN
            bd := NULL;
        ELSE
            BEGIN
                bd := p_birthdays[i]::date;
            EXCEPTION WHEN others THEN
                bad_first := fn;
                bad_last := ln;
                bad_phone := ph;
                reason := 'invalid birthday';
                RETURN NEXT;
                CONTINUE;
            END;
        END IF;

        INSERT INTO groups (name) VALUES (gn)
        ON CONFLICT (name) DO NOTHING;

        SELECT id INTO grp_id FROM groups WHERE name = gn;

        INSERT INTO contacts (first_name, last_name, email, birthday, group_id)
        VALUES (fn, ln, em, bd, grp_id)
        RETURNING id INTO c_id;

        INSERT INTO phones (contact_id, phone, type)
        VALUES (c_id, ph, pt)
        ON CONFLICT DO NOTHING;
    END LOOP;
END;
$$;
