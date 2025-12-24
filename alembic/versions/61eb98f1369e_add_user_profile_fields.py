"""add_user_profile_fields

Revision ID: 61eb98f1369e
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '61eb98f1369e'
down_revision: Union[str, None] = 'c161be12178e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create enum type for user role
    op.execute("CREATE TYPE userrole AS ENUM ('user', 'admin')")
    
    # Add new columns
    op.add_column('users', sa.Column('username', sa.String(length=50), nullable=True))
    op.add_column('users', sa.Column('email', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('role', postgresql.ENUM('user', 'admin', name='userrole', create_type=False), nullable=True, server_default='user'))
    op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    
    # Set default values for existing rows
    op.execute("""
        UPDATE users 
        SET username = 'user_' || id::text,
            email = 'user_' || id::text || '@example.com',
            role = 'user'::userrole,
            created_at = NOW()
        WHERE username IS NULL OR email IS NULL
    """)
    
    # Make columns NOT NULL after setting defaults
    op.alter_column('users', 'username', nullable=False)
    op.alter_column('users', 'email', nullable=False)
    op.alter_column('users', 'role', nullable=False)
    op.alter_column('users', 'created_at', nullable=False)
    
    # Create indexes
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    
    # Drop columns
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'role')
    op.drop_column('users', 'email')
    op.drop_column('users', 'username')
    
    # Drop enum type
    op.execute('DROP TYPE IF EXISTS userrole')

