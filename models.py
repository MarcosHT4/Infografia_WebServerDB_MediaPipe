from sqlalchemy import Column, Integer, JSON
from database import Base

class PoseLandmark(Base):
    __tablename__ = "pose_landmarks"
    id = Column(Integer, primary_key=True, index=True)
    landmarks = Column(JSON)