import fdb
import pandas as pd

def fdb_to_excel(fdb_file, excel_file):
    con = None  # Initialize 'con' to None
    try:
        # Connect to the Firebird database
        con = fdb.connect(dsn=fdb_file, user='sysdba', password='masterkey')  # Modify username/password if needed
        cursor = con.cursor()

        # Fetch all table names
        cursor.execute("SELECT rdb$relation_name FROM rdb$relations WHERE rdb$system_flag = 0 AND rdb$view_blr IS NULL;")
        tables = [t[0].strip() for t in cursor.fetchall()]

        # Export each table to Excel
        with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
            for table in tables:
                query = f'SELECT * FROM {table}'
                data = pd.read_sql(query, con)
                data.to_excel(writer, sheet_name=table, index=False)

        print(f"Successfully exported Firebird database to {excel_file}")
    except fdb.DatabaseError as e:
        print(f"Error: {e}")
    finally:
        if con:  # Close the connection only if it's established
            con.close()

def excel_to_fdb(excel_file, fdb_file):
    con = None
    try:
        # Connect to the Firebird database (create new if it doesn't exist)
        con = fdb.create_database(dsn=fdb_file, user='sysdba', password='masterkey')
        cursor = con.cursor()

        # Load the Excel file
        excel_data = pd.ExcelFile(excel_file)
        for sheet_name in excel_data.sheet_names:
            df = excel_data.parse(sheet_name)

            # Generate column names and types for table creation
            columns = ', '.join([f'"{col}" VARCHAR(255)' for col in df.columns])
            cursor.execute(f'CREATE TABLE {sheet_name} ({columns})')

            # Insert data into the newly created table
            for row in df.itertuples(index=False):
                placeholders = ', '.join(['?'] * len(row))
                cursor.execute(f'INSERT INTO {sheet_name} VALUES ({placeholders})', row)

        con.commit()
        print(f"Successfully imported Excel data to {fdb_file}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if con:
            con.close()

def convert(file_path, option):
    if option == 'fdb_to_excel':
        if not file_path.endswith('.fdb'):
            print("Error: Please provide a valid Firebird (.fdb) file.")
            return
        excel_file = file_path.replace('.fdb', '.xlsx')
        fdb_to_excel(file_path, excel_file)

    elif option == 'excel_to_fdb':
        if not file_path.endswith('.xlsx'):
            print("Error: Please provide a valid Excel (.xlsx) file.")
            return
        fdb_file = file_path.replace('.xlsx', '.fdb')
        excel_to_fdb(file_path, fdb_file)

    else:
        print("Error: Invalid option. Please choose 'fdb_to_excel' or 'excel_to_fdb'.")

if __name__ == "__main__":
    # Example: Provide the path and option here for the function call
    file_path = input("Enter the file path: ")
    option = input("Choose conversion type ('fdb_to_excel' or 'excel_to_fdb'): ")
    convert(file_path, option)
