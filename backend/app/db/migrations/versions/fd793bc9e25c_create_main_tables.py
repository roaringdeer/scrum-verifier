"""create_main_tables
Revision ID: fd793bc9e25c
Revises: 
Create Date: 2020-11-15 13:27:54.523623
"""
from alembic import op
import sqlalchemy as sa
from typing import Tuple

# revision identifiers, used by Alembic
revision = 'fd793bc9e25c'
down_revision = None
branch_labels = None
depends_on = None

def create_updated_at_trigger() -> None:
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS
        $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)

# def create_calculate_project_progress_trigger() -> None:
#     op.execute('''
#         CREATE OR REPLACE FUNCTION calculate_project_progress() 
#         RETURNS trigger AS $calculate_project_progress$
#         BEGIN
#             UPDATE projects 
#                 SET progress = (SELECT SUM(points)
#                                 FROM user_points
#                                 WHERE user_id = NEW.user_id)
#                 WHERE user_id = NEW.user_id;

#             RETURN NEW;
#         END;
#         $calculate_total_points$ LANGUAGE plpgsql;
#     ''')

def timestamps() -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            'created_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False
        ),
        sa.Column(
            'updated_at',
            sa.TIMESTAMP(timezone=True),
            server_default=sa.func.now(),
            nullable=False
        )
    )

def create_tasks_table() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Text, nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('cost', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=True),
        sa.Column('project_id', sa.Integer, sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('status', sa.Text, nullable=False, server_default='backlog'),
        sa.Column('date_todo', sa.DateTime(timezone=True), nullable=True),
        sa.Column('date_done', sa.DateTime(timezone=True), nullable=True),
        sa.Column('dependent_on', sa.types.ARRAY(sa.Integer), nullable=False),
        *timestamps()
    )
    op.execute(
        """
        CREATE TRIGGER update_tasks_modtime
            BEFORE UPDATE
            ON tasks
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )

def create_events_table() -> None:
    op.create_table(
        'events',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('project_id', sa.Integer, sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('event_type', sa.Text, nullable=False, server_default='other'),
        sa.Column('start_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('all_day', sa.Boolean, nullable=False, server_default='f'),
        *timestamps()
    )
    op.execute(
        """
        CREATE TRIGGER update_events_modtime
            BEFORE UPDATE
            ON events
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )

def create_sprints_table() -> None:
    op.create_table(
        'sprints',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('number', sa.Text, nullable=False),
        sa.Column('project_id', sa.Integer, sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('date_start', sa.DateTime(timezone=True), nullable=False),
        sa.Column('date_end', sa.DateTime(timezone=True), nullable=False),
        *timestamps()
    )
    op.execute(
        """
        CREATE TRIGGER update_sprint_modtime
            BEFORE UPDATE
            ON sprints
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )

def create_projects_table() -> None:
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Text, nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('is_archived', sa.Boolean, nullable=False, server_default='f'),
        sa.Column('team_id', sa.Integer, sa.ForeignKey('teams.id', ondelete='CASCADE')),
        sa.Column('sprint_interval', sa.Integer, nullable=False), # weeks
        *timestamps()
    )
    op.execute(
        """
        CREATE TRIGGER update_projects_modtime
            BEFORE UPDATE
            ON projects
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )

def create_teams_table() -> None:
    op.create_table(
        'teams',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.Text),
        sa.Column('description', sa.Text),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE')),
        *timestamps()
    )
    op.execute(
        """
        CREATE TRIGGER update_teams_modtime
            BEFORE UPDATE
            ON teams
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )

def create_members_table() -> None:
    op.create_table(
        'members',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('team_id', sa.Integer, sa.ForeignKey('teams.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('role', sa.Text, nullable=False, server_default='none', index=True),
        *timestamps(),
    )
    op.create_primary_key('pk_members', 'members', ['user_id', 'team_id'])
    op.execute(
        """
        CREATE TRIGGER update_members_modtime
            BEFORE UPDATE
            ON members
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )

def create_users_table() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.Text, unique=True, nullable=False, index=True),
        sa.Column('email_verified', sa.Boolean, nullable=False, server_default='f'),
        sa.Column('username', sa.Text, unique=True, nullable=False, index=True),
        sa.Column('password', sa.Text),
        sa.Column('salt', sa.Text, nullable=False),
        sa.Column('is_active', sa.Boolean, server_default='True'),
        sa.Column('is_superuser', sa.Boolean, nullable=False, server_default='f'),
        *timestamps()
    )
    op.execute(
        """
        CREATE TRIGGER update_users_modtime
            BEFORE UPDATE
            ON users
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )

def create_profiles_table() -> None:
    op.create_table(
        'profiles',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('full_name', sa.Text, nullable=True),
        sa.Column('phone_number', sa.Text, nullable=True),
        sa.Column('bio', sa.Text, nullable=True, server_default=''),
        sa.Column('image', sa.Text, nullable=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE')),
        *timestamps()
    )
    op.execute(
        """
        CREATE TRIGGER update_profiles_modtime
            BEFORE UPDATE
            ON profiles
            FOR EACH ROW
        EXECUTE PROCEDURE update_updated_at_column();
        """
    )

def upgrade() -> None:
    create_updated_at_trigger()
    create_users_table()
    create_teams_table()
    create_members_table()
    create_projects_table()
    create_sprints_table()
    create_tasks_table()
    create_profiles_table()
    create_events_table()
    

def downgrade() -> None:
    op.drop_table('events')
    op.drop_table('profiles')
    op.drop_table('tasks')
    op.drop_table('sprints')
    op.drop_table('projects')
    op.drop_table('members')
    op.drop_table('teams')
    op.drop_table('users')
    op.execute('DROP FUNCTION update_updated_at_column')
