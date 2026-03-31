CREATE OR REPLACE PROCEDURE upsert_contact(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR,
    p_email VARCHAR DEFAULT NULL,
    p_address TEXT DEFAULT NULL
)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE phone = p_phone) THEN
        UPDATE contacts 
        SET first_name = p_first_name,
            last_name = p_last_name,
            email = COALESCE(p_email, email),
            address = COALESCE(p_address, address)
        WHERE phone = p_phone;
        RAISE NOTICE 'Contact with phone % updated', p_phone;
    ELSE
        INSERT INTO contacts (first_name, last_name, phone, email, address)
        VALUES (p_first_name, p_last_name, p_phone, p_email, p_address);
        RAISE NOTICE 'New contact inserted: % %', p_first_name, p_last_name;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE bulk_insert_contacts(
    contacts_data TEXT[][]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
    contact_record TEXT[];
    invalid_phones TEXT[] := '{}';
    phone_valid BOOLEAN;
BEGIN
    FOR i IN 1..array_length(contacts_data, 1) LOOP
        contact_record := contacts_data[i];
        
        phone_valid := (contact_record[3] ~ '^[+0-9][0-9\-+\s]{5,20}$');
        
        IF phone_valid THEN
            CALL upsert_contact(
                contact_record[1],
                contact_record[2],
                contact_record[3],
                contact_record[4],
                contact_record[5]
            );
        ELSE
            invalid_phones := array_append(invalid_phones, 
                format('Invalid phone: %s for %s %s', 
                    contact_record[3], contact_record[1], contact_record[2]));
        END IF;
    END LOOP;
    
    IF array_length(invalid_phones, 1) > 0 THEN
        RAISE NOTICE 'Invalid contacts: %', invalid_phones;
    ELSE
        RAISE NOTICE 'All contacts inserted/updated successfully!';
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact_by(
    p_first_name VARCHAR DEFAULT NULL,
    p_last_name VARCHAR DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL
)
LANGUAGE plpgsql AS $$
DECLARE
    deleted_count INT;
BEGIN
    IF p_first_name IS NULL AND p_last_name IS NULL AND p_phone IS NULL THEN
        RAISE EXCEPTION 'At least one parameter must be provided';
    END IF;
    
    IF p_phone IS NOT NULL THEN
        DELETE FROM contacts WHERE phone = p_phone;
        GET DIAGNOSTICS deleted_count = ROW_COUNT;
        RAISE NOTICE 'Deleted % contact(s) with phone: %', deleted_count, p_phone;
    END IF;
    
    IF p_first_name IS NOT NULL THEN
        IF p_last_name IS NOT NULL THEN
            DELETE FROM contacts 
            WHERE first_name = p_first_name AND last_name = p_last_name;
        ELSE
            DELETE FROM contacts WHERE first_name = p_first_name;
        END IF;
        GET DIAGNOSTICS deleted_count = ROW_COUNT;
        RAISE NOTICE 'Deleted % contact(s) with name: % %', 
            deleted_count, 
            COALESCE(p_first_name, 'NULL'),
            COALESCE(p_last_name, '');
    END IF;
END;
$$;