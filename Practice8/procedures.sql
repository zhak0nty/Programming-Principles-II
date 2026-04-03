DROP PROCEDURE IF EXISTS upsert_contact(character varying, character varying, character varying);
DROP PROCEDURE IF EXISTS delete_contact_by_name_or_phone(boolean, character varying, character varying);

CREATE OR REPLACE PROCEDURE upsert_contact(
    p_first_name character varying,
    p_last_name character varying,
    p_phone character varying
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1 FROM contacts c
        WHERE c.first_name = p_first_name
          AND COALESCE(c.last_name, '') = COALESCE(p_last_name, '')
    ) THEN
        UPDATE contacts SET phone = p_phone
        WHERE first_name = p_first_name
          AND COALESCE(last_name, '') = COALESCE(p_last_name, '');
    ELSE
        INSERT INTO contacts (first_name, last_name, phone)
        VALUES (p_first_name, COALESCE(p_last_name, ''), p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact_by_name_or_phone(
    p_by_phone boolean,
    p_first_name character varying,
    p_phone character varying
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_by_phone THEN
        DELETE FROM contacts WHERE phone = p_phone;
    ELSE
        DELETE FROM contacts WHERE LOWER(first_name) = LOWER(p_first_name);
    END IF;
END;
$$;
