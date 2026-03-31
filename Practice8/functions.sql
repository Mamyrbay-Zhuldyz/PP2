CREATE OR REPLACE FUNCTION search_contacts_by_pattern(search_text TEXT)
RETURNS TABLE(
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR,
    email VARCHAR,
    address TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.last_name, c.phone, c.email, c.address
    FROM contacts c
    WHERE c.first_name ILIKE '%' || search_text || '%'
       OR c.last_name ILIKE '%' || search_text || '%'
       OR c.phone ILIKE '%' || search_text || '%'
    ORDER BY c.first_name;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(
    page_num INT,
    page_size INT
)
RETURNS TABLE(
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR,
    email VARCHAR,
    address TEXT,
    total_count BIGINT
) AS $$
DECLARE
    offset_val INT;
    total BIGINT;
BEGIN
    offset_val := (page_num - 1) * page_size;
    SELECT COUNT(*) INTO total FROM contacts;
    
    RETURN QUERY
    SELECT 
        c.id, c.first_name, c.last_name, c.phone, c.email, c.address,
        total AS total_count
    FROM contacts c
    ORDER BY c.first_name
    LIMIT page_size
    OFFSET offset_val;
END;
$$ LANGUAGE plpgsql;