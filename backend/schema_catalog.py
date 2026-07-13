def extract_schema():
    from database import get_connection, return_connection

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='public'
        AND table_type='BASE TABLE';
        """)

        tables = [t[0] for t in cur.fetchall()]
        schema = {}

        for table in tables:
            cur.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name=%s
            ORDER BY ordinal_position;
            """, (table,))

            columns = [
                {
                    "column": col[0],
                    "type": col[1],
                    "primary_key": False,
                    "references": None,
                }
                for col in cur.fetchall()
            ]

            cur.execute("""
            SELECT kcu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            WHERE tc.constraint_type = 'PRIMARY KEY'
            AND tc.table_name = %s;
            """, (table,))

            primary_keys = {row[0] for row in cur.fetchall()}

            cur.execute("""
            SELECT
                kcu.column_name,
                ccu.table_name,
                ccu.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage ccu
            ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
            AND tc.table_name = %s;
            """, (table,))

            foreign_keys = {
                row[0]: {"table": row[1], "column": row[2]}
                for row in cur.fetchall()
            }

            for column in columns:
                if column["column"] in primary_keys:
                    column["primary_key"] = True
                if column["column"] in foreign_keys:
                    column["references"] = foreign_keys[column["column"]]

            schema[table] = columns

        return schema

    finally:
        cur.close()
        return_connection(conn)