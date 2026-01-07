from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from datetime import datetime

class TimestampMixin:
    """Tự động thêm created_at và updated_at"""
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

class SoftDeleteMixin:
    """Thêm deleted_at để xử lý xóa mềm"""
    deleted_at = Column(DateTime(timezone=True), nullable=True)