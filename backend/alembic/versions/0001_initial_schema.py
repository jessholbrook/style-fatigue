"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-07-02
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import JSONB

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def _json():
    return sa.JSON().with_variant(JSONB(), "postgresql")


def upgrade():
    op.create_table(
        "participants",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("token", sa.String(64), nullable=False),
        sa.Column("condition", sa.String(20), nullable=True),
        sa.Column("shift_eligible_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("consent_given_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("metadata_json", _json(), nullable=True),
    )
    op.create_index("ix_participants_token", "participants", ["token"], unique=True)

    op.create_table(
        "sessions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("participant_id", sa.Uuid(), sa.ForeignKey("participants.id"), nullable=False),
        sa.Column("session_number", sa.Integer(), nullable=False),
        sa.Column("style_profile", sa.String(20), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_shift_session", sa.Boolean(), nullable=True),
    )

    op.create_table(
        "conversations",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("session_id", sa.Uuid(), sa.ForeignKey("sessions.id"), nullable=False),
        sa.Column("intent", sa.String(100), nullable=False),
        sa.Column("topic", sa.String(100), nullable=False),
        sa.Column("messages", _json(), nullable=True),
        sa.Column("turn_count", sa.Integer(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
    )

    op.create_table(
        "survey_responses",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("session_id", sa.Uuid(), sa.ForeignKey("sessions.id"), nullable=False),
        sa.Column("survey_type", sa.String(30), nullable=False),
        sa.Column("responses", _json(), nullable=True),
        sa.Column("noticeability_score", sa.Integer(), nullable=True),
        sa.Column("preference_score", sa.Integer(), nullable=True),
        sa.Column("free_text", sa.Text(), nullable=True),
        sa.Column("submitted_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "event_log",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("participant_id", sa.Uuid(), sa.ForeignKey("participants.id"), nullable=True),
        sa.Column("session_id", sa.Uuid(), sa.ForeignKey("sessions.id"), nullable=True),
        sa.Column("event_type", sa.String(50), nullable=False),
        sa.Column("payload", _json(), nullable=True),
        sa.Column("client_timestamp", sa.DateTime(timezone=True), nullable=True),
        sa.Column("server_timestamp", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_event_log_participant_id", "event_log", ["participant_id"])
    op.create_index("ix_event_log_session_id", "event_log", ["session_id"])
    op.create_index("ix_event_log_event_type", "event_log", ["event_type"])


def downgrade():
    op.drop_table("event_log")
    op.drop_table("survey_responses")
    op.drop_table("conversations")
    op.drop_table("sessions")
    op.drop_table("participants")
