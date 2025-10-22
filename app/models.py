from enum import Enum as PyEnum
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime, Date, Float, Text, Boolean,
    ForeignKey, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy.orm import relationship
from .db import Base
from sqlalchemy.sql import func

class InterviewStatus(PyEnum):
    SUBMITTED = "SUBMITTED"
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class InterviewMode(PyEnum):
    WITH_AI = "WITH_AI"
    WITHOUT_AI = "WITHOUT_AI"

class EducationLevel(PyEnum):
    NONE = "NONE"
    SD = "SD"
    SMP = "SMP"
    SMA = "SMA"
    UNIVERSITY = "UNIVERSITY"

class UserRole(PyEnum):
    ADMIN = "ADMIN"
    ENUMERATOR = "ENUMERATOR"
    SUPERVISOR = "SUPERVISOR"

class AnswerSource(PyEnum):
    MANUAL = "MANUAL"
    AI_GENERATED = "AI_GENERATED"

# --- Tables ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    phone = Column(String(20), nullable=True)
    role = Column(PGEnum(UserRole, name="user_role", create_type=False), nullable=False, server_default=UserRole.ENUMERATOR.value)
    voice_sample_path = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    interviews = relationship("Interview", back_populates="user", cascade="all, delete-orphan")
    password_reset_token = relationship("PasswordResetToken", uselist=False, back_populates="user", cascade="all, delete-orphan")

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    token = Column(String(255), unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="password_reset_token")

class Respondent(Base):
    __tablename__ = "respondents"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(255), nullable=False)
    gender = Column(String(10), nullable=True)
    place_of_birth = Column(String(50), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    age = Column(Integer, nullable=True)
    education_level = Column(PGEnum(EducationLevel, name="education_level", create_type=False), nullable=True)
    occupation = Column(String(100), nullable=True)
    hobby = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    interviews = relationship("Interview", back_populates="respondent", cascade="all, delete-orphan")

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    respondent_id = Column(Integer, ForeignKey("respondents.id"), nullable=True)
    interview_code = Column(String(50), nullable=False, unique=True, index=True)
    status = Column(PGEnum(InterviewStatus, name="interview_status", create_type=False), nullable=False, server_default=InterviewStatus.PENDING.value)
    mode = Column(PGEnum(InterviewMode, name="interview_mode", create_type=False), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    duration = Column(Integer, nullable=True)
    has_recording = Column(Boolean, nullable=False, server_default="false")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="interviews")
    respondent = relationship("Respondent", back_populates="interviews")
    audio_files = relationship("AudioFile", back_populates="interview", cascade="all, delete-orphan")
    answers = relationship("Answer", back_populates="interview", cascade="all, delete-orphan")

class AudioFile(Base):
    __tablename__ = "audio_files"

    id = Column(Integer, primary_key=True)
    interview_id = Column(Integer, ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    interview = relationship("Interview", back_populates="audio_files")
    segments = relationship("TranscriptionSegment", back_populates="audio_file", cascade="all, delete-orphan")

class TranscriptionSegment(Base):
    __tablename__ = "transcription_segments"

    id = Column(Integer, primary_key=True)
    audio_file_id = Column(Integer, ForeignKey("audio_files.id", ondelete="CASCADE"), nullable=False)
    segment_start = Column(Float, nullable=True)
    segment_end = Column(Float, nullable=True)
    speaker_label = Column(String(50), nullable=True)
    transcription_text = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    audio_file = relationship("AudioFile", back_populates="segments")
    answer_segments = relationship("AnswerSegment", back_populates="segment", cascade="all, delete-orphan")

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    interview_id = Column(Integer, ForeignKey("interviews.id", ondelete="CASCADE"), nullable=False)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text, nullable=True)
    source = Column(PGEnum(AnswerSource, name="answer_source", create_type=False), nullable=False, server_default=AnswerSource.MANUAL.value)
    confidence_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    interview = relationship("Interview", back_populates="answers")
    segments = relationship("AnswerSegment", back_populates="answer", cascade="all, delete-orphan")

class AnswerSegment(Base):
    __tablename__ = "answer_segments"

    id = Column(Integer, primary_key=True)
    answer_id = Column(Integer, ForeignKey("answers.id", ondelete="CASCADE"), nullable=False)
    segment_id = Column(Integer, ForeignKey("transcription_segments.id", ondelete="CASCADE"), nullable=False)

    answer = relationship("Answer", back_populates="segments")
    segment = relationship("TranscriptionSegment", back_populates="answer_segments")

    __table_args__ = (
        UniqueConstraint("answer_id", "segment_id", name="uq_answer_segment"),
    )