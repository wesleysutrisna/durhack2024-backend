import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('durhack-ncl-firebase-adminsdk-1zaof-93d6a42eb9.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://durhack-ncl-default-rtdb.europe-west1.firebasedatabase.app/'
})


def add_item_of_the_day(id, item, date):
    ref = db.reference('py/')
    item_ref = ref.child('items_of_the_day')
    item_ref.update({
        id: {
            'item': item,
            'date': date
        }})


def add_user(id, items_found_today, total_items_found, score):
    ref = db.reference('py/')
    item_ref = ref.child('user')
    item_ref.update({
        id: {
            'items_found_today': items_found_today,
            'total_items_found': total_items_found,
            'score': score
        }})


def add_user_quest(id, userid, itemid, complete, location):
    ref = db.reference('py/')
    item_ref = ref.child('user_quest')
    item_ref.update({
        id: {
            'user_id': userid,
            'item_id': itemid,
            'complete': complete,
            'location': location
        }})


def reset_user_stats():
    # Reference to the 'user' node in the database
    ref = db.reference('py/user')

    # Retrieve all users
    users = ref.get()

    # Check if there are any users
    if users:
        for user_id in users:
            # Set items_found_today to 0 for each user
            ref.child(user_id).update({'items_found_today': 0})


def update_score(user_id, amount):
    # Reference to the specific user's data in the database
    user_ref = db.reference(f'py/user/{user_id}')

    # Retrieve the current score of the user
    user_data = user_ref.get()

    if user_data:
        # Current score (default to 0 if not set)
        current_score = user_data.get('score', 0)

        # Calculate new score
        new_score = current_score + amount

        # Update the user's score in the database
        user_ref.update({'score': new_score})


def update_items_found(user_id):
    # Reference to the specific user's data in the database
    user_ref = db.reference(f'py/user/{user_id}')

    # Retrieve the current score of the user
    user_data = user_ref.get()

    if user_data:
        # Current score (default to 0 if not set)
        items_found_today = user_data.get('items_found_today', 0) + 1
        total_items_found = user_data.get('total_items_found', 0) + 1

        user_ref.update({'items_found_today': items_found_today})
        user_ref.update({'total_items_found': total_items_found})