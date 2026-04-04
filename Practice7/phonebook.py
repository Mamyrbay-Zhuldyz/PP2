import psycopg2
import csv
from config import config

def create_table():
    """Create phonebook table if not exists"""
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(100) NOT NULL,
                last_name VARCHAR(100),
                phone VARCHAR(20) NOT NULL UNIQUE,
                email VARCHAR(100),
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        print(" Table 'contacts' is ready")
        cur.close()
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        if conn:
            conn.close()

def import_from_csv(filename='contacts.csv'):
    """Import contacts from CSV file"""
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
                        INSERT INTO contacts (first_name, last_name, phone, email, address)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (row['first_name'], row['last_name'], row['phone'], row['email'], row['address']))
                    count += 1
                except psycopg2.errors.UniqueViolation:
                    print(f"  Skipping duplicate phone: {row.get('phone', 'unknown')}")
                    conn.rollback()
                except Exception as e:
                    print(f"  Error adding {row.get('first_name', 'unknown')}: {e}")
                    conn.rollback()
        
        conn.commit()
        print(f" Imported {count} contacts from {filename}")
        cur.close()
    except FileNotFoundError:
        print(f" File {filename} not found!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

def add_contact():
    """Add a new contact manually"""
    conn = None
    try:
        print("\n--- Add New Contact ---")
        first_name = input("First name: ").strip()
        last_name = input("Last name: ").strip()
        phone = input("Phone: ").strip()
        email = input("Email: ").strip()
        address = input("Address: ").strip()
        
        if not first_name or not phone:
            print(" First name and phone are required!")
            return
        
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO contacts (first_name, last_name, phone, email, address)
            VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, phone, email, address))
        
        conn.commit()
        print(f" Contact '{first_name} {last_name}' added successfully!")
        cur.close()
    except psycopg2.errors.UniqueViolation:
        print(f" Phone '{phone}' already exists!")
        conn.rollback()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

def update_contact():
    """Update contact by ID"""
    conn = None
    try:
        show_all_contacts(show_id=True)
        
        contact_id = input("\nEnter contact ID to update: ").strip()
        if not contact_id.isdigit():
            print(" Invalid ID!")
            return
        
        print("\nWhat to update?")
        print("1. First name")
        print("2. Last name")
        print("3. Phone")
        print("4. Email")
        print("5. Address")
        print("6. All")
        
        choice = input("Choose option (1-6): ").strip()
        
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        if choice == '1':
            new_value = input("New first name: ").strip()
            cur.execute("UPDATE contacts SET first_name = %s WHERE id = %s", (new_value, contact_id))
        elif choice == '2':
            new_value = input("New last name: ").strip()
            cur.execute("UPDATE contacts SET last_name = %s WHERE id = %s", (new_value, contact_id))
        elif choice == '3':
            new_value = input("New phone: ").strip()
            cur.execute("UPDATE contacts SET phone = %s WHERE id = %s", (new_value, contact_id))
        elif choice == '4':
            new_value = input("New email: ").strip()
            cur.execute("UPDATE contacts SET email = %s WHERE id = %s", (new_value, contact_id))
        elif choice == '5':
            new_value = input("New address: ").strip()
            cur.execute("UPDATE contacts SET address = %s WHERE id = %s", (new_value, contact_id))
        elif choice == '6':
            first = input("New first name: ").strip()
            last = input("New last name: ").strip()
            phone = input("New phone: ").strip()
            email = input("New email: ").strip()
            address = input("New address: ").strip()
            cur.execute("""
                UPDATE contacts SET 
                    first_name = %s, last_name = %s, phone = %s, email = %s, address = %s 
                WHERE id = %s
            """, (first, last, phone, email, address, contact_id))
        else:
            print(" Invalid option!")
            return
        
        conn.commit()
        print(f" Contact {contact_id} updated!")
        cur.close()
    except psycopg2.errors.UniqueViolation:
        print(f" Phone already exists!")
        conn.rollback()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

