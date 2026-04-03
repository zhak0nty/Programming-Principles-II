DROP FUNCTION IF EXISTS get_contacts_by_pattern(text);
DROP FUNCTION IF EXISTS get_contacts_page(integer, integer);
DROP FUNCTION IF EXISTS bulk_insert_contacts(text[], text[], text[]);

CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p text)
RETURNS TABLE(id integer, first_name character varying, last_name character varying, phone character varying)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.last_name, c.phone
    FROM contacts c
    WHERE c.first_name ILIKE '%' || p || '%'
       OR c.last_name ILIKE '%' || p || '%'
       OR c.phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_page(p_limit integer, p_offset integer)
RETURNS TABLE(id integer, first_name character varying, last_name character varying, phone character varying)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.last_name, c.phone
    FROM contacts c
    ORDER BY c.first_name, c.last_name
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION bulk_insert_contacts(p_first_names text[], p_last_names text[], p_phones text[])
RETURNS TABLE(bad_first text, bad_last text, bad_phone text, reason text)
LANGUAGE plpgsql
AS $$
DECLARE
    i integer;
    n integer;
    fn text;
    ln text;
    ph text;
    digits text;
BEGIN
    n := COALESCE(array_length(p_first_names, 1), 0);
    IF n = 0 THEN
        RETURN;
    END IF;
    IF COALESCE(array_length(p_last_names, 1), 0) <> n OR COALESCE(array_length(p_phones, 1), 0) <> n THEN
        bad_first := NULL;
        bad_last := NULL;
        bad_phone := NULL;
        reason := 'array length mismatch';
        RETURN NEXT;
        RETURN;
    END IF;
    FOR i IN 1..n LOOP
        fn := p_first_names[i];
        ln := COALESCE(p_last_names[i], '');
        ph := p_phones[i];
        IF fn IS NULL OR trim(fn) = '' THEN
            bad_first := fn;
            bad_last := ln;
            bad_phone := ph;
            reason := 'empty first name';
            RETURN NEXT;
        ELSE
            digits := regexp_replace(ph, '[^0-9]', '', 'g');
            IF length(digits) < 10 OR length(digits) > 15 THEN
                bad_first := fn;
                bad_last := ln;
                bad_phone := ph;
                reason := 'invalid phone';
                RETURN NEXT;
            ELSE
                INSERT INTO contacts (first_name, last_name, phone)
                VALUES (trim(fn), trim(ln), ph);
            END IF;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
