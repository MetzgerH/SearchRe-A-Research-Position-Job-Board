from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import  DataRequired, Length, NumberRange, Email
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms_sqlalchemy.fields import QuerySelectMultipleField

from app.Model.models import Major, ProgLang

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
    
class ApplicationForm(FlaskForm):
    interest = TextAreaField('Interest Statement', validators=[DataRequired(),Length(min=0, max=500)])
    ref_name = TextAreaField('Reference Name', validators=[Length(min=0,max=100)])
    ref_email = StringField('Reference E-Mail', validators=[Email(),Length(min=0,max=500)])
    apply = SubmitField('Submit Application')

#Form for searching
class FilterForm(FlaskForm):
    title = TextAreaField('Title Keywords', validators=[Length(min=0, max=100)])
    description = TextAreaField('Description Keywords', validators=[Length(min=0, max=100)])
    titleOrDesc = TextAreaField('Title or Description', validators=[Length(min=0, max=100)])
    prof = TextAreaField('Professor Name', validators=[Length(min=0, max=100)])
    major = QuerySelectMultipleField( 'Expected Majors', query_factory= lambda: Major.query.all() , get_label= lambda x: x.name, 
        widget=ListWidget(prefix_label=False), option_widget=CheckboxInput() )
    languages = QuerySelectMultipleField( 'Expected Programming Languages', query_factory= lambda: ProgLang.query.all() , get_label= lambda x: x.name, 
        widget=ListWidget(prefix_label=False), option_widget=CheckboxInput() )
    search = SubmitField('Search')