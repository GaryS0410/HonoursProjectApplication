from flask_login import current_user

from app.models import *

# Function used in order to delete a patient
def delete_patient(patient_id):
    if (current_user.is_therapist):
        patient = User.query.get(patient_id)
        associations = Association.query.filter_by(patient_id=patient_id).all()

        # Deletes the users emotion data
        for session in patient.session_data:
            EmotionData.query.filter_by(session_id=session.id).delete()

        # Deletes the users session data
        SessionData.query.filter_by(user_id=patient_id).delete()

        # Delete association between therapist and patient
        for association in associations:
            db.session.delete(association)

        # Delete the patient
        db.session.delete(patient)
        db.session.commit()

        return redirect(url_for('admin'))