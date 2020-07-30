from flask import g
import psycopg2
import psycopg2.extras
import random

# Database Utilities ########################################

data_source_name = 'host=faraday.cse.taylor.edu dbname=dthomas008 user=dthomas008 password=roduqedi'


def open_db_connection():
    g.connection = psycopg2.connect(data_source_name)
    g.cursor = g.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)


def close_db_connection(self):
    g.cursor.close()
    g.connection.close()

# currently grabs listing in the database, we will eventually slim it down depending on the user
def get_feed():
    """List sample data for home feed"""
    query = '''
        SELECT id, name, price_per_unit, unit, seller_name, email, zipcode, rating, city, state, address_id, other_address_details
            FROM gardeners.listings INNER JOIN gardeners.users ON gardeners.listings.seller_name = gardeners.users.username
            ORDER BY zipcode
        '''
    g.cursor.execute(query)
    return g.cursor.fetchall()


def get_feed_search(keyword):
    keyword = '%' + str(keyword) + '%'
    query = '''
            SELECT id, name, price_per_unit, unit, seller_name, email, zipcode, rating, city, state, address_id, other_address_details
            FROM gardeners.listings INNER JOIN gardeners.users ON gardeners.listings.seller_name = gardeners.users.username 
            WHERE LOWER(name) LIKE LOWER(%(keyword)s) OR LOWER(seller_name) LIKE LOWER(%(keyword)s) ORDER BY zipcode
            '''
    g.cursor.execute(query, {'keyword': keyword})
    return g.cursor.fetchall()

def get_user_info(user):
    query = '''
            SELECT *
            FROM gardeners.users
            WHERE username= %(uname)s
            '''
    g.cursor.execute(query, {'uname':user})
    return g.cursor.fetchone()

def get_user_item_photo(listingsInfo):
    listingsPhotos = []

    for listing in listingsInfo:
        listingsPhotos.append(get_listing_pics(listing['id']))

    return listingsPhotos


def get_user_listings(user):
    query = '''
            SELECT id, name, price_per_unit, unit, seller_name, email, zipcode, rating, city, state, address_id, other_address_details
            FROM gardeners.listings INNER JOIN gardeners.users on seller_name=username
            WHERE seller_name = %(seller_name)s
            '''
    g.cursor.execute(query, {'seller_name':user})

    listingsInfo = g.cursor.fetchall()

    listingsPhotos = get_user_item_photo(listingsInfo)

    return listingsInfo, listingsPhotos


def create_user(username, emailaddress, zipcode, password):
    rating=0
    query = '''
        INSERT INTO gardeners.users (username, email, pass, zipcode, rating)
        VALUES (%(username)s, %(email)s, %(pass)s, %(zipcode)s, %(rating)s)
    '''
    g.cursor.execute(query, {'username': username, 'email': emailaddress, 'zipcode': zipcode, 'pass': password, 'rating': rating})
    g.connection.commit()
    return g.cursor.rowcount

def login(emailaddress, password):
    """List sample data for profile page"""
    query = '''
            SELECT username
            FROM gardeners.users
            WHERE email = %(emailaddress)s  AND pass = %(password)s
            '''
    g.cursor.execute(query, {'emailaddress':emailaddress, 'password':password})
    return g.cursor.fetchone()

def get_userinfo(user):
    """List sample data for profile page"""
    query = '''
            SELECT username, email, pass, zipcode, rating
            FROM gardeners.users
            WHERE username = %(user)s
            '''
    g.cursor.execute(query, {'user':user})
    return g.cursor.fetchall()

def change_user_photo(photo_id, user):
    query = '''
        DELETE FROM gardeners.user_photo
        WHERE user_id = %(u_id)s
    '''
    g.cursor.execute(query, {'u_id': user})
    g.connection.commit()

    query = '''
        INSERT INTO gardeners.user_photo (photo_id, user_id)
        VALUES (%(pic_id)s, %(u_id)s)
    '''
    print(photo_id)
    g.cursor.execute(query, {'pic_id': photo_id[0], 'u_id': user})
    g.connection.commit()
    return g.cursor.rowcount


def create_item_photo(photo_id, listing_id):
    query = '''
        INSERT INTO gardeners.listing_photo (photo_id, listing_id)
        VALUES (%(pic_id)s, %(l_id)s)
    '''
    g.cursor.execute(query, {'pic_id': photo_id, 'l_id': listing_id})
    g.connection.commit()
    return g.cursor.rowcount


def create_item(name, price_per_unit, unit, seller_name):
    query = '''
        INSERT INTO gardeners.listings (id, name, price_per_unit, unit, seller_name)
        VALUES (DEFAULT, %(name)s, %(price_per_unit)s, %(unit)s, %(seller_name)s)
    '''
    g.cursor.execute(query, {'name': name, 'price_per_unit': price_per_unit, 'unit': unit, 'seller_name': seller_name})
    g.connection.commit()
    return g.cursor.rowcount


def get_most_recent_user_item(user):
    query = '''
            SELECT id
            FROM gardeners.listings
            WHERE seller_name = %(name_of_seller)s
            ORDER BY id DESC
            '''
    g.cursor.execute(query, {'name_of_seller': user})
    return g.cursor.fetchone()


def get_item_id(item, seller_name):
    query = '''
            SELECT id
            FROM gardeners.listings
            WHERE name = %(item_name)s and seller_name = %(name_of_seller)s
            '''
    g.cursor.execute(query, {'item_name': item, 'name_of_seller': seller_name})
    return g.cursor.fetchone()


def init_photo():
    randominteger=random.randint(20,20000)
    query = '''
                INSERT INTO gardeners.photos (id) VALUES (%(randominteger)s)
                '''
    g.cursor.execute(query, {'randominteger': randominteger})
    return randominteger


def get_profile_pic(user):
    """List sample data for profile page"""
    query = '''
            SELECT photo_id
            FROM gardeners.user_photo
            WHERE user_id = %(username)s
        '''
    g.cursor.execute(query, {'username':user})
    return g.cursor.fetchone()


def get_listing_pics(listingID):
    """List sample data for profile page"""
    query = '''
            SELECT photo_id
            FROM gardeners.listing_photo
            WHERE listing_id = %(listing)s
        '''
    #  Sometimes id is a list
    # try:
    #     g.cursor.execute(query, {'listing': str(listingID[0])})
    # except:
    #     g.cursor.execute(query, {'listing': str(listingID)})
    g.cursor.execute(query, {'listing': listingID})
    return g.cursor.fetchone()

#grabs the info for the item when ready to purhcase
def purchase_item(id):
    query = '''
            SELECT *
            FROM gardeners.listings INNER JOIN gardeners.users on seller_name=username
            WHERE id =  %(id)s
            '''
    g.cursor.execute(query, {'id':id})
    return g.cursor.fetchall()
