import re


# Dangerous SQL keywords
BLOCKED_KEYWORDS = [
    "DROP",
    "DELETE",
    "TRUNCATE",
    "ALTER",
    "UPDATE",
    "INSERT",
    "CREATE",
    "GRANT",
    "REVOKE"
]


def validate_sql(sql: str):

    if sql is None:
        return False, "No SQL was generated."

    sql = sql.strip()

    if sql == "":
        return False, "Empty SQL generated."

    upper_sql = sql.upper()

    # -------------------------
    # Dangerous Keywords
    # -------------------------

    for keyword in BLOCKED_KEYWORDS:

        if re.search(rf"\b{keyword}\b", upper_sql):

            return (
                False,
                f"Blocked dangerous SQL command: {keyword}"
            )

    # -------------------------
    # Only SELECT allowed
    # -------------------------

    if not upper_sql.startswith("SELECT"):

        return (
            False,
            "Only SELECT statements are allowed."
        )

    # -------------------------
    # Prevent multiple statements
    # -------------------------

    statements = sql.split(";")

    statements = [
        s.strip()
        for s in statements
        if s.strip()
    ]

    if len(statements) > 1:

        return (
            False,
            "Multiple SQL statements are not allowed."
        )

    return True, "SQL validated successfully."