import random
from bson import ObjectId
import db_utils

from numpy import random

client = db_utils.get_connection('mongodb://localhost:27117')
db = client.Course_Work
collection = db.Checks


def get_random_time():
    hour = random.randint(8, 22)
    minutes = random.randint(1, 59)
    seconds = random.randint(1, 59)
    res = str(hour) + ":" + str(minutes) + ":" + str(seconds)
    return res


def get_random_date(x):
    days = ["Monday", "Tuesday","Thursday", "Sunday","Saturday","Friday", "Wednesday"]
    if x == 0 or x == 7:
        return days[0]
    return days[x]


def round_nums(num):
    rounded = round(num)
    if rounded == 0:
        rounded = 1
    return rounded


def Validation_of_checks(sum, num_of_purchases):
    if (sum / num_of_purchases) < 100:
        return False
    return True


def Generator_of_checks(num_of_checks):
    checks = []
    ids = [str(check_id) for check_id in db.Users.find().distinct('_id')]
    sums = random.chisquare(df=6, size=num_of_checks)
    dates = random.binomial(n=7, p=0.5, size=num_of_checks)
    nums = random.chisquare(df=1, size=num_of_checks)
    i = 0
    while i != num_of_checks:
        check = {
            "owner": ObjectId(random.choice(ids)),
            "sum": int(round(sums[i] * 2000)),
            "num_of_purchases": round_nums(nums[i]),
            "time": get_random_time(),
            "day_of_week": get_random_date(dates[i])
        }
        if Validation_of_checks(round(sums[i] * 2000), round_nums(nums[i])):
            checks.append(check)
            i = i + 1
        else:
            nums[i] = nums[i] - 1

    res = collection.insert_many(checks)


