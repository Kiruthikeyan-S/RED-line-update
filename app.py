from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import os
import math
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_fallback_key_red_line_2026')

# Default DB for users
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///default.db'

# Additional DB binds
app.config['SQLALCHEMY_BINDS'] = {
    'blood_donations': 'sqlite:///blood_donations.db',
    'blood_requests': 'sqlite:///blood_requests.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

### MODELS ###

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='client')  # 'admin' or 'client'

class BloodRequest(db.Model):
    __bind_key__ = 'blood_requests'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    blood_type = db.Column(db.String(10), nullable=False)
    address = db.Column(db.Text, nullable=False)
    id_proof = db.Column(db.String(200), nullable=True)  # File path for uploaded ID proof

class BloodDonation(db.Model):
    __bind_key__ = 'blood_donations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    blood_type = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    medical_conditions = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

### ACCESS CONTROL DECORATORS ###

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        if session.get('role') != 'admin':
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

### HAVERSINE SHORTEST-DISTANCE ALGORITHM ###

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance (km) between two GPS coordinates.
    Uses the Haversine formula — the shortest path on a sphere."""
    R = 6371  # Earth's radius in kilometers
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

### ROUTES ###

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'client')

        # Only allow 'client' role from public signup for security
        if role not in ('client', 'admin'):
            role = 'client'

        if not username or not email or not password:
            error = "Please fill in all required fields."
            return render_template('signup.html', error=error)

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            error = "Username or Email is already registered."
            return render_template('signup.html', error=error)

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login_identifier = (request.form.get('login_identifier') or
                            request.form.get('username') or
                            request.form.get('email') or '').strip()
        password = request.form.get('password', '')

        if not login_identifier or not password:
            error = "Please enter both credentials and password."
            return render_template('login.html', error=error)

        user = User.query.filter(
            (User.email == login_identifier) | (User.username == login_identifier)
        ).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = getattr(user, 'role', 'client') or 'client'
            next_page = request.form.get('next') or request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            error = "Invalid email/username or password"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/link')
@login_required
def link():
    return render_template('link.html')

@app.route('/map')
@login_required
def map():
    return render_template('map.html')

# Route for Receiving Blood Requests (Contact Page) — with shortest-path sorting
@app.route('/contact', methods=['GET', 'POST'])
@login_required
def contact():
    if request.method == 'POST':
        # Get form data from the contact form
        name = request.form.get('fname', '').strip()
        gender = request.form.get('gender', 'Other')
        email = request.form.get('femail', '').strip()
        phone = request.form.get('fphone', '').strip()
        blood_type = (request.form.get('ftype') or '').strip().upper()
        address = request.form.get('fdetails', '').strip()

        # Get requester's real-time GPS coordinates
        req_lat_str = request.form.get('latitude', '').strip()
        req_lng_str = request.form.get('longitude', '').strip()
        req_lat = float(req_lat_str) if req_lat_str else None
        req_lng = float(req_lng_str) if req_lng_str else None

        # Handle file upload for ID proof securely
        upload_folder = os.path.join(app.root_path, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        file = request.files.get('id_proof')
        file_path = ''
        if file and file.filename:
            filename = secure_filename(file.filename)
            if filename:
                file_path = os.path.join('uploads', filename)
                file.save(os.path.join(app.root_path, file_path))

        # Save recipient request into the database
        new_request = BloodRequest(
            name=name,
            gender=gender,
            email=email,
            phone=phone,
            blood_type=blood_type,
            address=address,
            id_proof=file_path
        )
        db.session.add(new_request)
        db.session.commit()

        # Define blood type compatibility mapping
        compatibility = {
            "A+": ["A+", "A-", "O+", "O-"],
            "A-": ["A-", "O-"],
            "B+": ["B+", "B-", "O+", "O-"],
            "B-": ["B-", "O-"],
            "A1B+": ["AB+", "A1B+"],
            "AB+": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
            "AB-": ["A-", "B-", "AB-", "O-"],
            "O+": ["O+", "O-"],
            "O-": ["O-"]
        }
        donor_types = compatibility.get(blood_type, [blood_type])

        matching_donors = []

        # 1. Read donors.xlsx from the "donor" folder
        donors_file = os.path.join(app.root_path, 'donor', 'donors.xlsx')
        try:
            if os.path.exists(donors_file):
                df = pd.read_excel(donors_file)
                df.columns = df.columns.str.strip().str.lower()

                required_cols = {"blood group", "name", "phone number"}
                if required_cols.issubset(set(df.columns)):
                    matching_donors_df = df[df['blood group'].astype(str).str.upper().isin(donor_types)]
                    for _, row in matching_donors_df.iterrows():
                        donor_entry = {
                            'name': row['name'],
                            'phone': str(row.get('phone number', '')),
                            'blood_group': str(row['blood group']).upper(),
                            'latitude': float(row['latitude']) if 'latitude' in row and pd.notna(row.get('latitude')) else None,
                            'longitude': float(row['longitude']) if 'longitude' in row and pd.notna(row.get('longitude')) else None,
                            'distance_km': None
                        }
                        matching_donors.append(donor_entry)
        except Exception as e:
            print(f"Error reading donors file: {e}")

        # 2. Also include matching donors registered in the database
        try:
            db_donations = BloodDonation.query.filter(BloodDonation.blood_type.in_(donor_types)).all()
            for d in db_donations:
                matching_donors.append({
                    'name': d.name,
                    'phone': d.phone,
                    'blood_group': d.blood_type,
                    'latitude': d.latitude,
                    'longitude': d.longitude,
                    'distance_km': None
                })
        except Exception as e:
            print(f"Error querying db donors: {e}")

        # 3. SHORTEST-PATH SORTING: Calculate distance from requester to each donor
        #    using Haversine formula and sort nearest first
        if req_lat is not None and req_lng is not None:
            for donor in matching_donors:
                if donor.get('latitude') and donor.get('longitude'):
                    dist = haversine(req_lat, req_lng, donor['latitude'], donor['longitude'])
                    donor['distance_km'] = round(dist, 2)

            # Sort: donors WITH location come first (nearest first), then donors without location
            donors_with_loc = [d for d in matching_donors if d['distance_km'] is not None]
            donors_without_loc = [d for d in matching_donors if d['distance_km'] is None]
            donors_with_loc.sort(key=lambda x: x['distance_km'])
            matching_donors = donors_with_loc + donors_without_loc

        # Render matching donors page with the results
        return render_template("matching.html", donors=matching_donors, recipient=blood_type,
                               req_lat=req_lat, req_lng=req_lng)

    return render_template('contact.html')

# Route for Donating Blood (Donate Page) with Location Tracking
@app.route('/donate', methods=['GET', 'POST'])
@login_required
def donate():
    if request.method == 'POST':
        name = request.form.get('fname', '').strip()
        gender = request.form.get('gender', 'Other')
        age_str = request.form.get('fage', '18').strip()
        weight_str = request.form.get('fweight', '50').strip()
        email = request.form.get('femail', '').strip()
        phone = request.form.get('fphone', '').strip()
        blood_type = (request.form.get('ftype') or '').strip().upper()
        medical_conditions = request.form.get('fdetails', '').strip()

        try:
            age = int(age_str)
        except (ValueError, TypeError):
            age = 18

        try:
            weight = int(weight_str)
        except (ValueError, TypeError):
            weight = 50

        lat_str = request.form.get('latitude', '').strip()
        lng_str = request.form.get('longitude', '').strip()
        latitude = float(lat_str) if lat_str else None
        longitude = float(lng_str) if lng_str else None

        # Handle optional Doctor Certificate file upload
        upload_folder = os.path.join(app.root_path, 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file = request.files.get('id_proof')
        if file and file.filename:
            filename = secure_filename(file.filename)
            if filename:
                file.save(os.path.join(upload_folder, filename))

        # Save donation record
        new_donation = BloodDonation(
            name=name,
            gender=gender,
            email=email,
            phone=phone,
            blood_type=blood_type,
            age=age,
            weight=weight,
            medical_conditions=medical_conditions,
            latitude=latitude,
            longitude=longitude
        )
        db.session.add(new_donation)
        db.session.commit()

        # Load donor tracking dataset (CSV file) or user's real-time position
        tracking_file = os.path.join(app.root_path, 'donor', 'donor_tracking.csv')
        donor_lat = latitude
        donor_lng = longitude
        donor_name = name

        if not donor_lat or not donor_lng:
            try:
                if os.path.exists(tracking_file):
                    df = pd.read_csv(tracking_file)
                    df.columns = df.columns.str.strip().str.lower()
                    matching_df = df[df['blood_group'].astype(str).str.upper() == blood_type]

                    if not matching_df.empty:
                        donor_info = matching_df.iloc[0]
                        donor_lat = donor_info['latitude']
                        donor_lng = donor_info['longitude']
                        donor_name = donor_info['name']
            except Exception as e:
                print(f"Error reading donor tracking file: {e}")

        if donor_lat and donor_lng:
            return render_template('tracking.html', donor_lat=donor_lat, donor_lng=donor_lng, donor_name=donor_name)
        else:
            flash('Thank you for registering as a donor!', 'success')
            return redirect(url_for('index'))

    return render_template('donate.html')

@app.route('/api/donors_location')
@login_required
def donors_location():
    donations = BloodDonation.query.filter(BloodDonation.latitude.isnot(None), BloodDonation.longitude.isnot(None)).all()
    results = []
    for d in donations:
        results.append({
            'name': d.name,
            'blood_type': d.blood_type,
            'phone': d.phone,
            'latitude': d.latitude,
            'longitude': d.longitude
        })
    return jsonify(results)

@app.route('/api/track_donor/<int:donor_id>')
@login_required
def track_donor(donor_id):
    """Real-time donor location tracking API — returns live GPS coordinates for a specific donor."""
    donor = BloodDonation.query.get(donor_id)
    if not donor or not donor.latitude or not donor.longitude:
        return jsonify({'error': 'Donor location not available'}), 404
    return jsonify({
        'id': donor.id,
        'name': donor.name,
        'blood_type': donor.blood_type,
        'phone': donor.phone,
        'latitude': donor.latitude,
        'longitude': donor.longitude
    })

@app.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    user_donations = BloodDonation.query.filter_by(email=user.email).all() if user else []
    user_requests = BloodRequest.query.filter_by(email=user.email).all() if user else []
    return render_template('profile.html', user=user, donations=user_donations, requests=user_requests)

@app.route('/download_certificate')
@login_required
def download_certificate():
    from flask import send_from_directory
    downloads_dir = os.path.join(app.root_path, 'static', 'downloads')
    return send_from_directory(downloads_dir, 'Doctor_Medical_Certificate_Form.txt', as_attachment=True)

@app.route('/blood_donations')
@admin_required
def view_donations():
    donations = BloodDonation.query.all()
    return render_template('blood_donations.html', donations=donations)

@app.route('/blood_requests')
@admin_required
def view_requests():
    requests_rec = BloodRequest.query.all()
    return render_template('blood_requests.html', requests=requests_rec)

### STARTUP ###

def seed_admin():
    """Create default admin user if none exists."""
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin_user = User(
            username='admin',
            email='admin@redline.com',
            password=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Default admin user created: admin / admin123")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_admin()
    app.run(debug=True)
