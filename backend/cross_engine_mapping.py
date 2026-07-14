CROSS_ENGINE_MAPPING = """
Cross Database Relationship Mapping

Database: omnisight

customers.id
    ↔ marketing_db.marketing_metrics.campaign_id
    Relationship:
    Used as a conceptual customer-to-campaign reference.

customers.email
    ↔ marketing_db.campaigns.campaign_name
    Relationship:
    Example mapping for cross-engine reasoning.

orders.customer_id
    ↔ customers.id
    Relationship:
    Orders belong to customers.

orders.amount
    ↔ marketing_db.marketing_metrics.cost
    Relationship:
    Financial metrics can be compared.

orders.created_at
    ↔ marketing_db.campaigns.start_date
    Relationship:
    Time-based analysis between orders and campaigns.
"""