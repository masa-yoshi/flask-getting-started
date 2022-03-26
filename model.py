import json

""" 
loads() method can be used to parse a valid JSON string 
and convert it into a Python Dictionary. 
"""
def load_db():
    with open("flashcards_db.json") as f:
        return json.load(f)


""" 
dump() method is used to save the data
"""
def save_db():
    with open("flashcards_db.json", 'w') as f:
        return json.dump(db, f, indent=2)

db = load_db()