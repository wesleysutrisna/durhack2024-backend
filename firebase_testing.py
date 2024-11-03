import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate('durhack-ncl-firebase-adminsdk-1zaof-93d6a42eb9.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://durhack-ncl-default-rtdb.europe-west1.firebasedatabase.app/'
})


def add_item_of_the_day(id, quest_num, item, date):
    ref = db.reference('py/')
    item_ref = ref.child('items_of_the_day')
    item_ref.update({
        id: {
            'quest_num': quest_num,
            'item': item,
            'date': date
        }})


def add_user(id, display_name):
    ref = db.reference('py/')
    item_ref = ref.child('user')
    item_ref.update({
        id: {
            'display_name': display_name,
            'items_found_today': 0,
            'total_items_found': 0,
            'score': 0,
            'item1_found': False,
            'item2_found': False,
            'item3_found': False,
            'item1_location': 'not found',
            'item2_location': 'not found',
            'item3_location': 'not found'
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
            ref.child(user_id).update({
                'items_found_today': 0,
                'item1_found': False,
                'item2_found': False,
                'item3_found': False,
                'item1_location': 'not found',
                'item2_location': 'not found',
                'item3_location': 'not found'
            })


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


def update_items_found(user_id, items_found):
    # Reference to the specific user's data in the database
    user_ref = db.reference(f'py/user/{user_id}')

    # Retrieve the current score of the user
    user_data = user_ref.get()

    if user_data:
        # Current score (default to 0 if not set)
        items_found_today = user_data.get('items_found_today', 0) + items_found
        total_items_found = user_data.get('total_items_found', 0) + items_found

        user_ref.update({
            'items_found_today': items_found_today,
            'total_items_found': total_items_found})


def update_daily_quest(user_id, quest_num, location):
    # Reference to the specific user's data in the database
    user_ref = db.reference(f'py/user/{user_id}')

    user_data = user_ref.get()

    quest_code = 'item'+str(quest_num)+'_found'
    quest_code_loc = 'item'+str(quest_num)+'_location'

    user_ref.update({
        quest_code: True,
        quest_code_loc: location})


def get_item_of_the_day(date):
    # Reference to the 'items_of_the_day' node in the database
    items_ref = db.reference('py/items_of_the_day')

    # Retrieve all items of the day
    items = items_ref.get()

    # Check if there are any items and filter by date
    if items:
        # Filter items that match the specified date
        matching_items = {item_id: item_info for item_id, item_info in items.items() if item_info.get('date') == date}

        if matching_items:
            return matching_items
        else:
            return {}
    else:
        return {}


# Example call to the function
print(get_item_of_the_day('03-11-2024'))

'''
add_user('user1', 'testuser1')
add_user('user2', 'testuser2')
add_user('user3', 'testuser3')

add_item_of_the_day('item1', 1, 'tree', '03-11-2024')
add_item_of_the_day('item2', 2, 'lake', '03-11-2024')
add_item_of_the_day('item3', 3, 'bridge', '03-11-2024')
add_item_of_the_day('item4', 1, 'bird', '04-11-2024')
add_item_of_the_day('item5', 2, 'car', '04-11-2024')
add_item_of_the_day('item6', 3, 'bike', '04-11-2024')

'''
#update_score('user1', 150)
#update_items_found('user2', 3)
#update_daily_quest('user3', 2, '00.000000, 00,000000')

#reset_user_stats()
