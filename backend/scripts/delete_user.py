"""
Delete a user by email from the database.
Usage: python backend/scripts/delete_user.py <email>
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import app, db, User, Subscription, ActivityLog  # noqa: E402


def delete_user(email: str):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"No user found with email: {email}")
            return

        uid = user.id
        # Delete activity logs first to avoid FK/NOT NULL issues
        logs_deleted = ActivityLog.query.filter_by(user_id=uid).delete()
        subs_deleted = Subscription.query.filter_by(user_id=uid).delete()
        db.session.delete(user)
        db.session.commit()
        print(
            f"Deleted user {email} (id={uid}), "
            f"{subs_deleted} subscriptions, {logs_deleted} activity logs"
        )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python backend/scripts/delete_user.py <email>")
        sys.exit(1)
    delete_user(sys.argv[1])

