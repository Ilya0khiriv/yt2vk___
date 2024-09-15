#!/usr/bin/env python

import sqlite3
import io
import sys


def get_schema_info(db_path):
    """Retrieve the schema information from the SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema_info = {}

    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        schema_info[table_name] = [col[1] for col in columns]

    conn.close()
    return schema_info


def main(argv=sys.argv):
    """Converts cookies stored in a sqlite3 database to the old Netscape cookies.txt format."""

    if len(argv) != 3:
        sys.stderr.write('Usage: {} <cookie_db_path> <output_file>\n'.format(argv[0]))
        sys.exit(2)

    cookie_file = argv[1]
    output_file = argv[2]

    schema_info = get_schema_info(cookie_file)

    # Print schema information for debugging
    for table, columns in schema_info.items():
        print(f"Table: {table}")
        print("Columns: ", columns)

    # Check if the expected table and columns are available
    if 'cookies' in schema_info:
        columns = schema_info['cookies']
        print(f"Columns in 'cookies' table: {columns}")  # Debug line

        # Check if the table contains columns we expect
        expected_columns = ['host_key', 'path', 'secure', 'expires_utc', 'name', 'value']
        column_indices = {col: columns.index(col) for col in expected_columns if col in columns}

        if len(column_indices) == len(expected_columns):
            conn = sqlite3.connect(cookie_file)
            cur = conn.cursor()
            query = 'SELECT {0} FROM cookies'.format(', '.join(expected_columns))
            cur.execute(query)

            with io.open(output_file, 'w', encoding='utf-8') as f:
                i = 0
                for row in cur.fetchall():
                    f.write("{0}\tTRUE\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(
                        row[column_indices['host_key']],
                        row[column_indices['path']],
                        str(bool(row[column_indices['secure']])).upper(),
                        row[column_indices['expires_utc']],
                        str(row[column_indices['name']]),
                        str(row[column_indices['value']])
                    ))
                    i += 1
                print(f"{i} rows written")

            conn.close()
        else:
            sys.stderr.write('Error: Unexpected columns in table "cookies".\n')
            sys.exit(1)
    else:
        sys.stderr.write('Error: Table "cookies" not found in database.\n')
        sys.exit(1)


if __name__ == '__main__':
    main()
