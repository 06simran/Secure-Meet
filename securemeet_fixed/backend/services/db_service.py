"""
Database Service — SQLAlchemy + Azure MySQL
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def init_db(app):
    """Initialise SQLAlchemy and create all tables."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("[DB] Tables created ✓")


# ─────────────────────────────────────────────────────────────────
#  Models
# ─────────────────────────────────────────────────────────────────

class User(db.Model):
    __tablename__ = "users"

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username   = db.Column(db.String(80),  nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(255), nullable=False)
    role       = db.Column(db.String(20),  default="user")   # 'admin' | 'user'
    violations = db.Column(db.Integer,     default=0)
    flagged    = db.Column(db.Boolean,     default=False)
    created_at = db.Column(db.DateTime,    default=datetime.utcnow)

    meetings         = db.relationship("Meeting",        backref="host",   lazy=True)
    flagged_messages = db.relationship("FlaggedMessage", backref="author", lazy=True)

    def to_dict(self):
        return {
            "id":         self.id,
            "username":   self.username,
            "email":      self.email,
            "role":       self.role,
            "violations": self.violations,
            "flagged":    self.flagged,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Meeting(db.Model):
    __tablename__ = "meetings"

    id            = db.Column(db.Integer,     primary_key=True, autoincrement=True)
    title         = db.Column(db.String(200), nullable=False)
    code          = db.Column(db.String(20),  unique=True, nullable=False)
    host_id       = db.Column(db.Integer,     db.ForeignKey("users.id"), nullable=False)
    status        = db.Column(db.String(20),  default="active")
    message_count = db.Column(db.Integer,     default=0)
    created_at    = db.Column(db.DateTime,    default=datetime.utcnow)

    def to_dict(self):
        return {
            "_id":           self.id,
            "title":         self.title,
            "code":          self.code,
            "host_id":       self.host_id,
            "status":        self.status,
            "message_count": self.message_count,
            "created_at":    self.created_at.isoformat() if self.created_at else None,
        }


class FlaggedMessage(db.Model):
    __tablename__ = "flagged_messages"

    id         = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    user_id    = db.Column(db.Integer,  db.ForeignKey("users.id"), nullable=False)
    meeting_id = db.Column(db.Integer,  nullable=True)
    message    = db.Column(db.Text,     nullable=False)
    toxic      = db.Column(db.Boolean,  default=True)
    confidence = db.Column(db.Float,    default=0.0)
    labels     = db.Column(db.String(200), default="")
    action     = db.Column(db.String(50),  default="warning")
    model_used = db.Column(db.String(50),  default="rule-based")
    timestamp  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "_id":        self.id,
            "user_id":    self.user_id,
            "meeting_id": self.meeting_id,
            "message":    self.message,
            "toxic":      self.toxic,
            "confidence": self.confidence,
            "labels":     self.labels.split(",") if self.labels else [],
            "action":     self.action,
            "model":      self.model_used,
            "timestamp":  self.timestamp.isoformat() if self.timestamp else None,
        }
