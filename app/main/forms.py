from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField
from wtforms.validators import DataRequired

class PHQ9Form(FlaskForm):
    question1 = RadioField('Little interest or pleasure in doing things?', choices=[('0', 'Not at all'), ('1', 'Several days'), ('2', 'More than half the days'), ('3', 'Nearly every day')], validators=[DataRequired()])
    question2 = RadioField('Feeling down, depressed, or hopeless?', choices=[('0', 'Not at all'), ('1', 'Several days'), ('2', 'More than half the days'), ('3', 'Nearly every day')], validators=[DataRequired()])
    question3 = RadioField('Trouble falling or staying asleep, or sleeping too much?', choices=[('0', 'Not at all'), ('1', 'Several days'), ('2', 'More than half the days'), ('3', 'Nearly every day')], validators=[DataRequired()])
    question4 = RadioField('Feeling tired or having little energy?', choices=[('0', 'Not at all'), ('1', 'Several days'), ('2', 'More than half the days'), ('3', 'Nearly every day')], validators=[DataRequired()])
    question5 = RadioField('Poor appetite or overeating?', choices=[('0', 'Not at all'), ('1', 'Several days'), ('2', 'More than half the days'), ('3', 'Nearly every day')], validators=[DataRequired()])
    question6 = RadioField('Feeling bad about yourself, or that you are a failure, or have let yourself or your family down?', choices=[('0', 'Not at all'), ('1', 'Several days'), ('2', 'More than half the days'), ('3', 'Nearly every day')], validators=[DataRequired()])
    question7 = RadioField('Trouble concentraing on things, such as reading the newspaper or watching television?', choices=[('0', 'Not at all'), ('1', 'Several days'), ('2', 'More than half the days'), ('3', 'Nearly every day')], validators=[DataRequired()])
    question8 = RadioField('Moving or speaking so slowly that other people could have noticed?', choices=[('0', 'Not at all'), ('1', 'Several days'), ('2', 'More than half the days'), ('3', 'Nearly every day')], validators=[DataRequired()])
    question9 = RadioField('Thoughts that you would be better off dead, or of hurting yourself?', choices=[('0', 'Not at all'), ('1', 'Several days'), ('2', 'More than half the days'), ('3', 'Nearly every day')], validators=[DataRequired()])
    submit = SubmitField('Submit')