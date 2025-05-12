from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from SMalchemyBase import Base, User, Vote, Search, Friendship, UserInterests, Interest, Place, Event, SharedThought, Blocked


# Connect to your SQLite database
engine = create_engine("sqlite:///SocialMap.db")
Session = sessionmaker(bind=engine)
session = Session()


# These are some preset cities that users can pick when adding their location to their profile.
# This helps make sure people don't type cities in random ways and mess up the database.
# This ties back to the User table since the location is saved there.
allowed_locations= ["Minneapolis", "Saint Paul",  "Duluth",  "Rochester",  "Bloomington",  "Mankato", "St. Cloud"]
def get_location_input():
    print("\nAvailable Locations:")
    for loc in allowed_locations:
        print(f"- {loc}")
    while True:
        loc = input("Enter your location exactly as shown above: ")
        if loc in allowed_locations:
            return loc
        else:
            print("Invalid location. Please choose from the list.")


# This helps users pick a gender so that it's always the same wording across the "program"
# This connects to the User table since the gender is part of their profile.
def get_gender_input(current_gender=None):
    print("\nAvailable Genders: Female, Male, Other")
    while True:
        gender = input(f"Gender [{current_gender or ''}]: ").capitalize() or current_gender
        if gender in ["Female", "Male", "Other"]:
            return gender
        print("Invalid gender. Please choose 'Female', 'Male', or 'Other'.")


#this is the main menu for SocialMap :)
# Main menu where users can choose to register, log in, or exit the program.
# This doesn't touch any tables directly but starts the whole program.
#AI USAGE: In the bottom of main menu theres a except because when I ran this code I would get a error and AI recommened to add this which seemed to help. 
def main_menu():
    #main menu to welcome a user/existing user (1)
    try:
        while True:
            print("\n--- Welcome to SocialMap ---")
            print("1. Register New User")
            print("2. Log In")
            print("0. Exit")
            choice = input("Choose an option: ")

            if choice == "1":
                user = register_user()
                if user:
                    logged_in_menu(user)
            elif choice == "2":
                user = login_user()
                if user:
                    logged_in_menu(user)
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Try again.")

    except KeyboardInterrupt:
        print("\n\n[!] Program interrupted by user. Exiting safely.\n")
        exit(0)


# This lets new users make an account by adding basic info like email, username, etc.
# It checks if the email and username are already used. This ties to the User table.
def register_user():
    print("\n--- Register New User ---")
    email = input("Email (or 'exit' to cancel): ")
    if email.lower() == 'exit':
        return None

    if session.query(User).filter_by(email=email).first():
        print("Email already taken. Please try again with a different email.")
        return None
    
    password = input("Password: ")

    username = input("Username: ")
    if session.query(User).filter_by(username=username).first():
        print("Username already taken. Please try again with a different username.")
        return None
    
    first = input("First name: ")
    last = input("Last name: ")
    location = get_location_input() #makes sure they choose one of the ones we listed
    gender = get_gender_input() #makes sure they choose one of the ones we listed 
    new_user = User(email=email, password=password, username=username,  first_name=first, last_name=last, location=location, gender=gender, created_at=datetime.now(timezone.utc))
    session.add(new_user)
    session.commit()
    print(f"User '{username}' registered and logged in!")
    show_profile_summary(new_user)
    return new_user


# This lets existing users log in by checking their email and password.
# It connects to the User table to find their account.
def login_user():
    print("\n--- Log In ---")
    email = input("Email (or 'exit' to cancel): ")
    if email.lower() == 'exit':
        return None
    
    password = input("Password: ")
    user = session.query(User).filter_by(email=email, password=password).first()
    if user:
        print(f"Welcome back, {user.username}!")
        show_profile_summary(user)
        return user
    else:
        print("Login failed. Please check your email and password.")
        return None
    

# After logging in or registering, this shows the user's basic profile info like their name, email, and interests.
# This pulls from User, UserInterests, and Interest tables.
def show_profile_summary(user):
    print("\n--- Your Profile Summary ---")
    print(f"Username: {user.username}")
    print(f"Email: {user.email}")
    print(f"Name: {user.first_name} {user.last_name}")
    print(f"Location: {user.location}")
    print(f"Gender: {user.gender}")
    print(f"Religion: {user.religion or 'Not set'}")
    print(f"Race: {user.race or 'Not set'}")
    print(f"Bio: {user.bio or 'Not set'}")
    print(f"Interests: ", end="")
    interests = session.query(UserInterests).filter_by(user_id=user.id).all()
    if interests:
        print(", ".join(session.query(Interest).get(i.interest_id).name for i in interests))
    else:
        print("None")


