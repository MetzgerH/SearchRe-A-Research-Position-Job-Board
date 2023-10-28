from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import  DataRequired, Length, NumberRange
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms_sqlalchemy.fields import QuerySelectMultipleField

from app.Model.models import Major, ProgLang

#class PostForm(FlaskForm):
#    title = StringField('Title', validators=[DataRequired()])
#    happiness_level = SelectField('Happiness Level',choices = [(3, 'I can\'t stop smiling'), (2, 'Really happy'), (1,'Happy')])
#    submit = SubmitField('Post')



#Form for creating an opening
class OpeningForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(),Length(min=0, max=100)])
    description = TextAreaField('Description', validators=[DataRequired(),Length(min=0, max=800)])
    start = DateField('Start Date (MM-DD-YYYY)', format="%m-%d-%Y")
    end = DateField('End Date (MM-DD-YYYY)', format="%m-%d-%Y")
    time_commitment = IntegerField('Time Commitment (in hours per week)', validators=[DataRequired(),NumberRange(min=0, max=80)])
    majors = QuerySelectMultipleField( 'Relevant Field(s)', query_factory= lambda: Major.query.all() , get_label= lambda x: x.name, 
        widget=ListWidget(prefix_label=False), option_widget=CheckboxInput() )
    languages = QuerySelectMultipleField( 'Relevant Programming Language(s)', query_factory= lambda: ProgLang.query.all() , get_label= lambda x: x.name, 
        widget=ListWidget(prefix_label=False), option_widget=CheckboxInput() )
    create = SubmitField('Create')
    
