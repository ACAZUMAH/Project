import datetime
import bcrypt
import watch_list_db

print('Welcome to the watchlist app!')
create_user = ''' 
1) Create user
2) Log in 
3) Quit   
  Enter: '''
# this function is used to create an account
def create_account():
    user_name = input('Full Name: ')
    user_email = input('Email: ')
    user_password = input('Password: ').encode()
    user_password = hash_password(user_password)
    while(watch_list_db.add_user(user_name,user_email,user_password) == 'user name is taken!' or
        watch_list_db.add_user(user_name,user_email,user_password) ==  'email is taken'):
        print('User name or email taken log in with email or try again!')
        user_name = input('Full Name: ')
        user_email = input('Email: ')
        user_password = input('Password: ')
        watch_list_db.add_user(user_name,user_email,user_password)
        break
# this function hashes the user password
def hash_password(user_password):
    password = bytes(user_password)
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password,salt)
    return hashed_password
# this function is used to log into the app
def log_in():
    while True:
        user_email = input('Email: ')
        user_password = input('Password: ')
        stored_hash = watch_list_db.fetch_hash_password(user_email)
        password_encode = user_password.encode()
        if stored_hash:
            if bcrypt.hashpw(password_encode,stored_hash) == stored_hash:
                print()
                print(f'--- Welcome --- ')
                break
            else:
               print('User name or password not recognized')
               again = input('try again Y/N:').lower()
               if again == 'n':
                   break 
        else:
            print('User name or password not recognized')
            again = input('try again Y/N:').lower()
            if again == 'n':
                break 
# this function adds a movie into the database
def prompt_add_movie():
    title = input('Movie title: ')
    release_date = input('Release date (dd-mm-YYYY): ')
    parsed_date = datetime.datetime.strptime(release_date, '%d-%m-%Y')
    timestamp = parsed_date.timestamp()
    watch_list_db.add_movie(title, timestamp)
# this function adds watched movie into the database
def promt_add_to_watched():
    user_name = input('Username: ')
    movie_title = input('Enter the movie title you have watched: ')
    user_id = watch_list_db.get_user_id(user_name)
    movie_id = watch_list_db.get_movie_id(movie_title)
    if user_id:
        if movie_id:
            watch_list_db.add_to_watched(user_id, movie_id) 
        else:
            return 'This movie title is not in the movies list!'
    else:
        return 'This user name is not in the users list!'
    return "Added!"
# this function prints the movies and upcoming movies list
def view_movie_list(heading,movies):
    print(f'-- {heading} movies --')
    for _id,title,release_date in movies:
        movie_date = datetime.datetime.fromtimestamp(release_date)
        human_date = movie_date.strftime('%b %d %Y')
        print(f'{_id}: {title} (on {human_date})') 
    print('----\n')
# this function prints the watched movies list
def view_watched_movie_list(movies):
    print(f"--- watched movies ---")
    for movie in movies:
        print(movie)
    print('----\n')
# this function is used to search for a movie 
def promt_search_movie():
    search = input('Enter the movie title: ')
    movies = watch_list_db.get_searched_movie(search)
    if movies:
        view_movie_list('Movies found', movies)
    else:
        print('Found no movies for this search!')
# this function is used to update user names 
def promt_update_username():
    while True:
        email = input("Enter email: ")
        new_username = input('Enter new name:')
        password = input('Enter password:')
        password_encode = password.encode()
        stored_hash = watch_list_db.fetch_hash_password(email)
        if stored_hash:
            if bcrypt.hashpw(password_encode,stored_hash) == stored_hash:
                watch_list_db.update_username(new_username,email)
            else:
               print('Email or password not recognized!')
               again = input('try again Y/N:').lower()
               if again == 'n':
                   break 
        else:
            print('Email or password not recognized!')
            again = input('try again Y/N:').lower()
            if again == 'n':
                break 
        return "Updated!"
        break
# this function is used is to update movie titles
def promt_update_movies():
    user_name = input("Enter user name: ")
    old_movie = input("Enter old movie title: ")
    movie_id = watch_list_db.get_movie_id(old_movie)
    new_movie = input("Enter the new movie title: ")
    user_id = watch_list_db.get_user_id(user_name)
    if user_id:
        if movie_id:
            if watch_list_db.check_watched(user_id,movie_id):
                watch_list_db.delete_watched_movie(user_id,movie_id)
            watch_list_db.update_movies(new_movie,movie_id)
        else:
            return "This movie title is not in the movies list!"
    else:
        return "This user name is not on the users list!"
    return "Updated!"