def delete_contact():
    """Delete contact by ID, name, or phone"""
    conn = None
    try:
        print("\n--- Delete Contact ---")
        print("Delete by:")
        print("1. ID")
        print("2. Name")
        print("3. Phone")
        
        choice = input("Choose option (1-3): ").strip()
        
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        if choice == '1':
            contact_id = input("Enter contact ID: ").strip()
            cur.execute("DELETE FROM contacts WHERE id = %s RETURNING first_name", (contact_id,))
            result = cur.fetchone()
            if result:
                print(f" Contact '{result[0]}' deleted!")
            else:
                print(" Contact not found!")
        elif choice == '2':
            name = input("Enter name to search: ").strip()
            cur.execute("SELECT id, first_name, last_name FROM contacts WHERE first_name ILIKE %s OR last_name ILIKE %s", 
                       (f'%{name}%', f'%{name}%'))
            rows = cur.fetchall()
            if not rows:
                print(" No contacts found with that name!")
                return
            print("\nFound contacts:")
            for row in rows:
                print(f"  ID: {row[0]}, Name: {row[1]} {row[2]}")
            contact_id = input("\nEnter ID to delete: ").strip()
            cur.execute("DELETE FROM contacts WHERE id = %s", (contact_id,))
            print(" Contact deleted!")
        elif choice == '3':
            phone = input("Enter phone number: ").strip()
            cur.execute("DELETE FROM contacts WHERE phone = %s RETURNING first_name", (phone,))
            result = cur.fetchone()
            if result:
                print(f" Contact '{result[0]}' deleted!")
            else:
                print(" Contact not found!")
        else:
            print(" Invalid option!")
            return
        
        conn.commit()
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

def search_contacts():
    """Search contacts with different filters"""
    conn = None
    try:
        print("\n--- Search Contacts ---")
        print("Search by:")
        print("1. Name")
        print("2. Phone")
        print("3. Email")
        print("4. Show all")
        
        choice = input("Choose option (1-4): ").strip()
        
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        if choice == '1':
            name = input("Enter name to search: ").strip()
            cur.execute("""
                SELECT id, first_name, last_name, phone, email, address 
                FROM contacts 
                WHERE first_name ILIKE %s OR last_name ILIKE %s
                ORDER BY first_name
            """, (f'%{name}%', f'%{name}%'))
        elif choice == '2':
            phone = input("Enter phone to search: ").strip()
            cur.execute("""
                SELECT id, first_name, last_name, phone, email, address 
                FROM contacts 
                WHERE phone LIKE %s
                ORDER BY first_name
            """, (f'%{phone}%',))
        elif choice == '3':
            email = input("Enter email to search: ").strip()
            cur.execute("""
                SELECT id, first_name, last_name, phone, email, address 
                FROM contacts 
                WHERE email ILIKE %s
                ORDER BY first_name
            """, (f'%{email}%',))
        elif choice == '4':
            cur.execute("""
                SELECT id, first_name, last_name, phone, email, address 
                FROM contacts 
                ORDER BY first_name
            """)
        else:
            print(" Invalid option!")
            return
        
        rows = cur.fetchall()
        
        if not rows:
            print("\n No contacts found!")
        else:
            print("\n" + "="*70)
            print(f"{'ID':<5} {'Name':<25} {'Phone':<15} {'Email':<25}")
            print("="*70)
            for row in rows:
                name = f"{row[1]} {row[2]}".strip()
                print(f"{row[0]:<5} {name:<25} {row[3]:<15} {row[4]:<25}")
            print("="*70)
            print(f"Total: {len(rows)} contact(s)")
        
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

def show_all_contacts(show_id=False):
    """Display all contacts"""
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, first_name, last_name, phone, email, address 
            FROM contacts 
            ORDER BY first_name
        """)
        rows = cur.fetchall()
        
        if not rows:
            print("\n No contacts found!")
        else:
            print("\n" + "="*70)
            if show_id:
                print(f"{'ID':<5} {'Name':<25} {'Phone':<15} {'Email':<25}")
            else:
                print(f"{'Name':<25} {'Phone':<15} {'Email':<25}")
            print("="*70)
            for row in rows:
                name = f"{row[1]} {row[2]}".strip()
                if show_id:
                    print(f"{row[0]:<5} {name:<25} {row[3]:<15} {row[4]:<25}")
                else:
                    print(f"{name:<25} {row[3]:<15} {row[4]:<25}")
            print("="*70)
            print(f"Total: {len(rows)} contact(s)")
        
        cur.close()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

def menu():
    """Main menu"""
    while True:
        print("\n" + "="*50)
        print("        PHONEBOOK MANAGER")
        print("="*50)
        print("1. Show all contacts")
        print("2. Add new contact")
        print("3. Search contacts")
        print("4. Update contact")
        print("5. Delete contact")
        print("6. Import from CSV")
        print("7. Exit")
        print("="*50)
        
        choice = input("Choose option (1-7): ").strip()
        
        if choice == '1':
            show_all_contacts()
        elif choice == '2':
            add_contact()
        elif choice == '3':
            search_contacts()
        elif choice == '4':
            update_contact()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            filename = input("CSV filename (default: contacts.csv): ").strip()
            if not filename:
                filename = 'contacts.csv'
            import_from_csv(filename)
        elif choice == '7':
            print("\n Goodbye!")
            break
        else:
            print("\n Invalid option! Please choose 1-7.")

if __name__ == "__main__":
    create_table()
    menu()