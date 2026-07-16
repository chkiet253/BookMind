"""create all tables

Revision ID: 001
Revises: 
Create Date: 2026-06-17
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:

    # ── users ──────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id",              UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("email",           sa.String(),  nullable=False),
        sa.Column("name",            sa.String(),  nullable=False),
        sa.Column("hashed_password", sa.String(),  nullable=False),
        sa.Column("avatar_url",      sa.String()),
        sa.Column("profile_vector",  JSONB,        server_default="{}"),
        sa.Column("psych_scores",    JSONB,        server_default="{}"),
        sa.Column("created_at",      sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at",      sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )

    # ── books ──────────────────────────────────────────────────────────
    op.create_table(
        "books",
        sa.Column("id",           UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("title",        sa.String(),  nullable=False),
        sa.Column("author",       sa.String(),  nullable=False),
        sa.Column("isbn",         sa.String(),  unique=True),
        sa.Column("publisher",    sa.String()),
        sa.Column("pages",        sa.Integer()),
        sa.Column("year",         sa.Integer()),
        sa.Column("language",     sa.String(),  server_default="vi"),
        sa.Column("genres",       ARRAY(sa.String()), server_default="{}"),
        sa.Column("cover_url",    sa.String()),
        sa.Column("avg_rating",   sa.Float()),
        sa.Column("review_count", sa.Integer(), server_default="0"),
        sa.Column("tiki_url",     sa.String()),
        sa.Column("fahasa_url",   sa.String()),
        sa.Column("goodreads_url",sa.String()),
        sa.Column("scraped_at",   sa.DateTime(timezone=True)),
        sa.Column("created_at",   sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_books_author",   "books", ["author"])
    op.create_index("ix_books_language", "books", ["language"])
    op.create_index("ix_books_genres",   "books", ["genres"],
                    postgresql_using="gin")

    # ── reviews ────────────────────────────────────────────────────────
    op.create_table(
        "reviews",
        sa.Column("id",              UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("book_id",         UUID(as_uuid=True), sa.ForeignKey("books.id"), nullable=False),
        sa.Column("source",          sa.String(), nullable=False),
        sa.Column("source_url",      sa.String()),
        sa.Column("reviewer_name",   sa.String()),
        sa.Column("content",         sa.Text(),   nullable=False),
        sa.Column("sentiment_score", sa.Float()),
        sa.Column("like_count",      sa.Integer(), server_default="0"),
        sa.Column("published_at",    sa.DateTime(timezone=True)),
        sa.Column("scraped_at",      sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_reviews_book_sentiment", "reviews", ["book_id", "sentiment_score"])
    op.create_index("ix_reviews_book_source",    "reviews", ["book_id", "source"])

    # ── quotes ─────────────────────────────────────────────────────────
    op.create_table(
        "quotes",
        sa.Column("id",         UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("book_id",    UUID(as_uuid=True), sa.ForeignKey("books.id"), nullable=False),
        sa.Column("content",    sa.Text(),  nullable=False),
        sa.Column("source_url", sa.String()),
        sa.Column("scraped_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_quotes_book_id", "quotes", ["book_id"])

    # ── search_sessions ────────────────────────────────────────────────
    op.create_table(
        "search_sessions",
        sa.Column("id",              UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id",         UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True),
        sa.Column("raw_query",       sa.Text(), nullable=False),
        sa.Column("parsed_intent",   JSONB),
        sa.Column("result_book_ids", ARRAY(UUID(as_uuid=True)), server_default="{}"),
        sa.Column("created_at",      sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_search_sessions_user_id",    "search_sessions", ["user_id"])
    op.create_index("ix_search_sessions_created_at", "search_sessions", ["created_at"])

    # ── user_interactions ──────────────────────────────────────────────
    op.create_table(
        "user_interactions",
        sa.Column("id",         UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id",    UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("book_id",    UUID(as_uuid=True), sa.ForeignKey("books.id"), nullable=False),
        sa.Column("action",     sa.String(), nullable=False),
        sa.Column("rating",     sa.Float()),
        sa.Column("metadata",   JSONB, server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_user_interactions_user_book",   "user_interactions", ["user_id", "book_id"])
    op.create_index("ix_user_interactions_action",      "user_interactions", ["action"])
    op.create_index("ix_user_interactions_created_at",  "user_interactions", ["created_at"])

    # ── research_chats ─────────────────────────────────────────────────
    op.create_table(
        "research_chats",
        sa.Column("id",         UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id",    UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("book_id",    UUID(as_uuid=True), sa.ForeignKey("books.id"), nullable=False),
        sa.Column("messages",   JSONB, nullable=False, server_default="[]"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_research_chats_user_book", "research_chats", ["user_id", "book_id"])

    # ── psych_test_results ─────────────────────────────────────────────
    op.create_table(
        "psych_test_results",
        sa.Column("id",         UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id",    UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("test_level", sa.String(), nullable=False),
        sa.Column("answers",    JSONB, nullable=False),
        sa.Column("scores",     JSONB, nullable=False),
        sa.Column("taken_at",   sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )
    op.create_index("ix_psych_test_results_user_id", "psych_test_results", ["user_id"])


def downgrade() -> None:
    op.drop_table("psych_test_results")
    op.drop_table("research_chats")
    op.drop_table("user_interactions")
    op.drop_table("search_sessions")
    op.drop_table("quotes")
    op.drop_table("reviews")
    op.drop_table("books")
    op.drop_table("users")