# This is the main menu after logging in. It lets users do all the different features in the app.
# No direct table connection here, but it leads to the other functions that do.
def logged_in_menu(user):
    print(f"\n--- Welcome, {user.username}! ---")
    while True:
        print("\n--- Main Menu ---")
        print("1. Create an Event")
        print("2. View All Events")
        print("3. Share a Thought")
        print("4. Search Places")
        print("5. Vote on a Place")
        print("6. Leave a Ghost at a Place")
        print("7. Add a Friend")
        print("8. Block a User")
        print("9. Edit My Profile")
        print("10. View Notifications (Nearby Users, Shared Interests, Friends' Thoughts)")
        print("11. Log Out")

        choice = input("\nChoose an option: ")

        if choice == "1":
            add_event(user)
        elif choice == "2":
            view_events()
        elif choice == "3":
            share_thought(user)
        elif choice == "4":
            search_places()
        elif choice == "5":
            vote_on_place(user)
        elif choice == "6":
            leave_ghost(user)
        elif choice == "7":
            add_friend(user)
        elif choice == "8":
            block_user(user)
        elif choice == "9":
            edit_profile(user)
        elif choice == "10":
            view_notifications(user)
        elif choice == "11":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please try again.")


# This lets users see all the places that have been added, along with how many upvotes and downvotes each place has.
# It uses the Place and Vote tables.
#AI USAGE: I wanted to add a thumbs up and down for the funs and asked chat to include them in the last line. 
def view_all_places():
    print("\n--- All Places ---")
    places = session.query(Place).all()
    if not places:
        print("No places found.")
    for p in places:
        upvotes = session.query(Vote).filter_by(place_id=p.id, up_down=True).count()
        downvotes = session.query(Vote).filter_by(place_id=p.id, up_down=False).count()
        print(f"ID: {p.id} | Name: {p.name} | Category: {p.category} | Location: {p.location} | 👍 {upvotes} | 👎 {downvotes}")


# This lets users add new places to the database by giving details like the name, category, and location.
# This saves data to the Place table.
def add_place():
    print("\n--- Add a New Place ---")
    name = input("Place name (or 'exit' to cancel): ")
    if name.lower() == "exit":
        return
    
    category = input("Category: ")
    location = get_location_input()
    try:
        x = float(input("Latitude: "))
        y = float(input("Longitude: "))
    except ValueError:
        print("Invalid coordinates. Returning to the main menu.")
        return

    description = input("Description: ")
    place = Place(name=name, category=category, location=location, x=x, y=y, description=description)
    session.add(place)
    session.commit()
    print(f"Place '{name}' added!")


# This lets users create events at existing places by giving a name, category, and date.
# It uses the Place and Event tables.
def add_event(user):
    print("\n--- Add an Event ---")
    view_all_places()
    place_name = input("Enter the name of the place for this event (or 'exit' to cancel): ")
    if place_name.lower() == "exit":
        return
    place = session.query(Place).filter_by(name=place_name).first()
    if not place:
        print("Place not found. Please add the place first.")
        return
    name = input("Event name: ")
    category = input("Category: ")
    description = input("Description: ")
    date_str = input("Event date (YYYY-MM-DD): ")
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        dt = dt.replace(hour=12, minute=0)
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    event = Event(name=name, category=category, x=place.x, y=place.y, description=description,
                  place_id=place.id, user_id=user.id, event_date_time=dt, created_at=datetime.now(timezone.utc))
    session.add(event)
    session.commit()
    print("Event created!")


# This shows a list of all events that have been created so far.
# This pulls from the Event table.
def view_events():
    print("\n--- All Events ---")
    events = session.query(Event).all()
    if not events:
        print("No events found.")
    for event in events:
        print(f"{event.name} at place {event.place_id} on {event.event_date_time}")


# This lets users post a "thought" or a short message. (only friends can see)
# It saves the message to the SharedThought table.
def share_thought(user):
    print("\n--- Share a Thought ---")
    text = input("Thought (or 'exit' to cancel): ")
    if text.lower() == "exit":
        return 

    thought = SharedThought(user_id=user.id, text=text, created_at=datetime.now(timezone.utc))
    session.add(thought)
    session.commit()
    print("Thought shared!")


