import random
import names
import db_utils

client = db_utils.get_connection('mongodb://localhost:27117')
db = client.Course_Work
collection = db.Users

kyiv_limits = [[50.553944, 30.397457], [50.552467, 30.688273],
               [50.364873, 30.431714], [50.384401, 30.698019]]


def random_cord():
    y = random.uniform(50.384401, 50.553944)
    x = random.uniform(30.397457, 30.688273)
    y = round(y, 6)
    x = round(x, 6)
    return y, x


def Validator_of_users(user):
    lat = user.get("latitude")
    long = user.get("longitude")

    # Checking if user is in Kyiv
    if not (50.384401 < lat < 50.553944 and 30.397457 < long < 30.688273):
        return False

    # Checking if user is not in Dripro
    if 50.355810 < lat < 50.524699 and 30.533193 < long < 30.600478:
        return False
    return True


def Generator_of_users(num_of_users):
    users = []
    i = 0
    while i != num_of_users:
        lat, long = random_cord()
        newUsr = {
            "firstName": names.get_first_name(gender=random.choice(['female', 'male'])),
            "lastName": names.get_last_name(),
            "latitude": lat,
            "longitude": long
        }
        if Validator_of_users(newUsr):
            users.append(newUsr)
            i = i + 1
    res = collection.insert_many(users)
