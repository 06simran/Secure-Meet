"""
Meeting Routes — /api/meetings
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import random, string

from services.db_service import db, Meeting

meeting_bp = Blueprint("meetings", __name__)


def gen_code(length=8):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


@meeting_bp.route("/create", methods=["POST"])
@jwt_required()
def create_meeting():
    data    = request.get_json()
    host_id = int(get_jwt_identity())

    # Ensure unique code
    code = gen_code()
    while Meeting.query.filter_by(code=code).first():
        code = gen_code()

    meeting = Meeting(
        title=data.get("title", "Untitled Meeting"),
        code=code,
        host_id=host_id,
    )
    db.session.add(meeting)
    db.session.commit()

    return jsonify({"message": "Meeting created", "meeting": meeting.to_dict()}), 201


@meeting_bp.route("/join", methods=["POST"])
@jwt_required()
def join_meeting():
    data    = request.get_json()
    meeting = Meeting.query.filter_by(code=data.get("code", "").upper()).first()

    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404

    return jsonify({"message": "Joined", "meeting": meeting.to_dict()})


@meeting_bp.route("/", methods=["GET"])
@jwt_required()
def list_meetings():
    host_id  = int(get_jwt_identity())
    meetings = Meeting.query.filter_by(host_id=host_id).order_by(Meeting.created_at.desc()).all()
    return jsonify({"meetings": [m.to_dict() for m in meetings]})


@meeting_bp.route("/<int:meeting_id>", methods=["GET"])
@jwt_required()
def get_meeting(meeting_id):
    meeting = Meeting.query.get(meeting_id)
    if not meeting:
        return jsonify({"error": "Meeting not found"}), 404
    return jsonify({"meeting": meeting.to_dict()})


@meeting_bp.route("/<int:meeting_id>/end", methods=["POST"])
@jwt_required()
def end_meeting(meeting_id):
    meeting = Meeting.query.get(meeting_id)
    if not meeting:
        return jsonify({"error": "Not found"}), 404
    meeting.status = "ended"
    db.session.commit()
    return jsonify({"message": "Meeting ended", "meeting": meeting.to_dict()})