# This lets users add other users as friends by searching for their username.
# It uses the Friendship table.
def add_friend(user):
    print("\n--- Add a Friend ---")
    print("Type 'exit' to return to the main menu.")

    existing_friendships = session.query(Friendship).filter_by(user_id1=user.id).all()
    if existing_friendships:
        print("Your current friends:")
        for f in existing_friendships:
            friend = session.query(User).filter_by(id=f.user_id2).first()
            if friend:
                print(f"- {friend.username}")
    else:
        print("You have no friends yet.")

    while True:
        friend_username = input("Enter the username of the user you want to add as a friend: ")
        if friend_username.lower() == "exit":
            return

        friend = session.query(User).filter(User.username.ilike(friend_username)).first()
        if not friend:
            print("User not found. Please try again.")
            continue

        if friend.id == user.id:
            print("You cannot add yourself. Please try again.")
            continue

        existing = session.query(Friendship).filter_by(user_id1=user.id, user_id2=friend.id).first()
        if existing:
            print(f"You are already friends with {friend.username}.")
            return

        friendship = Friendship(user_id1=user.id, user_id2=friend.id, created_at=datetime.now(timezone.utc))
        session.add(friendship)
        session.commit()
        print(f"You are now friends with {friend.username}.")
        return


# This lets users block other users if they don’t want to interact with them anymore.
# It uses the Blocked table.
def block_user(user):
    print("\n--- Block a User ---")
    print("Type 'exit' to return to the main menu.")

    existing_blocks = session.query(Blocked).filter_by(blocker_id=user.id).all()
    if existing_blocks:
        print("You have already blocked:")
        for b in existing_blocks:
            blocked_user = session.query(User).filter_by(id=b.blocked_id).first()
            if blocked_user:
                print(f"- {blocked_user.username}")
    else:
        print("You have not blocked anyone yet.")

    while True:
        blocked_username = input("Enter the username of the user you want to block: ")
        if blocked_username.lower() == "exit":
            return

        blocked_user = session.query(User).filter(User.username.ilike(blocked_username)).first()
        if not blocked_user:
            print("User not found. Please try again.")
            continue

        if blocked_user.id == user.id:
            print("You cannot block yourself. Please try again.")
            continue

        existing = session.query(Blocked).filter_by(blocker_id=user.id, blocked_id=blocked_user.id).first()
        if existing:
            print(f"You have already blocked {blocked_user.username}.")
            return

        block = Blocked(blocker_id=user.id, blocked_id=blocked_user.id)
        session.add(block)
        session.commit()
        print(f"You have blocked {blocked_user.username}.")
        return


# This lets users update their profile details like location, religion, race, and bio.
# It also lets them add new interests with a category, which saves to the Interest and UserInterests tables.
def edit_profile(user):
    while True:
        print("\n--- Edit Profile ---")
        print("1. Update Location")
        print("2. Update Religion")
        print("3. Update Race")
        print("4. Update Bio")
        print("5. Add Interest")
        print("0. Return to Main Menu")

        choice = input("Choose an option: ")
        if choice == "1":
            user.location = get_location_input()
        elif choice == "2":
            user.religion = input(f"Religion [{user.religion if user.religion else ''}]: ") or user.religion
        elif choice == "3":
            user.race = input(f"Race [{user.race if user.race else ''}]: ") or user.race
        elif choice == "4":
            user.bio = input(f"Bio [{user.bio if user.bio else ''}]: ") or user.bio
        elif choice == "5":
            interest_name = input("Interest name: ")
            interest_category = input("Interest category: ")

            existing_interest = session.query(Interest).filter_by(name=interest_name, category=interest_category).first()
            if not existing_interest:
                existing_interest = Interest(name=interest_name, category=interest_category)
                session.add(existing_interest)
                session.commit()
                print(f"Created new interest '{interest_name}' under category '{interest_category}'")
            user_interest_link = UserInterests(user_id=user.id, interest_id=existing_interest.id)
            session.add(user_interest_link)
            session.commit()
            print(f"Interest '{interest_name}' added to your profile.")
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please select a valid option.")
            continue

        print("\nProfile updated!")
        show_profile_summary(user)

        again = input("\nWould you like to edit anything else? (yes/no): ").lower()
        if again != "yes":
            break


# This lets users search for places by name or category.
# It pulls data from the Place table and uses the search table.
def search_places(user):
    print("\n--- Search Places ---")
    term = input("Search by name or category: ").lower()
    search_log = Search(user_id=user.id, search_term=term, searched_at=datetime.now(timezone.utc))
    session.add(search_log)
    session.commit()
    results = session.query(Place).filter((Place.name.contains(term)) | (Place.category.contains(term))).all()
    if results:
        for p in results:
            print(f"{p.id}: {p.name} - {p.category} at {p.location}")
    else:
        print("No results.")


