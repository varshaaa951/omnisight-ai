import pandas as pd

from database import get_connection, return_connection
from query_planner import analyze_question


def run_cross_database_query(question):

    plan = analyze_question(question)

    df_customers = None
    df_marketing = None

    # -------------------------
    # OmniSight
    # -------------------------

    if plan["use_omnisight"]:

        conn = get_connection("omnisight")

        try:

            df_customers = pd.read_sql(
                plan["customer_query"],
                conn
            )

        finally:

            return_connection(conn, "omnisight")

    # -------------------------
    # Marketing
    # -------------------------

    if plan["use_marketing"]:

        conn = get_connection("marketing_db")

        try:

            df_marketing = pd.read_sql(
                plan["marketing_query"],
                conn
            )

        finally:

            return_connection(conn, "marketing_db")

    # -------------------------
    # Return only OmniSight
    # -------------------------

    if (
        plan["use_omnisight"]
        and
        not plan["use_marketing"]
    ):

        return df_customers

    # -------------------------
    # Return only Marketing
    # -------------------------

    if (
        plan["use_marketing"]
        and
        not plan["use_omnisight"]
    ):

        return df_marketing

    # -------------------------
    # Merge
    # -------------------------

    merged = df_customers.merge(

        df_marketing,

        left_on="id",

        right_on="campaign_id",

        how="outer"

    )

    merged = merged.astype(object)
    merged = merged.where(pd.notnull(merged), None)

    return merged