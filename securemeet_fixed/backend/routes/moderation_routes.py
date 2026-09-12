"""
Moderation Routes — /api/moderation
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from services.db_service import db, FlaggedMessage, User, Meeting
from services.moderation_service import ModerationService

moderation_bp = Blueprint("moderation", __name__)
mod_service   = ModerationService()


@moderation_bp.route("/predict", methods=["POST"])
@jwt_required()
def predict():
    data       = request.get_json()
    user_id    = int(get_jwt_identity())
    message    = data.get("message", "").strip()
    meeting_id = data.get("meeting_id")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    result = mod_service.analyze(message)

    if result["toxic"]:
        log = FlaggedMessage(
            user_id    = user_id,
            meeting_id = int(meeting_id) if meeting_id else None,
            message    = message,
            toxic      = result["toxic"],
            confidence = result["confidence"],
            labels     = ",".join(result.get("labels", [])),
            action     = result["action"],
            model_used = result.get("model", "rule-based"),
        )
        db.session.add(log)

        # Increment user violations
        user = User.query.get(user_id)
        if user:
            user.violations += 1
            if user.violations >= 5:
                user.flagged = True

        # Increment meeting message count
        if meeting_id:
            meeting = Meeting.query.get(int(meeting_id))
            if meeting:
                meeting.message_count += 1

        db.session.commit()

    return jsonify(result)


@moderation_bp.route("/flagged", methods=["GET"])
@jwt_required()
def flagged_messages():
    meeting_id = request.args.get("meeting_id")
    query = FlaggedMessage.query
    if meeting_id:
        query = query.filter_by(meeting_id=int(meeting_id))

    messages = query.order_by(FlaggedMessage.timestamp.desc()).limit(100).all()
    return jsonify({
        "flagged_messages": [m.to_dict() for m in messages],
        "total": len(messages),
    })


@moderation_bp.route("/history", methods=["GET"])
@jwt_required()
def moderation_history():
    messages        = FlaggedMessage.query.order_by(FlaggedMessage.timestamp.desc()).limit(200).all()
    total           = len(messages)
    high_confidence = sum(1 for m in messages if m.confidence > 0.85)

    return jsonify({
        "history": [m.to_dict() for m in messages],
        "stats": {
            "total_flagged":    total,
            "high_confidence":  high_confidence,
        },
    })


@moderation_bp.route("/stats", methods=["GET"])
@jwt_required()
def stats():
    total_users    = User.query.count()
    flagged_users  = User.query.filter(User.violations > 0).count()
    total_flagged  = FlaggedMessage.query.count()
    total_meetings = Meeting.query.count()

    # Action breakdown
    actions = {}
    for action in ["allow", "warning", "mute", "ban", "filter"]:
        actions[action] = FlaggedMessage.query.filter_by(action=action).count()

    return jsonify({
        "total_users":            total_users,
        "flagged_users":          flagged_users,
        "total_flagged_messages": total_flagged,
        "total_meetings":         total_meetings,
        "actions_breakdown":      actions,
    })
