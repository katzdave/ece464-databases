"""initial schema

Revision ID: 10ce2c8b9d7d
Revises:
Create Date: 2026-02-19 19:07:14.349385

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '10ce2c8b9d7d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

game_phase = postgresql.ENUM(
    'waiting', 'prompting', 'submitting', 'voting', 'results', 'finished',
    name='gamephase',
    create_type=False,
)


def upgrade() -> None:
    """Upgrade schema."""
    # Create the enum type first
    game_phase.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'users',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('supabase_id', sa.String(), nullable=False, unique=True),
        sa.Column('display_name', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        'rooms',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('code', sa.String(4), nullable=False, unique=True, index=True),
        sa.Column('phase', game_phase, nullable=False, server_default='waiting'),
        sa.Column('host_id', sa.UUID(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        'room_players',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('room_id', sa.UUID(), sa.ForeignKey('rooms.id'), nullable=False),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint('room_id', 'user_id'),
    )

    op.create_table(
        'prompts',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('room_id', sa.UUID(), sa.ForeignKey('rooms.id'), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        'submissions',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('prompt_id', sa.UUID(), sa.ForeignKey('prompts.id'), nullable=False),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        'votes',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('submission_id', sa.UUID(), sa.ForeignKey('submissions.id'), nullable=False),
        sa.Column('user_id', sa.UUID(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('votes')
    op.drop_table('submissions')
    op.drop_table('prompts')
    op.drop_table('room_players')
    op.drop_table('rooms')
    op.drop_table('users')
    game_phase.drop(op.get_bind(), checkfirst=True)
