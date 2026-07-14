def analyze_question(question: str):

    question = question.lower()

    plan = {
        "use_omnisight": False,
        "use_marketing": False,
        "customer_query": None,
        "marketing_query": None
    }

    # -------------------------
    # OmniSight Keywords
    # -------------------------

    if any(word in question for word in [
        "customer",
        "customers",
        "name",
        "email"
    ]):

        plan["use_omnisight"] = True

        plan["customer_query"] = """
        SELECT
            id,
            name,
            email
        FROM customers
        """

    # -------------------------
    # Marketing Keywords
    # -------------------------

    if any(word in question for word in [
        "campaign",
        "marketing",
        "click",
        "clicks",
        "ctr",
        "cost",
        "impression",
        "performance"
    ]):

        plan["use_marketing"] = True

        plan["marketing_query"] = """
        SELECT
            campaign_id,
            impressions,
            clicks,
            ctr,
            cost
        FROM marketing_metrics
        """

    return plan