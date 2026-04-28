import psycopg2
import csv
import json
import os
from config import config

def create_tables():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        with open('schema.sql', 'r', encoding='utf-8') as f:
            cur.execute(f.read())
        conn.commit()
        print("Tables created/updated!")
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

def create_procedures():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        with open('functions.sql', 'r', encoding='utf-8') as f:
            cur.execute(f.read())
        with open('procedures.sql', 'r', encoding='utf-8') as f:
            cur.execute(f.read())
        conn.commit()
        print("Procedures created!")
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

def import_csv(filename='contacts.csv'):
    conn = None
    count = 0
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    cur.execute("""
                        INSERT INTO contacts (first_name, last_name, phone, email, address, birthday)
                        VALUES (%s, %s, %s, %s, %s, %s::DATE)
                        ON CONFLICT (phone) DO UPDATE SET
                            first_name=EXCLUDED.first_name, last_name=EXCLUDED.last_name,
                            email=COALESCE(EXCLUDED.email, contacts.email),
                            birthday=COALESCE(EXCLUDED.birthday, contacts.birthday)
                        RETURNING id
                    """, (row['first_name'], row['last_name'], row['phone'],
                          row.get('email') or None, row.get('address') or None,
                          row.get('birthday') or None))
                    contact_id = cur.fetchone()[0]
                    phone_type = row.get('phone_type', 'mobile')
                    cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                               (contact_id, row['phone'], phone_type))
                    group_name = row.get('group')
                    if group_name:
                        cur.execute("SELECT id FROM groups WHERE name=%s", (group_name,))
                        g = cur.fetchone()
                        if g:
                            cur.execute("UPDATE contacts SET group_id=%s WHERE id=%s", (g[0], contact_id))
                    count += 1
                    conn.commit()
                except Exception as e:
                    print(f"  Skipping {row.get('first_name','?')}: {e}")
                    conn.rollback()
        print(f"Imported {count} contacts")
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

def export_json(filename='contacts_export.json'):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("""
            SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, c.address, c.created_at,
                   g.name AS group_name,
                   json_agg(json_build_object('phone', p.phone, 'type', p.type)) AS phones
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            LEFT JOIN phones p ON c.id = p.contact_id
            GROUP BY c.id, g.name ORDER BY c.first_name
        """)
        contacts = []
        for row in cur.fetchall():
            contacts.append({
                "id": row[0], "first_name": row[1], "last_name": row[2],
                "email": row[3], "birthday": row[4].isoformat() if row[4] else None,
                "address": row[5], "created_at": row[6].isoformat() if row[6] else None,
                "group": row[7], "phones": row[8] if row[8] and row[8][0] and row[8][0]['phone'] else []
            })
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(contacts, f, ensure_ascii=False, indent=2)
        print(f"Exported {len(contacts)} contacts to {filename}")
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

def import_json(filename='contacts_import.json'):
    if not os.path.exists(filename):
        print(f"File {filename} not found!")
        return
    conn = None
    added = skipped = overwritten = 0
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for c in data:
            try:
                name = f"{c.get('first_name','')} {c.get('last_name','')}".strip()
                phone = c.get('phones', [{}])[0].get('phone', '') if c.get('phones') else ''
                cur.execute("SELECT id FROM contacts WHERE phone=%s", (phone,))
                if cur.fetchone():
                    ans = input(f"Contact '{name}' exists. Overwrite? (y/n): ").lower()
                    if ans != 'y':
                        skipped += 1
                        continue
                    overwritten += 1
                cur.execute("""INSERT INTO contacts (first_name, last_name, phone, email, birthday, address)
                    VALUES (%s,%s,%s,%s,%s::DATE,%s) ON CONFLICT (phone) DO UPDATE SET
                    first_name=EXCLUDED.first_name, last_name=EXCLUDED.last_name,
                    email=COALESCE(EXCLUDED.email, contacts.email)
                    RETURNING id""",
                    (c.get('first_name'), c.get('last_name'), phone, c.get('email'), c.get('birthday'), c.get('address')))
                cid = cur.fetchone()[0]
                pt = c.get('phones', [{}])[0].get('type', 'mobile')
                cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING", (cid, phone, pt))
                gn = c.get('group')
                if gn:
                    cur.execute("SELECT id FROM groups WHERE name=%s", (gn,))
                    g = cur.fetchone()
                    if g:
                        cur.execute("UPDATE contacts SET group_id=%s WHERE id=%s", (g[0], cid))
                added += 1
                conn.commit()
            except Exception as e:
                print(f"Error: {e}")
                conn.rollback()
        print(f"Added: {added}, Overwritten: {overwritten}, Skipped: {skipped}")
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

