from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    userrole_enum = postgresql.ENUM("user", "admin", name="userrole", create_type=True)
    userrole_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("first_name", sa.String(length=30), nullable=False),
        sa.Column("last_name", sa.String(length=30), nullable=False),
        sa.Column(
            "role",
            postgresql.ENUM("user", "admin", name="userrole", create_type=False),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)

    op.create_table(
        "passports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("passport_number", sa.Integer(), nullable=False),
        sa.Column("city", sa.String(length=30), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("passport_number"),
        sa.UniqueConstraint("user_id"),
    )
    op.create_index(op.f("ix_passports_id"), "passports", ["id"], unique=False)
    op.create_index(
        op.f("ix_passports_passport_number"),
        "passports",
        ["passport_number"],
        unique=True,
    )
    op.create_index(op.f("ix_passports_user_id"), "passports", ["user_id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_passports_user_id"), table_name="passports")
    op.drop_index(op.f("ix_passports_passport_number"), table_name="passports")
    op.drop_index(op.f("ix_passports_id"), table_name="passports")
    op.drop_table("passports")

    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")

    userrole_enum = postgresql.ENUM("user", "admin", name="userrole")
    userrole_enum.drop(op.get_bind(), checkfirst=True)
