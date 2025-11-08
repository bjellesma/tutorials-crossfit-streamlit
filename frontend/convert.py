#!/usr/bin/env python3
"""Convert CSV data to DuckDB database for improved performance.
This script converts the athletes.csv file to a DuckDB database file.
"""

import duckdb
import pandas as pd
import os


def convert_csv_to_duckdb(csv_path: str, db_path: str = 'athletes.duckdb'):
    """Convert CSV file to DuckDB database.

    Args:
        csv_path (str): Path to the CSV file
        db_path (str): Path for the output DuckDB database file

    """
    print(f'Converting {csv_path} to DuckDB database...')

    # Create DuckDB connection
    conn = duckdb.connect(db_path)

    try:
        # Read CSV with pandas to handle data types properly
        print('Reading CSV file...')
        df = pd.read_csv(csv_path)

        print(f'CSV loaded: {len(df)} rows, {len(df.columns)} columns')
        print(f'Columns: {list(df.columns)}')

        # Create table in DuckDB
        print('Creating table in DuckDB...')
        conn.execute("""
            CREATE TABLE athletes (
                athlete_id DOUBLE,
                name VARCHAR,
                region VARCHAR,
                team VARCHAR,
                affiliate VARCHAR,
                gender VARCHAR,
                age DOUBLE,
                height DOUBLE,
                weight DOUBLE,
                fran DOUBLE,
                helen DOUBLE,
                grace DOUBLE,
                filthy50 DOUBLE,
                fgonebad DOUBLE,
                run400 DOUBLE,
                run5k DOUBLE,
                candj DOUBLE,
                snatch DOUBLE,
                deadlift DOUBLE,
                backsq DOUBLE,
                pullups DOUBLE,
                eat VARCHAR,
                train VARCHAR,
                background VARCHAR,
                experience VARCHAR,
                schedule VARCHAR,
                howlong VARCHAR
            )
        """)

        # Insert data from pandas DataFrame
        print('Inserting data into DuckDB...')
        conn.execute('INSERT INTO athletes SELECT * FROM df')

        # Create some useful indexes for common queries
        print('Creating indexes...')
        conn.execute('CREATE INDEX idx_athlete_id ON athletes(athlete_id)')
        conn.execute('CREATE INDEX idx_gender ON athletes(gender)')
        conn.execute('CREATE INDEX idx_region ON athletes(region)')
        conn.execute('CREATE INDEX idx_affiliate ON athletes(affiliate)')

        # Get some basic statistics
        result = conn.execute('SELECT COUNT(*) as total_rows FROM athletes').fetchone()
        print(f'Successfully inserted {result[0]} rows into DuckDB database')

        # Show sample data
        sample = conn.execute('SELECT * FROM athletes LIMIT 5').fetchall()
        print('\nSample data:')
        for row in sample:
            print(f'  {row}')

    except Exception as e:
        print(f'Error during conversion: {e}')
        raise
    finally:
        conn.close()

    print(f'DuckDB database created successfully: {db_path}')
    return db_path


def verify_duckdb_database(db_path: str):
    """Verify the DuckDB database by running some test queries.

    Args:
        db_path (str): Path to the DuckDB database file

    """
    print(f'\nVerifying DuckDB database: {db_path}')

    conn = duckdb.connect(db_path)

    try:
        # Test basic queries
        queries = [
            ('Total rows', 'SELECT COUNT(*) FROM athletes'),
            ('Unique athletes', 'SELECT COUNT(DISTINCT athlete_id) FROM athletes'),
            ('Gender distribution', 'SELECT gender, COUNT(*) FROM athletes GROUP BY gender'),
            (
                'Top 5 regions',
                'SELECT region, COUNT(*) as count FROM athletes WHERE region IS NOT NULL GROUP BY region ORDER BY count DESC LIMIT 5',
            ),
            (
                'Sample athlete data',
                'SELECT name, gender, age, weight, deadlift FROM athletes WHERE name IS NOT NULL LIMIT 3',
            ),
        ]

        for description, query in queries:
            print(f'\n{description}:')
            result = conn.execute(query).fetchall()
            for row in result:
                print(f'  {row}')

    except Exception as e:
        print(f'Error verifying database: {e}')
        raise
    finally:
        conn.close()


def main():
    """Main function to convert CSV to DuckDB."""
    csv_path = 'temp/athletes.csv'
    db_path = 'athletes.duckdb'

    # Check if CSV file exists
    if not os.path.exists(csv_path):
        print(f'Error: CSV file not found at {csv_path}')
        print('Please ensure the athletes.csv file is in the temp/ directory')
        return

    # Convert CSV to DuckDB
    try:
        convert_csv_to_duckdb(csv_path, db_path)
        verify_duckdb_database(db_path)
        print('\n✅ Conversion completed successfully!')
        print(f'Database file: {db_path}')
        print(f'File size: {os.path.getsize(db_path) / (1024 * 1024):.2f} MB')

    except Exception as e:
        print(f'❌ Conversion failed: {e}')
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
