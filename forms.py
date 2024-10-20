from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, TextAreaField, FileField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class SignupForm(FlaskForm):
    full_name = StringField('الاسم بالكامل', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('البريد الالكتروني', validators=[DataRequired(), Email()])
    password = PasswordField('كلمة المرور', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('تاكيد كلمة المرور', validators=[DataRequired(), EqualTo('password')])

class LoginForm(FlaskForm):
    email = StringField('البريد الالكتروني', validators=[DataRequired(), Email()])
    password = PasswordField('كلمة المرور', validators=[DataRequired()])

class RequestForm(FlaskForm):
    location_type = RadioField('حدد مكان المشكلة:', 
                             choices=[('مكتب', 'مكتب'), ('معمل', 'معمل'), ('قاعة', 'قاعة')],
                             validators=[DataRequired()])
    location_number = StringField('رقم القاعة او المكتب او المعمل:', validators=[DataRequired()])
    problem_type = SelectField('نوع المشكلة',
                             choices=[('جهاز مكتبي', 'جهاز مكتبي'), ('جهاز عرض', 'جهاز عرض'), ('طابعة', 'طابعة')],
                             validators=[DataRequired()])
    description = TextAreaField('وصف المشكلة:', validators=[DataRequired()])
    image = FileField('اضافة صورة (اختياري)')  
