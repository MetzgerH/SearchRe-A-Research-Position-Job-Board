import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, DateField, IntegerField, DecimalField, BooleanField, TextAreaField
from wtforms.validators import  DataRequired, Length, Email, EqualTo, NumberRange, ValidationError, Optional
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms_sqlalchemy.fields import QuerySelectMultipleField

from app.Model.models import User, Major, ProgLang

# I took this class/method directly from https://stackoverflow.com/questions/27766417/how-to-implement-not-required-datefield-using-flask-wtf
class NullableDateField(DateField):
    """Native WTForms DateField throws error for empty dates.
    Let's fix this so that we could have DateField nullable."""
    def process_formdata(self, valuelist):
        if valuelist:
            date_str = ' '.join(valuelist).strip()
            if date_str == '':
                self.data = None
                return
            try:
                self.data = datetime.datetime.strptime(date_str, "%m-%d-%y").date()
            except ValueError:
                self.data = None
                raise ValueError(self.gettext('Not a valid date value'))

class StudentRegistration(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(),Length(min=0, max=60)])
    last_name = StringField('Last Name',validators=[DataRequired(),Length(min=0, max=60)])
    username = StringField('Username',validators=[DataRequired()])
    student_id = IntegerField('Student ID Number', validators=[DataRequired()])
    email = StringField('Contact E-Mail', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    majors = QuerySelectMultipleField( 'Major(s)', query_factory= lambda: Major.query.all() , get_label= lambda x: x.name, 
        widget=ListWidget(prefix_label=False), option_widget=CheckboxInput() )
    languages = QuerySelectMultipleField( 'Known Programming Language(s)', query_factory= lambda: ProgLang.query.all() , get_label= lambda x: x.name, 
        widget=ListWidget(prefix_label=False), option_widget=CheckboxInput() )
    phone = IntegerField('Phone Number (Optional)', validators=[NumberRange(min=0, max=9999999999999), Optional()])
    graduation_date = NullableDateField('Expected Graduation Date (Optional) in format MM-DD-YYYY')
    gpa = DecimalField('GPA (Optional)', validators=[NumberRange(min=0, max=4), Optional()])
    research_history = TextAreaField('Research History (Optional)',validators=[Length(min=0, max=500)])
    submit = SubmitField('Submit')
    isUpdateForm = False
    def validate_username(self,username):
        if self.isUpdateForm:
            if User.query.filter_by(username=username.data).count() > 1:
                raise ValidationError('The username already exists! Please use a different username.')
        else:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('The username already exists! Please use a different username.')

        
    def validate_email(self,email):
        if self.isUpdateForm:
            if User.query.filter_by(username=email.data).count() > 1:
                raise ValidationError('The username already exists! Please use a different username.')
        else:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('That email is already connected to an account! Please use a different email.')

class ProfRegistration(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(),Length(min=0, max=60)])
    last_name = StringField('Last Name',validators=[DataRequired(),Length(min=0, max=60)])
    username = StringField('Username',validators=[DataRequired()])
    email = StringField('Contact E-Mail', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    phone = IntegerField('Phone Number (Optional)', validators=[NumberRange(min=0, max=9999999999999), Optional()])
    submit = SubmitField('Submit')
    isUpdateForm = False

    def validate_username(self,username):
        if self.isUpdateForm:
            if User.query.filter_by(username=username.data).count() > 1:
                raise ValidationError('The username already exists! Please use a different username.')
        else:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('The username already exists! Please use a different username.')

        
    def validate_email(self,email):
        if self.isUpdateForm:
            if User.query.filter_by(username=email.data).count() > 1:
                raise ValidationError('The username already exists! Please use a different username.')
        else:
            user = User.query.filter_by(email=email.data).first()
            if user is not None:
                raise ValidationError('That email is already connected to an account! Please use a different email.')

#Form for logging in
class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')