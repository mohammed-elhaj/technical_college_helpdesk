from werkzeug.utils import secure_filename
import os
import plotly.express as px
import pandas as pd
from models import db, User, Request, Message
from forms import SignupForm, LoginForm, RequestForm

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('main.signup'))
        
        new_user = User(
            full_name=form.full_name.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('main.login'))
    
    return render_template('signup.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid email or password')
    
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        requests = Request.query.all()
        return render_template('admin_dashboard.html', requests=requests)
    else:
        requests = Request.query.filter_by(user_id=current_user.id).all()
        return render_template('user_dashboard.html', requests=requests)

@main.route('/request/new', methods=['GET', 'POST'])
@login_required
def new_request():
    if current_user.is_admin:
        return redirect(url_for('main.dashboard'))
    
    form = RequestForm()
    if form.validate_on_submit():
        image_path = None
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            form.image.data.save(filepath)
            image_path = filename
        
        new_request = Request(
            user_id=current_user.id,
            location_type=form.location_type.data,
            location_number=form.location_number.data,
            problem_type=form.problem_type.data,
            description=form.description.data,
            image_path=image_path
        )
        db.session.add(new_request)
        db.session.commit()
        
        return redirect(url_for('main.dashboard'))
    
    return render_template('add_request.html', form=form)

@main.route('/request/<int:request_id>/solve', methods=['POST'])
@login_required
def solve_request(request_id):
    if not current_user.is_admin:
        return redirect(url_for('main.dashboard'))
    
    request = Request.query.get_or_404(request_id)
    request.status = 'solved'
    db.session.commit()
    
    return redirect(url_for('main.dashboard'))

@main.route('/request/<int:request_id>/message', methods=['POST'])
@login_required
def add_message(request_id):
    request = Request.query.get_or_404(request_id)
    content = request.form.get('content')
    
    if content:
        message = Message(
            request_id=request_id,
            sender_id=current_user.id,
            content=content
        )
        db.session.add(message)
        db.session.commit()
    
    return redirect(url_for('main.dashboard'))

@main.route('/admin/stats')
@login_required
def admin_stats():
    if not current_user.is_admin:
        return redirect(url_for('main.dashboard'))
    
    # Create statistics for problem types
    problems_df = pd.DataFrame([
        {'problem': req.problem_type, 'count': 1}
        for req in Request.query.all()
    ])
    problems_df = problems_df.groupby('problem').sum().reset_index()
    
    fig = px.bar(problems_df, x='problem', y='count', title='Problem Types Distribution')
    graph_json = fig.to_json()
    
    return render_template('admin_dashboard.html', graph_json=graph_json)