# This lets users vote "up" or "down" on a place. They can also update their vote if they change their mind.
# It uses the Vote table.
def vote_on_place(user):
    print("\n--- Vote on a Place ---")
    print("Type 'exit' to cancel and return to the main menu.")
    view_all_places()
    while True:
        place_id_input = input("Enter Place ID: ")
        if place_id_input.lower() == "exit":
            return
        if not place_id_input.isdigit():
            print("Invalid input. Please enter a numeric Place ID.")
            continue

        place_id = int(place_id_input)
        place = session.query(Place).filter_by(id=place_id).first()
        if not place:
            print("No place found with that ID. Please try again.")
            continue
        break  # Valid place found

    while True:
        vote_type = input("Vote 'up' or 'down': ").lower()
        if vote_type == "exit":
            return
        if vote_type not in ["up", "down"]:
            print("Invalid vote type. Please enter 'up' or 'down'.")
            continue
        break

    existing_vote = session.query(Vote).filter_by(user_id=user.id, place_id=place_id).first()
    if existing_vote:
        existing_vote.up_down = (vote_type == "up")
        print("Updated your vote.")
    else:
        session.add(Vote(user_id=user.id, place_id=place_id, up_down=(vote_type == "up")))
        print("Vote recorded.")
    session.commit()


# This is just a fun feature that lets users "leave a ghost" at a place. It doesn’t actually save anything to the database.
# It's mostly for user engagement.
def leave_ghost(user):
    print("\n--- Leave a Ghost ---")
    print("Type 'exit' to cancel and return to the main menu.")
    view_all_places()
    while True:
        place_id_input = input("Enter Place ID to leave a ghost at: ")
        if place_id_input.lower() == "exit":
            return
        if not place_id_input.isdigit():
            print("Invalid input. Please enter a numeric Place ID.")
            continue

        place_id = int(place_id_input)
        place = session.query(Place).filter_by(id=place_id).first()
        if not place:
            print("No place found with that ID. Please try again.")
            continue
        break  # Valid place found

    print(f"Ghost left at {place.name} (ID {place_id}) for User ID {user.id} ")


# This shows users who else is in the same location (encounter feature).
# It also shows people with similar interests and friends' shared thoughts.
# It uses User, Blocked, UserInterests, Interest, Friendship, and SharedThought tables.
def view_notifications(user):
    print("\n--- Notification Center ---")

    # Get IDs of users blocked by the current user
    blocked_user_ids = {b.blocked_id for b in session.query(Blocked).filter_by(blocker_id=user.id).all()}

    # --- Nearby Users / Encounters ---
    nearby_users = session.query(User).filter(
    User.id != user.id,
    User.location == user.location,
    ~User.id.in_(blocked_user_ids)).all()

    if nearby_users:
        print(f"\nUsers currently in {user.location}:")
        for other_user in nearby_users:
            print(f"- {other_user.username}")
    else:
        print(f"\nNo nearby users found in {user.location}.")

    # --- Users With Shared Interests ---
    user_interests = session.query(UserInterests).filter_by(user_id=user.id).all()
    user_interest_ids = {ui.interest_id for ui in user_interests}

    matching_users_found = False
    for other_user in session.query(User).filter(User.id != user.id).all():
        if other_user.id in blocked_user_ids:
            continue  # Skip blocked users

        other_user_interests = session.query(UserInterests).filter_by(user_id=other_user.id).all()
        other_interest_ids = {oui.interest_id for oui in other_user_interests}
        common_interest_ids = user_interest_ids & other_interest_ids

        if common_interest_ids:
            matching_users_found = True
            interests_list = [session.query(Interest).get(i).name for i in common_interest_ids]
            interests_str = ", ".join(interests_list)
            print(f"\n{other_user.username} shares your interest(s): {interests_str}")

    if not matching_users_found:
        print("\nNo users share your interests.")

    # --- Friends' Shared Thoughts ---
    friendships = session.query(Friendship).filter_by(user_id1=user.id).all()
    if friendships:
        print("\nFriends' Shared Thoughts:")
        found_thoughts = False
        for friendship in friendships:
            friend = session.query(User).filter_by(id=friendship.user_id2).first()
            if friend and friend.id not in blocked_user_ids:
                thoughts = session.query(SharedThought).filter_by(user_id=friend.id).all()
                for thought in thoughts:
                    print(f"- {friend.username} shared: {thought.text}")
                    found_thoughts = True
        if not found_thoughts:
            print("- No shared thoughts yet.")
    else:
        print("\nYou have no friends yet.")


main_menu()