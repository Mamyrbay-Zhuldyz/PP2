CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_contact_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id FROM contacts 
    WHERE TRIM(CONCAT(first_name, ' ', COALESCE(last_name, ''))) ILIKE TRIM(p_contact_name) LIMIT 1;
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found!', p_contact_name;
    END IF;
    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Invalid phone type: %', p_type;
    END IF;
    INSERT INTO phones (contact_id, phone, type) VALUES (v_contact_id, p_phone, p_type);
END;
$$;

CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE v_contact_id INTEGER; v_group_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id FROM contacts 
    WHERE TRIM(CONCAT(first_name, ' ', COALESCE(last_name, ''))) ILIKE TRIM(p_contact_name) LIMIT 1;
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found!', p_contact_name;
    END IF;
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name) RETURNING id INTO v_group_id;
    END IF;
    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
END;
$$;

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(id INTEGER, first_name VARCHAR, last_name VARCHAR, email VARCHAR, birthday DATE, group_name VARCHAR, phones TEXT, created_at TIMESTAMP) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT ON (c.id) c.id, c.first_name, c.last_name, c.email, c.birthday, g.name AS group_name,
        STRING_AGG(p.phone || ' (' || p.type || ')', ', ') AS phones, c.created_at
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.first_name ILIKE '%' || p_query || '%'
       OR c.last_name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR c.phone ILIKE '%' || p_query || '%'
       OR EXISTS (SELECT 1 FROM phones WHERE contact_id = c.id AND phone ILIKE '%' || p_query || '%')
    GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name, c.created_at
    ORDER BY c.id, c.first_name;
END;
$$ LANGUAGE plpgsql;