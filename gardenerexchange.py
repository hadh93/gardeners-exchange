import requests
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField, PasswordField, BooleanField, ValidationError, \
    IntegerField, FileField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import Email, Length, DataRequired, NumberRange, InputRequired, EqualTo, Regexp
import db
import time
import os

# UPLOAD_FOLDER = '/static/images/uploaded/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Super Secret Unguessable Key'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
UPLOAD_FOLDER = db_path = os.path.join(app.root_path, 'static\\images\\uploaded')
print(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class ImageUploadForm(FlaskForm):
    image = FileField('이미지')
    submit = SubmitField('상품 등록')


class itemForSaleForm(FlaskForm):
    itemname = StringField('상품명')
    itemprice = IntegerField('가격')
    itemunit = StringField('수량')
    itemsellername = StringField('판매자명')  ## many-to-many db required. link seller's userID
    image = FileField('이미지')
    ##itemdescription = TextAreaField('Item Description', validators=[Length(max=500),InputRequired]) <- Probably required as well
    submit = SubmitField('상품 추가')


class registerForm(FlaskForm):
    username = StringField('유저명', validators=[Length(min=5)])
    emailaddress = StringField('이메일주소', validators=[Email()])
    zipcode = StringField('우편번호', validators=[Length(min=5, max=5)])
    password = PasswordField('패스워드',
                             validators=[Length(min=8),
                                         Regexp(r'.*[A-Za-z]', message="알파벳 1자 이상을 포함해야 합니다."),
                                         Regexp(r'.*[0-9]', message="숫자 1자 이상을 포함해야 합니다."),
                                         Regexp(r'.*[!?.,;:]',
                                                message="특수문자(! ? . , ; : 등)를 1자 이상 포함해야 합니다.")])
    passwordconfirmation = PasswordField('Password Confirmation',
                                         validators=[EqualTo('password', message='비밀번호가 일치하지 않습니다.')])
    submit = SubmitField('등록')


class loginForm(FlaskForm):
    emailaddress = StringField('이메일주소', validators=[Email()])
    password = PasswordField('패스워드')
    submit = SubmitField('로그인')


class searchForm(FlaskForm):
    keyword = StringField('키워드')
    submit = SubmitField('검색')


@app.before_request
def before():
    db.open_db_connection()
    session.permanent = False
    # deletes search keyword values after closing browser


@app.teardown_request
def after(exception):
    db.close_db_connection(exception)


@app.route('/')
def init_sample_session():

    example_user = db.get_user_info("drwhite")
    session['search-feed'] = None
    session['user'] = example_user['username']
    session['remember'] = example_user['username']
    session['email'] = example_user['email']
    session['location'] = example_user['zipcode']
    session['address'] = example_user['address_id']
    current_user = session.get('remember')

    # Set sample session data to work with session stuff
    example_user = db.get_user_info("drwhite")
    print(example_user)
    return render_template('index.html', current_user=current_user)


def init_feed(session):
    if session.get('search-feed'):
        origin_items = db.get_feed_search(session.get('search-feed'))
    else:
        origin_items = db.get_feed()
    return origin_items


# returns a sorted page with a feed of listings for the user to browse
@app.route('/item_feed', methods=['GET', 'POST'])
def item_feed():
    origin_items = init_feed(session)
    current_user = session.get('remember')
    sorted_items, item_photos = sort_items(session['location'], origin_items)
    search_form = searchForm(keyword=session.get('search-feed'))

    if search_form.validate_on_submit():
        session['search-feed'] = search_form.keyword.data
        return redirect(url_for('item_feed'))

    return render_template('home.html', items=sorted_items, item_photos=item_photos, search_form=search_form,
                           current_user=current_user)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# uses the Google maps API to determine the distance between two zipcodes
def parse_JSON_distance(from_location, to_location):
    #
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='+str(from_location)+'&destinations='+str(to_location)+'&key=AIzaSyADNijeSubOSzUfwwm8hM0GK1wqYL9Fv8s'
    resp = requests.get(url)
    data = resp.json()
    splitedDistanceList = data["rows"][0]["elements"][0]["distance"]["text"].split(" ")
    return splitedDistanceList[0]


def get_listings_pics(sorted_items):
    listingsPhotos = []
    for listing in sorted_items:
        # listingsPhotos.append(db.get_listing_pics(db.get_item_id(listing['name'], listing['seller_name'])))
        listingsPhotos.append(db.get_listing_pics(listing['id']))
    return listingsPhotos


# sorts items based on the customer's zipcode
def sort_items(customer_location, origin_items):
    for item in origin_items:
        item['zipcode'] = parse_JSON_distance(item['zipcode'], customer_location)

    sorted_items = sorted(origin_items, key=lambda x: float(x['zipcode']))

    listings_photos = get_listings_pics(sorted_items)

    return sorted_items, listings_photos


def update_profile_pic(request, user):
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        photo_id = db.init_photo()
        db.change_user_photo(photo_id, session["user"])
        file.save("static/images/uploaded/" + str(photo_id) + ".jpg")
        return redirect(("/profile/" + user))


@app.route('/profile/<user>', methods=['GET', 'POST'])
def profile(user):
    current_user = session.get('remember')
    session['search-feed'] = None
    if request.method == 'POST':
        update_profile_pic(request, user)

    origin_items, listingPhotos = db.get_user_listings(user)
    sorted_items = sort_items(session['location'], origin_items)

    return render_template('profile.html', items = sorted_items[0],
                           image = "/static/images/uploaded/" + str(db.get_profile_pic(user)[0]) + ".jpg",
                           item_photos=listingPhotos, current_user=current_user)


@app.route('/register', methods=['GET', 'POST'])
def register():
    session['search-feed'] = None
    register_form = registerForm()

    if register_form.validate_on_submit():
        result = db.create_user(register_form.username.data, register_form.emailaddress.data,
                                register_form.zipcode.data, register_form.password.data)

        if result == 1:
            flash('Registration Successful!', 'success')
            return redirect(url_for('register_confirmation'))
        else:
            flash('Oops! Something went wrong', 'failure')

    return render_template('register.html', register_form=register_form)


@app.route('/register_confirmation')
def register_confirmation():
    return render_template('confirmation.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    session['search-feed'] = None
    login_form = loginForm()

    if login_form.validate_on_submit():

        result = db.login(login_form.emailaddress.data, login_form.password.data)
        if result != None:
            session['remember'] = db.get_userinfo(result[0])
            flash('로그인 성공!', 'success')
            return redirect(url_for('item_feed'))
        else:
            flash('무언가 잘못되었습니다..', 'failure')

    return render_template('login.html', login_form=login_form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['remember'] = None
    return redirect(url_for('item_feed'))


@app.route('/itemForSale', methods=['GET', 'POST'])
def itemForSale():
    session['search-feed'] = None
    current_user = session['remember']
    item_form = itemForSaleForm()

    if request.method == "POST":
        if 'image' not in request.files:
            flash('No image selected')

        else:
            file = request.files['image']

            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)

            if file and allowed_file(file.filename):
                result = db.create_item(item_form.itemname.data, item_form.itemprice.data, item_form.itemunit.data, current_user)
                image_id = db.init_photo()
                item_id = db.get_most_recent_user_item(current_user)[0]
                print("Image ID:" , image_id, "Item ID:", item_id)
                db.create_item_photo(image_id, item_id)

                name = str(image_id) + ".jpg"
                f = os.path.join(app.config['UPLOAD_FOLDER'], name)
                print(f)
                file.save(f)

                if result == 1:
                    flash('The item was successfully created!', 'success')
                    return redirect(url_for('item_feed'))
                else:
                    flash('Oops! Something went wrong', 'failure')

    return render_template('itemForSale.html',
                           item_form=item_form, current_user=current_user)


@app.route('/messaging')
def messaging():
    session['search-feed'] = None
    current_user = session.get('remember')
    return render_template('messaging.html', current_user=current_user)


@app.route('/transaction/<id>')
def transaction(id):
    current_user = session.get('remember')
    return render_template('transaction.html', buy_item_info = db.purchase_item(id), current_user=current_user)

if __name__ == '__main__':
    app.run()
