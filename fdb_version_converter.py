import subprocess
import os

def backup_fdb(firebird_2_5_path, fdb_file, backup_file):
    try:
        # Ensure paths are correct
        if not os.path.isfile(fdb_file):
            raise FileNotFoundError(f"Database file not found: {fdb_file}")

        gbak_path = os.path.join(firebird_2_5_path, 'gbak.exe')
        if not os.path.isfile(gbak_path):
            raise FileNotFoundError(f"'gbak' not found at: {gbak_path}")

        # Command to backup using gbak from Firebird 2.5
        backup_command = [
            gbak_path, '-b', fdb_file, backup_file,
            '-user', 'sysdba', '-password', 'masterkey'
        ]

        # Run the backup command
        result = subprocess.run(backup_command, check=True, capture_output=True, text=True)
        print(result.stdout)
        print(f"Backup successful: {backup_file}")

    except FileNotFoundError as fnf_error:
        print(f"File error: {fnf_error}")
    except subprocess.CalledProcessError as e:
        print(f"Backup failed: {e}")
        print(f"Error output: {e.stderr}")
    except Exception as ex:
        print(f"An error occurred: {ex}")


def restore_fdb(firebird_3_0_path, backup_file, new_fdb_file):
    try:
        # Ensure paths are correct
        if not os.path.isfile(backup_file):
            raise FileNotFoundError(f"Backup file not found: {backup_file}")

        gbak_path = os.path.join(firebird_3_0_path, 'gbak.exe')
        if not os.path.isfile(gbak_path):
            raise FileNotFoundError(f"'gbak' not found at: {gbak_path}")

        # Command to restore using gbak from Firebird 3.0 or higher
        restore_command = [
            gbak_path, '-c', backup_file, new_fdb_file,
            '-user', 'sysdba', '-password', 'masterkey'
        ]

        # Run the restore command
        result = subprocess.run(restore_command, check=True, capture_output=True, text=True)
        print(result.stdout)
        print(f"Restore successful: {new_fdb_file}")

    except FileNotFoundError as fnf_error:
        print(f"File error: {fnf_error}")
    except subprocess.CalledProcessError as e:
        print(f"Restore failed: {e}")
        print(f"Error output: {e.stderr}")
    except Exception as ex:
        print(f"An error occurred: {ex}")


if __name__ == "__main__":
    firebird_2_5_path = r'C:\Program Files (x86)\Firebird\Firebird_2_5\bin'
    firebird_3_0_path = r'C:\Program Files\Firebird\Firebird_3_0\bin'

    fdb_file = input("Enter the path of your old Firebird (.fdb) file: ")
    backup_file = fdb_file.replace('.fdb', '.fbk')  # Creating a backup file
    new_fdb_file = fdb_file.replace('.fdb', '_upgraded.fdb')  # New upgraded database file

    backup_fdb(firebird_2_5_path, fdb_file, backup_file)

    restore_fdb(firebird_3_0_path, backup_file, new_fdb_file)
