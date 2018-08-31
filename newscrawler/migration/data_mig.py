
"""
이 모듈은 어느 하나의 몽고디비에서 다른 몽고디디로 데이터를 이관하는 모둘이다.

"""
from utils.mongo import MongDAO

class from_settings():
    MONGODB_SERVER = "localhost"
    MONGODB_PORT = 27017


class to_settings():
    MONGODB_SERVER = "localhost"
    MONGODB_PORT = 27027



from_db = MongDAO(from_settings)

to_db = MongDAO(to_settings)


cond = {
    '$or': [
        {'mig': None},
        {'mig': {'$exists': False}},
        {'mig': 0}
    ]
}

def entries_to_remove(entries, the_dict):
    for key in entries:
        if key in the_dict:
            del the_dict[key]


def all_unset():
    from_db.update_many('articles', {}, {"$unset": {"mig": 1}})


def migdate():
    while True:
        cnt = from_db.count('articles', cond)
        if cnt > 0 :
            rows = from_db.find('articles', cond, limit=50)
            for row in rows:
                drow = to_db.find_one('articles', {'articleId': row['articleId']})
                if drow:
                    row['mig'] = -1
                    from_db.update('articles', row)
                else:
                    cp_row = row.copy()
                    entries_to_remove(['_id', 'elas'], cp_row)
                    to_db.insert('articles', cp_row)
                    row['mig'] = 1
                    from_db.update('articles', row)
        else:
            break


if __name__ == "__main__":
    # all_unset()
    migdate()