# this function deletes an account
def promt_delete_account():
    email = input("enter email: ")
    password = input("enter password: ")
    password_encode = password.encode()
    stored_hash = watch_list_db.fetch_hash_password(email)
    if stored_hash:
        if bcrypt.hashpw(password_encode, stored_hash) == stored_hash:
            watch_list_db.delete_account(email)
        else:
            return "Email or password not recognized!"
    else:    
        return "Email or password not recognized!"
    return "Successfully deleted!"
# the function deletes a watched movies
def promt_delete_watched_movie():
    user_name = input("Enter user name: ")
    movie_title = input("Enter movie title: ")
    user_id = watch_list_db.get_user_id(user_name)
    movie_id = watch_list_db.get_movie_id(movie_title)
    if user_id:
        if movie_id:
            watch_list_db.delete_watched_movie(user_id, movie_id)
        else:
            return "This movie title is not in the watched list!"
    else:
        return "This user name is not in the watched list!"
    return "Successfully deleted!"
# this function deletes a movie
def promt_delete_movie():
    user_name = input("Enter user name: ")
    movie_title = input("Enter movie title: ")
    movie_id = watch_list_db.get_movie_id(movie_title)
    user_id = watch_list_db.get_user_id(user_name)
    if user_id:
        if movie_id:
            if watch_list_db.check_watched(user_id,movie_id):
                watch_list_db.delete_watched_movie(user_id,movie_id)
            watch_list_db.delete_movie(movie_id)
        else:
            return "This movie title is not in the movies list!"
    else:
        return "This user name is not in the users list!"
    return "Successfully deleted!"
watch_list_db.create_tables()
# this loop is used for creating and logging into an account
control = True
while control:
    user_responce = input(create_user)
    if user_responce == '3':
        break
    elif user_responce == '1':
        create_account()
        control = False
        loop_two = True
    elif user_responce == '2':
        log_in()
        control = False
        loop_two = True
 # this loop is used for the menu selection 
while loop_two:
    menu = input('''Please select from the menu:
    1) Adds.
    2) Views.
    3) Seaches.
    4) Updates.
    5) Deletes.
    6) Exit.
            Your selection : ''')
    if menu == '6':
        break
    elif menu == '1': 
        # this loop displays the add menu
        while True:
            adds_promt = input('''
            1) Add a movie.
            2) Add to Watched movies.
            3) Back
                        Select: ''')
            if adds_promt == '1':
                prompt_add_movie()
                print()
                break
            elif adds_promt == '2':
                print(promt_add_to_watched())
                break
            elif adds_promt == "3":
                break
            else:
                again = input("Invalid input try again Y/N").lower()
                if again == 'n':
                    break
    elif menu == "2":
        # this loop diplays the views menu
        while True:
            views_promt = input('''
            1) View all movies.
            2) View upcoming movies.
            3) View watched movies.
            4) Back 
                            Select: ''')
            if views_promt == '1':
                view_movie_list('All',watch_list_db.get_movies())
                break
            elif views_promt == '2':
                view_movie_list('Upcoming',watch_list_db.get_movies(True))
                break
            elif views_promt == '3':
                user_name = input('Username: ')
                movies = watch_list_db.get_watched_movies(user_name)
                if movies:
                   view_watched_movie_list(movies)
                else:
                   print("You don't have watched movies yet")
            elif views_promt == "4":
                break
            else:
                again = input("Invalid input try again Y/N:").lower()
                if again == 'n':
                    break
    elif menu == "3":
        promt_search_movie()
    elif menu == "4":
        # this loop displays the updates menu 
        while True:
            updates_promt = input('''
            1) Update user name.
            2) Update a movie.
            3) Back
                Select: ''')
            if updates_promt == '1':
                print(promt_update_username())
                break
            elif updates_promt == '2':
                print(promt_update_movies())
                break
            elif updates_promt == "3":
                break
            else:
                again = input("Invalid input try again Y/N:").lower()
                if again == 'n':
                    break
    elif menu == "5":
        # this loop displays the deletes menu
        while True:
            deletes_promt = input('''
            1) Delete account.
            2) Delete a watched movie.
            3) delete a movie.
            4) Back
                        Select: ''')
            if deletes_promt == '1':
                print(promt_delete_account())
                break
            elif deletes_promt == '2':
                print(promt_delete_watched_movie())
                break
            elif deletes_promt == '3':
                print(promt_delete_movie())
                break
            elif deletes_promt == "4":
                break
            else:
                again = input("Invalid input try again Y/N:").lower()
                if again == 'n':
                    break            
    else:
        print('Invalid input, Please try again!') 
        
    
