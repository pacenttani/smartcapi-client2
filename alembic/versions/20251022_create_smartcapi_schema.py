"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""create smartcapi schema (users, respondents, interviews, audio_files, transcription_segments, answers, answer_segments)

Revision ID: 20251022_create_smartcapi_schema
Revises: 
Create Date: 2025-10-22 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20251022_create_smartcapi_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create enums
    interview_status = postgresql.ENUM('SUBMITTED','PENDING','PROCESSING','COMPLETED','FAILED', name='interview_status')
    interview_status.create(op.get_bind(), checkfirst=True)

    interview_mode = postgresql.ENUM('WITH_AI','WITHOUT_AI', name='interview_mode')
    interview_mode.create(op.get_bind(), checkfirst=True)

    education_level = postgresql.ENUM('NONE','SD','SMP','SMA','UNIVERSITY', name='education_level')
    education_level.create(op.get_bind(), checkfirst=True)

    user_role = postgresql.ENUM('ADMIN','ENUMERATOR','SUPERVISOR', name='user_role')
    user_role.create(op.get_bind(), checkfirst=True)

    answer_source = postgresql.ENUM('MANUAL','AI_GENERATED', name='answer_source')
    answer_source.create(op.get_bind(), checkfirst=True)

    # tables
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('username', sa.String(length=100), nullable=False, unique=True),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False, unique=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('role', user_role, nullable=False, server_default='ENUMERATOR'),
        sa.Column('voice_sample_path', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False)
    )

    op.create_table(
        'password_reset_tokens',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True),
        sa.Column('token', sa.String(length=255), nullable=False, unique=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False)
    )

    op.create_table(
        'respondents',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('full_name', sa.String(length=255), nullable=False),
        sa.Column('gender', sa.String(length=10), nullable=True),
        sa.Column('place_of_birth', sa.String(length=50), nullable=True),
        sa.Column('date_of_birth', sa.Date, nullable=True),
        sa.Column('age', sa.Integer, nullable=True),
        sa.Column('education_level', education_level, nullable=True),
        sa.Column('occupation', sa.String(length=100), nullable=True),
        sa.Column('hobby', sa.String(length=50), nullable=True),
        sa.Column('address', sa.Text, nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('email', sa.String(length=100), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False)
    )

    op.create_table(
        'interviews',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=True),
        sa.Column('respondent_id', sa.Integer, sa.ForeignKey('respondents.id'), nullable=True),
        sa.Column('interview_code', sa.String(length=50), nullable=False, unique=True),
        sa.Column('status', interview_status, nullable=False, server_default='PENDING'),
        sa.Column('mode', interview_mode, nullable=False),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration', sa.Integer, nullable=True),
        sa.Column('has_recording', sa.Boolean, nullable=False, server_default=sa.text('false')), 
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False)
    )

    op.create_table(
        'audio_files',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('interview_id', sa.Integer, sa.ForeignKey('interviews.id', ondelete='CASCADE'), nullable=False),
        sa.Column('file_path', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False)
    )

    op.create_table(
        'transcription_segments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('audio_file_id', sa.Integer, sa.ForeignKey('audio_files.id', ondelete='CASCADE'), nullable=False),
        sa.Column('segment_start', sa.Float, nullable=True),
        sa.Column('segment_end', sa.Float, nullable=True),
        sa.Column('speaker_label', sa.String(length=50), nullable=True),
        sa.Column('transcription_text', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False)
    )

    op.create_table(
        'answers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('interview_id', sa.Integer, sa.ForeignKey('interviews.id', ondelete='CASCADE'), nullable=False),
        sa.Column('question_text', sa.Text, nullable=False),
        sa.Column('answer_text', sa.Text, nullable=True),
        sa.Column('source', answer_source, nullable=False, server_default='MANUAL'),
        sa.Column('confidence_score', sa.Float, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False)
    )

    op.create_table(
        'answer_segments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('answer_id', sa.Integer, sa.ForeignKey('answers.id', ondelete='CASCADE'), nullable=False),
        sa.Column('segment_id', sa.Integer, sa.ForeignKey('transcription_segments.id', ondelete='CASCADE'), nullable=False),
        sa.UniqueConstraint('answer_id', 'segment_id', name='uq_answer_segment')
    )

def downgrade():
    op.drop_table('answer_segments')
    op.drop_table('answers')
    op.drop_table('transcription_segments')
    op.drop_table('audio_files')
    op.drop_table('interviews')
    op.drop_table('respondents')
    op.drop_table('password_reset_tokens')
    op.drop_table('users')

    answer_source = postgresql.ENUM('MANUAL','AI_GENERATED', name='answer_source')
    answer_source.drop(op.get_bind(), checkfirst=True)

    user_role = postgresql.ENUM('ADMIN','ENUMERATOR','SUPERVISOR', name='user_role')
    user_role.drop(op.get_bind(), checkfirst=True)

    education_level = postgresql.ENUM('NONE','SD','SMP','SMA','UNIVERSITY', name='education_level')
    education_level.drop(op.get_bind(), checkfirst=True)

    interview_mode = postgresql.ENUM('WITH_AI','WITHOUT_AI', name='interview_mode')
    interview_mode.drop(op.get_bind(), checkfirst=True)

    interview_status = postgresql.ENUM('SUBMITTED','PENDING','PROCESSING','COMPLETED','FAILED', name='interview_status')
    interview_status.drop(op.get_bind(), checkfirst=True)