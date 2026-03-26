import json


def addCredits(username):
    dollars = float(input("Enter the amount of dollars you would like to add: "))
    credits_to_add = int(dollars * 3)
    try: 
        with open("data/users.json", "r") as file:
            users = json.load(file)
            for name in users['users']: 
                if name['username'] == username:
                    name['credits'] += credits
                    print(f"Added {credits_to_add} credits to {username}'s account. You now have {name['credits']} credits.")
                    break
        with open("data/users.json", "w") as file:
            json.dump(users, file, indent=4)
    except json.JSONDecodeError:
        print("Error: users.json is not a valid JSON file.")

def checkUse(username):
    try: 
        with open("data/users.json", "r") as file:
            foundUsername = False
            users = json.load(file)
            for name in users['users']: 
                if name['username'] == username:
                    foundUsername = True
                    print(f"Welcome, {username}!")
                    credits = name['credits']
                    print(f"You have {credits} credits.")
                    
                    break
            if not foundUsername:
                print("Username not found. Please try again. Would you like to create an account? (yes/no)")
                createUser(username)
                return False
    except json.JSONDecodeError:
        print("Error: users.json is not a valid JSON file.")
        return False            
    return True

def createUser(username):
    try: 
        with open("data/users.json", "r") as file:
            users = json.load(file)
            users['users'].append({"username": username})
        with open("data/users.json", "w") as file:
            json.dump(users, file, indent=4)
    except json.JSONDecodeError:
        print("Error: users.json is not a valid JSON file.")

