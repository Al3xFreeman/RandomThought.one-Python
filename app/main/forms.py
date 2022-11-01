from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, DataRequired, Length

class NewPostForm(FlaskForm):
    body = TextAreaField('New Random Thought', validators=[DataRequired(), Length(3, 1024)])
    submit = SubmitField('Send')