def filter_by_group():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM groups ORDER BY name")
        groups = cur.fetchall()
        print("\nGroups:")
        for g in groups:
            print(f"  {g[0]}. {g[1]}")
        choice = input("Enter group number or name: ").strip()
        if choice.isdigit():
            cur.execute("""SELECT c.id, c.first_name, c.last_name, c.phone, c.email, g.name
                FROM contacts c LEFT JOIN groups g ON c.group_id=g.id WHERE c.group_id=%s ORDER BY c.first_name""", (int(choice),))
        else:
            cur.execute("""SELECT c.id, c.first_name, c.last_name, c.phone, c.email, g.name
                FROM contacts c LEFT JOIN groups g ON c.group_id=g.id WHERE g.name ILIKE %s ORDER BY c.first_name""", (f'%{choice}%',))
        rows = cur.fetchall()
        if rows:
            print(f"\n{'ID':<5} {'Name':<25} {'Phone':<15} {'Email':<25} {'Group':<10}")
            print("-"*80)
            for r in rows:
                print(f"{r[0]:<5} {f'{r[1]} {r[2] or ''}':<25} {r[3]:<15} {r[4] or '':<25} {r[5] or 'None':<10}")
            print(f"Total: {len(rows)}")
        else:
            print("No contacts found!")
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

def search_by_email():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        pattern = input("Enter email to search: ").strip()
        cur.execute("""SELECT c.id, c.first_name, c.last_name, c.phone, c.email,
            STRING_AGG(p.phone || ' (' || p.type || ')', ', ')
            FROM contacts c LEFT JOIN phones p ON c.id=p.contact_id
            WHERE c.email ILIKE %s GROUP BY c.id ORDER BY c.first_name""", (f'%{pattern}%',))
        rows = cur.fetchall()
        if rows:
            print(f"\n{'ID':<5} {'Name':<25} {'Email':<30} {'Phones':<20}")
            print("-"*80)
            for r in rows:
                print(f"{r[0]:<5} {f'{r[1]} {r[2] or ''}':<25} {r[4] or '':<30} {r[5] or r[3]:<20}")
            print(f"Total: {len(rows)}")
        else:
            print("No contacts found!")
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

def sort_contacts():
    conn = None
    try:
        print("\nSort by: 1. Name  2. Birthday  3. Date added")
        choice = input("Choose: ").strip()
        order = "c.first_name"
        if choice == '2':
            order = "c.birthday NULLS LAST"
        elif choice == '3':
            order = "c.created_at DESC"
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(f"""SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, c.created_at, g.name,
            STRING_AGG(p.phone || ' (' || p.type || ')', ', ')
            FROM contacts c LEFT JOIN groups g ON c.group_id=g.id LEFT JOIN phones p ON c.id=p.contact_id
            GROUP BY c.id, g.name ORDER BY {order}""")
        rows = cur.fetchall()
        if rows:
            print(f"\n{'ID':<5} {'Name':<25} {'Email':<25} {'Birthday':<12} {'Group':<10}")
            print("-"*90)
            for r in rows:
                bd = r[4].strftime('%d.%m.%Y') if r[4] else 'None'
                print(f"{r[0]:<5} {f'{r[1]} {r[2] or ''}':<25} {r[3] or '':<25} {bd:<12} {r[6] or 'None':<10}")
            print(f"Total: {len(rows)}")
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

def paginated_nav():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        try:
            ps = int(input("Records per page: ").strip())
            if ps <= 0:
                ps = 5
        except:
            ps = 5
        cur.execute("SELECT COUNT(*) FROM contacts")
        total = cur.fetchone()[0]
        total_pages = (total + ps - 1) // ps
        if total == 0:
            print("No contacts!")
            return
        page = 1
        while True:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (page, ps))
            rows = cur.fetchall()
            print(f"\nPage {page} of {total_pages}")
            print(f"{'ID':<5} {'Name':<25} {'Phone':<15} {'Email':<25}")
            print("-"*75)
            for r in rows:
                print(f"{r[0]:<5} {f'{r[1]} {r[2] or ''}':<25} {r[3]:<15} {r[4] or '':<25}")
            print("\n[n]ext [p]rev [q]uit")
            nav = input("> ").lower()
            if nav in ('n', 'next') and page < total_pages:
                page += 1
            elif nav in ('p', 'prev') and page > 1:
                page -= 1
            elif nav in ('q', 'quit'):
                break
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

