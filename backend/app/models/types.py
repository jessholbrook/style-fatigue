from sqlalchemy import JSON
from sqlalchemy.dialects.postgresql import JSONB

# JSONB on PostgreSQL, plain JSON elsewhere (keeps SQLite tests viable)
JSONVariant = JSON().with_variant(JSONB(), "postgresql")
