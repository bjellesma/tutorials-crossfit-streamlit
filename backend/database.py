import duckdb


def get_athletes():
    """get from database"""
    db_path = "athletes.duckdb"

    with duckdb.connect(db_path) as conn:
        query = "SELECT * FROM athletes LIMIT 1000"
        result = conn.execute(query=query)
        return {
            "athletes": result.fetchall(),
            "columns": [col[0] for col in result.description],
        }