def add_phone_menu():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        print("\n--- Add Phone to Contact ---")
        name = input("Contact name (First Last): ").strip()
        
        # Check if contact exists
        cur.execute("SELECT id, first_name, last_name FROM contacts WHERE TRIM(CONCAT(first_name, ' ', COALESCE(last_name, ''))) ILIKE %s", (name,))
        result = cur.fetchone()
        
        if not result:
            # Contact not found - create new one
            print(f"Contact '{name}' not found!")
            create = input("Create new contact? (y/n): ").strip().lower()
            if create != 'y':
                print("Cancelled.")
                cur.close()
                return
            
            # Split name
            parts = name.split(' ', 1)
            first = parts[0]
            last = parts[1] if len(parts) > 1 else ''
            
            email = input("Email (optional): ").strip() or None
            address = input("Address (optional): ").strip() or None
            birthday = input("Birthday YYYY-MM-DD (optional): ").strip() or None
            phone = input("Phone number: ").strip()
            
            if not phone:
                print("Phone is required!")
                cur.close()
                return
            
            print("Phone type: 1. home  2. work  3. mobile")
            type_choice = input("Choose (1-3): ").strip()
            phone_type = {'1': 'home', '2': 'work', '3': 'mobile'}.get(type_choice, 'mobile')
            
            # Insert new contact
            cur.execute("""
                INSERT INTO contacts (first_name, last_name, phone, email, address, birthday)
                VALUES (%s, %s, %s, %s, %s, %s::DATE)
                ON CONFLICT (phone) DO NOTHING
                RETURNING id
            """, (first, last, phone, email, address, birthday))
            
            new_result = cur.fetchone()
            if new_result:
                contact_id = new_result[0]
                cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                           (contact_id, phone, phone_type))
                conn.commit()
                print(f"New contact '{name}' created with phone {phone} ({phone_type})")
            else:
                print(f"Phone {phone} already exists!")
                conn.rollback()
            cur.close()
            return
        
        # Contact exists - add new phone
        print(f"Found: {result[1]} {result[2] or ''}")
        phone = input("Enter new phone number: ").strip()
        
        if not phone:
            print("Phone is required!")
            cur.close()
            return
        
        print("Phone type: 1. home  2. work  3. mobile")
        type_choice = input("Choose (1-3): ").strip()
        phone_type = {'1': 'home', '2': 'work', '3': 'mobile'}.get(type_choice, 'mobile')
        
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, phone_type))
        conn.commit()
        print(f"Phone {phone} ({phone_type}) added to {name}")
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            
def move_to_group_menu():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        name = input("Contact name: ").strip()
        group = input("Group name: ").strip()
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        print(f"{name} moved to {group}")
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

def search_extended():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        q = input("Search query: ").strip()
        cur.execute("SELECT * FROM search_contacts(%s)", (q,))
        rows = cur.fetchall()
        if rows:
            print(f"\n{'ID':<5} {'Name':<25} {'Email':<25} {'Phones':<30}")
            print("-"*85)
            for r in rows:
                print(f"{r[0]:<5} {f'{r[1]} {r[2] or ''}':<25} {r[3] or '':<25} {r[6] or 'None':<30}")
            print(f"Total: {len(rows)}")
        else:
            print("No results!")
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

def menu():
    while True:
        print("\n" + "=" * 50)
        print("   PHONEBOOK MANAGER (Practice 9)")
        print("=" * 50)
        print("1.  Show contacts (sorted)")
        print("2.  Search by email")
        print("3.  Extended search")
        print("4.  Filter by group")
        print("5.  Paginated navigation")
        print("6.  Add phone to contact")
        print("7.  Move contact to group")
        print("8.  Import from CSV")
        print("9.  Export to JSON")
        print("10. Import from JSON")
        print("11. Exit")
        c = input("Choose (1-11): ").strip()
        if c == '1': sort_contacts()
        elif c == '2': search_by_email()
        elif c == '3': search_extended()
        elif c == '4': filter_by_group()
        elif c == '5': paginated_nav()
        elif c == '6': add_phone_menu()
        elif c == '7': move_to_group_menu()
        elif c == '8':
            f = input("CSV file (default: contacts.csv): ").strip() or 'contacts.csv'
            import_csv(f)
        elif c == '9':
            f = input("JSON file (default: contacts_export.json): ").strip() or 'contacts_export.json'
            export_json(f)
        elif c == '10':
            f = input("JSON file (default: contacts_import.json): ").strip() or 'contacts_import.json'
            import_json(f)
        elif c == '11':
            print("Goodbye!")
            return
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    create_tables()
    create_procedures()
    menu()