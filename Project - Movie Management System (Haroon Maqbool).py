import tkinter as tk
from PIL import ImageTk, Image

USER_DATA_FILE = "user_data.txt"
MOVIE_DATA_FILE = "movie_data.txt"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123"


class UserManagement:
    @staticmethod
    def load_data(file_path):
        with open(file_path, 'r') as file:
            users = [eval(line) for line in file.readlines()]
        return users

    @staticmethod
    def save_data(data, file_path):
        with open(file_path, 'w') as file:
            for user in data:
                file.write(str(user) + "\n")

    @staticmethod
    def get_movies():
        with open(MOVIE_DATA_FILE, 'r') as file:
            movies = [line.strip() for line in file.readlines()]
            return movies

    def login_user(self, username, password):
        users = self.load_data(USER_DATA_FILE)
        for user in users:
            if user.get('username') == username and user.get('password') == password:
                return user
        return None

    @staticmethod
    def is_admin(username, password):
        return username == ADMIN_USERNAME and password == ADMIN_PASSWORD


class FilterSortMenu(tk.Toplevel):
    def __init__(self, parent, movies):
        tk.Toplevel.__init__(self, parent)
        self.title("Movies List")
        self.geometry("1000x600")
        self.configure(bg="#040405")
        self.movies = movies
        self.filtered_movies = movies

        (tk.Label(self, text="Enter the Movie to Filter or Sort", font=("Arial", 16, "bold"), bg="#040405", fg="white")
         .pack(pady=10))
        self.search_entry = tk.Entry(self, font=("Arial", 12), width=50)
        self.search_entry.pack(pady=5)

        button_frame = tk.Frame(self, bg="#040405")
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Filter", command=self.apply_filter, font=("Arial", 12), bg="#3498db", fg="white",
                  relief=tk.GROOVE, width=15).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Sort", command=self.apply_sort, font=("Arial", 12), bg="#3498db", fg="white",
                  relief=tk.GROOVE, width=15).pack(side=tk.LEFT, padx=5)

        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE, font=("Arial", 12), bg="#040405", fg="white", height=20,
                                  width=150)

        for movie in self.filtered_movies:
            self.listbox.insert(tk.END, movie)
        self.listbox.pack(pady=10)

        tk.Button(self, text="Back to Menu", command=self.go_back_to_menu, font=("Arial", 12), bg="#e74c3c", fg="white",
                  relief=tk.GROOVE, width=20).pack(side=tk.LEFT, padx=5)

        tk.Button(self, text="Add to Watchlist", command=self.add_to_watchlist, font=("Arial", 12), bg="#2ecc71",
                  fg="white", relief=tk.GROOVE, width=20).pack(side=tk.RIGHT, padx=5)

        self.watchlist_status_var = tk.StringVar()
        tk.Label(self, textvariable=self.watchlist_status_var, font=("Arial", 12),
                 fg="green", bg="#040405").pack(pady=5)

        self.error_message_var = tk.StringVar()
        tk.Label(self, textvariable=self.error_message_var, font=("Arial", 12), fg="red",
                 bg="#040405").pack(pady=5)

    def apply_filter(self):
        search_text = self.search_entry.get().lower()
        if search_text:
            self.filtered_movies = []
            for movie in self.movies:
                if search_text in movie.lower():
                    self.filtered_movies.append(movie)
            self.update_listbox()
        else:
            self.error_message_var.set("Please enter a movie to filter.")

    def apply_sort(self):
        self.filtered_movies.sort()
        self.update_listbox()

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for movie in self.filtered_movies:
            self.listbox.insert(tk.END, movie)

    def add_to_watchlist(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_movie = self.filtered_movies[selected_index[0]]
            watchlist = MovieManagementSystem.current_user.get('watchlist', [])
            if selected_movie in watchlist:
                self.watchlist_status_var.set(f"{selected_movie} is already in the watchlist.")
            else:
                watchlist.append(selected_movie)
                MovieManagementSystem.current_user['watchlist'] = watchlist
                self.watchlist_status_var.set(f"{selected_movie.split(';')[0]} added to the watchlist.")
        else:
            self.error_message_var.set("Please select a movie to add to the watchlist.")

    def go_back_to_menu(self):
        self.destroy()


class WatchListMenu(tk.Toplevel):
    def __init__(self, parent, watchlist):
        tk.Toplevel.__init__(self, parent)
        self.title("Watchlist")
        self.geometry("1000x600")
        self.configure(bg="#040405")
        self.watchlist = watchlist

        tk.Label(self, text="Your Watchlist", font=("Arial", 16, "bold"), fg="white", bg="#040405").pack(pady=10)
        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE, font=("Arial", 12), bg="#040405", fg="white", height=20,
                                  width=150)
        self.update_listbox()
        self.listbox.pack(pady=10)
        button_frame = tk.Frame(self, bg="#040405")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Delete from Watchlist", command=self.delete_from_watchlist,
                  font=("Arial", 12), bg="#BF3EFF", fg="white", relief=tk.GROOVE, width=20).pack(side=tk.RIGHT, padx=5)
        tk.Button(button_frame, text="Back to Menu", command=self.destroy, font=("Arial", 12),
                  bg="#e74c3c", fg="white", relief=tk.GROOVE, width=20).pack(side=tk.LEFT, padx=5)
        self.status_label = tk.Label(self, text="", font=("Arial", 12), fg="#e74c3c", bg="#040405")
        self.status_label.pack(pady=5)

    def delete_from_watchlist(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_movie = self.watchlist[selected_index[0]]
            if selected_movie in MovieManagementSystem.current_user.get('watchlist', []):
                MovieManagementSystem.current_user['watchlist'].remove(selected_movie)
                self.watchlist = MovieManagementSystem.current_user['watchlist']
                self.update_listbox()
                self.status_label.config(text=f"{selected_movie.split(';')[0]} removed from the watchlist.")
            else:
                self.status_label.config(text=f"{selected_movie} is not in the watchlist.")
        else:
            self.status_label.config(text="Please select a movie to delete from the watchlist.")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for movie in self.watchlist:
            self.listbox.insert(tk.END, movie)


class RatingMenu(tk.Toplevel):
    def __init__(self, parent, predefined_movies):
        tk.Toplevel.__init__(self, parent)
        self.title("Rate and Review Movies")
        self.geometry("1000x600")
        self.configure(bg="#040405")
        self.predefined_movies = predefined_movies
        self.selected_movie = tk.StringVar()
        self.rating_var = tk.StringVar()
        self.review_var = tk.StringVar()

        tk.Label(self, text="Select Movie:", font=("Arial", 12, "bold"), bg="#040405", fg="white").pack(pady=5)

        self.movie_dropdown = tk.OptionMenu(self, self.selected_movie, *self.predefined_movies)
        self.movie_dropdown.config(font=("Arial", 12), bg="#040405", fg="white",
                                   cursor="arrow")
        self.movie_dropdown.pack(pady=5)

        tk.Label(self, text="Rating (1-5):", font=("Arial", 12, "bold"), bg="#040405", fg="white").pack(pady=5)
        self.rating_entry = tk.Entry(self, textvariable=self.rating_var, font=("Arial", 12), width=8,
                                     bg="#040405", fg="white", cursor="arrow", insertbackground="white",
                                     insertofftime=500, insertontime=500)
        self.rating_entry.pack(pady=5)

        tk.Label(self, text="Review:", font=("Arial", 12, "bold"), bg="#040405", fg="white").pack(pady=5)
        self.review_entry = tk.Text(self, font=("Arial", 12), width=75, height=15,
                                    bg="#040405", fg="white", cursor="arrow", insertbackground="white",
                                    insertofftime=500, insertontime=500)
        self.review_entry.pack(pady=10)

        button_frame = tk.Frame(self, bg="#040405")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Back to Menu", command=self.go_back_to_menu, font=("Arial", 12),
                  bg="#e74c3c", fg="white", relief=tk.GROOVE, width=20, cursor="hand2").pack(side=tk.LEFT,
                                                                                             padx=5)

        tk.Button(button_frame, text="Submit", command=self.submit, font=("Arial", 12),
                  bg="#2ecc71", fg="white", relief=tk.GROOVE, width=20, cursor="hand2").pack(side=tk.RIGHT,
                                                                                             padx=5)
        self.submit_status_var = tk.StringVar()
        self.submit_status_label = tk.Label(self, textvariable=self.submit_status_var, font=("Arial", 12), fg="green",
                                            bg="#040405")
        self.submit_status_label.pack(pady=5)

        self.error_message_var = tk.StringVar()
        self.error_message_label = tk.Label(self, textvariable=self.error_message_var, font=("Arial", 12), fg="red",
                                            bg="#040405")
        self.error_message_label.pack(pady=5)

    def submit(self):
        movie_name = self.selected_movie.get()
        rating = self.rating_var.get()
        review = self.review_entry.get("1.0", tk.END).strip()

        if not movie_name:
            self.error_message_var.set("Please select a movie.")
        elif not rating or not rating.isdigit() or not (1 <= int(rating) <= 5):
            self.error_message_var.set("Please enter a valid rating (1-5).")
        elif not review:
            self.error_message_var.set("Please enter a review.")
        else:
            username = MovieManagementSystem.current_user['username']
            users = UserManagement.load_data(USER_DATA_FILE)

            for user in users:
                if user['username'] == username:
                    user_reviews = user.get('reviews', [])
                    user_reviews.append({
                        'movie': movie_name,
                        'rating': rating,
                        'review': review
                    })
                    user['reviews'] = user_reviews

            self.submit_status_var.set(f"Review for {movie_name.split(';')[0]} stored for user {username}")
            self.after(3000, self.destroy)
            UserManagement.save_data(users, USER_DATA_FILE)

    def go_back_to_menu(self):
        self.destroy()


class RegisterWindow(tk.Toplevel):
    ALLOWED_GENRES = ['Action', 'Comedy', 'Drama', 'Thriller', 'Romance', 'Horror', 'Adventure', 'Documentary', 'Crime']

    def __init__(self, parent):
        tk.Toplevel.__init__(self)
        self.title("Register")
        self.geometry("1000x685")
        self.configure(bg="#040405")
        self.parent = parent
        self.error_message_var = tk.StringVar()
        self.success_message_var = tk.StringVar()

        tk.Label(self, text="Full Name:", font=("Arial", 14), bg="#040405", fg="white").pack(pady=10)
        self.fullname_entry = tk.Entry(self, font=("Arial", 12), width=40)
        self.fullname_entry.pack(pady=10)

        tk.Label(self, text="Username:", font=("Arial", 14), bg="#040405", fg="white").pack(pady=10)
        self.username_entry = tk.Entry(self, font=("Arial", 12), width=40)
        self.username_entry.pack(pady=10)

        tk.Label(self, text="Password:", font=("Arial", 14), bg="#040405", fg="white").pack(pady=10)

        self.password_frame = tk.Frame(self, bg="#040405")
        self.password_frame.pack(pady=10)

        self.password_entry = tk.Entry(self.password_frame, show="*", font=("Arial", 12), width=36)
        self.password_entry.pack(side=tk.LEFT)

        self.show_image = ImageTk.PhotoImage(file='show.png')
        self.hide_image = ImageTk.PhotoImage(file='hide.png')

        self.show_hide_button = tk.Button(self.password_frame, image=self.show_image,
                                          command=self.password_eye,
                                          font=("Arial", 12), fg="#3498db", relief=tk.FLAT, bd=0)
        self.show_hide_button.pack(side=tk.RIGHT, padx=5)

        tk.Label(self, text="Favorite Genre (e.g. Action, Comedy): ", font=("Arial", 14), bg="#040405",
                 fg="white").pack(pady=10)

        self.favorite_genre_entry = tk.Entry(self, font=("Arial", 12), width=40)
        self.favorite_genre_entry.pack(pady=10)

        tk.Label(self, text="Security Question:", font=("Arial", 14), bg="#040405", fg="white").pack(pady=10)
        self.security_question_entry = tk.Entry(self, font=("Arial", 12), width=40)
        self.security_question_entry.pack(pady=10)

        tk.Label(self, text="Security Answer:", font=("Arial", 14), bg="#040405", fg="white").pack(pady=10)
        self.security_answer_entry = tk.Entry(self, font=("Arial", 12), width=40)
        self.security_answer_entry.pack(pady=10)

        tk.Button(self, text="Register", command=self.register, font=("Arial", 14, "bold"), bg="#2ecc71", fg="white",
                  relief=tk.GROOVE, width=20).pack(pady=20)

        self.error_message_var = tk.StringVar()
        self.error_message_label = tk.Label(self, textvariable=self.error_message_var, font=("Arial", 12), fg="red",
                                            bg="#040405")
        self.error_message_label.pack(side=tk.TOP, pady=6)

        self.success_message_var = tk.StringVar()
        self.success_message_label = tk.Label(self, textvariable=self.success_message_var, font=("Arial", 12),
                                              fg="green", bg="#040405")
        self.success_message_label.pack(side=tk.TOP, pady=6)

    def password_eye(self):
        current_show_state = self.password_entry.cget("show")
        if current_show_state:
            show_char = ""
        else:
            show_char = "*"
        if current_show_state:
            show_image = self.hide_image
        else:
            show_image = self.show_image
        self.show_hide_button.configure(image=show_image)
        self.password_entry.configure(show=show_char)

    def register(self):
        fullname = self.fullname_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        security_question = self.security_question_entry.get()
        security_answer = self.security_answer_entry.get()
        favorite_genre = self.favorite_genre_entry.get()

        def clear_error_message():
            self.error_message_var.set("")

        if not (fullname and username and password and security_question and security_answer and favorite_genre):
            self.error_message_var.set('Please fill in all fields to create the account.')
            self.after(2000, clear_error_message)
            return

        if favorite_genre not in self.ALLOWED_GENRES:
            self.error_message_var.set('Invalid genre. Please choose from the allowed genres.')
            self.after(2000, clear_error_message)
            return

        new_user = {
            'fullname': fullname,
            'username': username,
            'password': password,
            'security_question': security_question,
            'security_answer': security_answer,
            'favorite_genre': favorite_genre,
        }
        users = UserManagement.load_data(USER_DATA_FILE)
        users.append(new_user)
        UserManagement.save_data(users, USER_DATA_FILE)
        self.success_message_var.set("Your account was successfully created")
        self.after(2000, self.destroy)


class RecommendationMenu(tk.Toplevel):
    def __init__(self, parent, movies, user_preferences):
        tk.Toplevel.__init__(self, parent)
        self.title("Movie Recommendations")
        self.geometry("1000x600")
        self.configure(bg="#040405")

        tk.Label(self, text="Recommended Movies", font=("Arial", 16, "bold"), bg="#040405", fg="white").pack(pady=10)
        self.recommendations_label = tk.Label(self, text="", font=("Arial", 12), bg="#040405", fg="white")
        self.recommendations_label.pack(pady=10)
        self.movies = movies
        tk.Button(self, text="Back to Menu", command=self.destroy, font=("Arial", 12), bg="#e74c3c", fg="white",
                  relief=tk.GROOVE).pack(pady=30)

        self.user_preferences = user_preferences

    def set_recommendations(self):
        recommendations = self.get_recommendations()
        if recommendations:
            recommendations_text = "\n\n\n\n".join(recommendations)
            self.recommendations_label.config(text=recommendations_text)
        else:
            self.recommendations_label.config(text="No recommendations available.")

    def get_recommendations(self):
        user_favorite_genre = self.user_preferences.get('favorite_genre', '')

        genre_filtered_movies = []
        for movie in self.movies:
            movie_info = movie.split(';')
            if len(movie_info) > 2 and user_favorite_genre.lower() in movie_info[2].lower():
                genre_filtered_movies.append(movie)

        return genre_filtered_movies[:5]


class ManageMoviesMenu(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Manage Movies")
        self.geometry("1000x600")
        self.configure(bg="#040405")
        self.parent = parent
        self.movies = UserManagement.get_movies()

        self.movies_listbox = tk.Listbox(self, selectmode=tk.SINGLE, font=("Arial", 12), bg="#040405", fg="white",
                                         height=27, width=150)
        self.movies_listbox.pack(pady=5, padx=20, fill=tk.BOTH)

        button_frame = tk.Frame(self, bg="#040405")
        button_frame.pack(pady=(10, 10))

        tk.Button(button_frame, text="Back to Menu", command=self.back_to_menu, font=("Arial", 12),
                  bg="#e74c3c", fg="white", relief=tk.GROOVE, width=20).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Add Movie", command=self.add_movie, font=("Arial", 12), bg="#3498db", fg="white",
                  relief=tk.GROOVE, width=20).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Delete Movie", command=self.delete_movie, font=("Arial", 12),
                  bg="#3498db", fg="white", relief=tk.GROOVE, width=20).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Edit Movie", command=self.edit_movie, font=("Arial", 12),
                  bg="#3498db", fg="white", relief=tk.GROOVE, width=20).pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(self, text="", fg="green", bg="#040405")
        self.status_label.pack()
        self.load_movies_from_file()

    def add_movie(self):
        add_movie_dialog = tk.Toplevel(self)
        add_movie_dialog.title("Add Movie")
        add_movie_dialog.geometry("500x350")
        add_movie_dialog.configure(bg="#040405")

        tk.Label(add_movie_dialog, text="Movie Title:", fg="white", bg="#040405").pack(pady=5)
        title_entry = tk.Entry(add_movie_dialog, width=40)
        title_entry.pack(pady=5)

        tk.Label(add_movie_dialog, text="Release Year:", fg="white", bg="#040405").pack(pady=5)
        year_entry = tk.Entry(add_movie_dialog, width=40)
        year_entry.pack(pady=5)

        tk.Label(add_movie_dialog, text="Genre:", fg="white", bg="#040405").pack(pady=5)
        genre_entry = tk.Entry(add_movie_dialog, width=40)
        genre_entry.pack(pady=5)

        tk.Label(add_movie_dialog, text="Cast:", fg="white", bg="#040405").pack(pady=5)
        cast_entry = tk.Entry(add_movie_dialog, width=40)
        cast_entry.pack(pady=5)

        tk.Button(add_movie_dialog, text="Submit",
                  command=lambda: self.add_movie_to_file(title_entry.get(), year_entry.get(),
                                                         genre_entry.get(), cast_entry.get()),
                  font=("Arial", 12), bg="#2ecc71", fg="white", relief=tk.GROOVE, width=15).pack(pady=10)

    def add_movie_to_file(self, title, genre, year, cast):
        title = title.strip()
        genre = genre.strip()
        year = year.strip()
        cast = cast.strip()
        if not all((title, genre, year, cast)):
            self.show_error("Please fill in all fields.")
            return False
        with open(MOVIE_DATA_FILE, "r") as file:
            lines = file.readlines()
            for line in lines:
                if title.lower() in line.lower():
                    self.show_error("Movie already exists.")
                    return False
        with open(MOVIE_DATA_FILE, "a") as file:
            file.write(f"{title};{genre};{year};{cast}\n")
        self.movies_listbox.insert(tk.END, f"{title};{genre};{year};{cast}")
        self.show_status("Movie added successfully.")
        return True

    def delete_movie(self):
        selected_index = self.movies_listbox.curselection()
        if not selected_index:
            self.show_error("Please select a movie to delete.")
            return
        selected_movie_details = self.movies_listbox.get(selected_index)
        self.movies_listbox.delete(selected_index)
        selected_movie_title = selected_movie_details.split(';')[0]
        self.delete_movie_from_file(selected_movie_details)
        self.show_status(f"{selected_movie_title} deleted successfully.")

    @staticmethod
    def delete_movie_from_file(selected_movie):
        with open(MOVIE_DATA_FILE, "r") as file:
            lines = file.readlines()
        updated_lines = []
        for line in lines:
            if selected_movie not in line:
                updated_lines.append(line)
        with open(MOVIE_DATA_FILE, "w") as file:
            file.writelines(updated_lines)

    def load_movies_from_file(self):
        with open(MOVIE_DATA_FILE, "r") as file:
            movie_data = file.readlines()
        for movie in movie_data:
            self.movies_listbox.insert(tk.END, movie.strip())

    def edit_movie(self):
        selected_index = self.movies_listbox.curselection()
        if not selected_index:
            self.show_error("Please select a movie to edit.")
            return

        selected_movie = self.movies_listbox.get(selected_index)
        edit_movie_dialog = tk.Toplevel(self)
        edit_movie_dialog.title("Edit Movie")
        edit_movie_dialog.geometry("500x350")
        edit_movie_dialog.configure(bg="#040405")
        selected_movie_details = selected_movie.split(';')
        if len(selected_movie_details) > 3:
            current_title, current_year, current_genre, current_cast = selected_movie_details[:4]
        else:
            current_title, current_genre, current_year, current_cast = selected_movie_details

        def submit_movie(index=selected_index[0]):
            new_title = title_entry.get()
            new_genre = genre_entry.get()
            new_year = year_entry.get()
            new_cast = cast_entry.get()
            updated_movie = f"{new_title};{new_genre};{new_year};{new_cast}"
            self.movies_listbox.delete(index)
            self.movies_listbox.insert(index, updated_movie)
            if 0 <= index < len(self.movies):
                self.movies[index] = updated_movie
                with open(MOVIE_DATA_FILE, "w") as file:
                    for movie in self.movies:
                        file.write(f"{movie}\n")
                self.show_status(f"{selected_movie.split(';')[0]} edited successfully.")
                edit_movie_dialog.destroy()
            else:
                self.show_error("Invalid index for movie list.")

        tk.Label(edit_movie_dialog, text="New Movie Title:", fg="white", bg="#040405").pack(pady=5)
        title_entry = tk.Entry(edit_movie_dialog, width=40)  # Increased entry field width
        title_entry.insert(tk.END, current_title)
        title_entry.pack(pady=5)

        tk.Label(edit_movie_dialog, text="New Genre:", fg="white", bg="#040405").pack(pady=5)
        genre_entry = tk.Entry(edit_movie_dialog, width=40)  # Increased entry field width
        genre_entry.insert(tk.END, current_genre)
        genre_entry.pack(pady=5)

        tk.Label(edit_movie_dialog, text="New Release Year:", fg="white", bg="#040405").pack(pady=5)
        year_entry = tk.Entry(edit_movie_dialog, width=40)  # Increased entry field width
        year_entry.insert(tk.END, current_year)
        year_entry.pack(pady=5)

        tk.Label(edit_movie_dialog, text="New Cast:", fg="white", bg="#040405").pack(pady=5)
        cast_entry = tk.Entry(edit_movie_dialog, width=40)
        cast_entry.insert(tk.END, current_cast)
        cast_entry.pack(pady=5)

        tk.Button(edit_movie_dialog, text="Submit", command=submit_movie, bg="#2ecc71", fg="white",
                  relief=tk.GROOVE, width=15, font=("Arial", 12)).pack(pady=10)

        status_label = tk.Label(edit_movie_dialog, text="", font=("Arial", 12), fg="green", bg="#040405")
        status_label.pack(pady=5)

    def back_to_menu(self):
        self.destroy()

    def show_status(self, message):
        self.status_label.config(text=message, fg="green", font=("Arial", 10))

    def show_error(self, message):
        self.status_label.config(text=message, fg="red", font=("Arial", 10))


class ManageUserMenu(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Manage Users")
        self.geometry("800x400")
        self.configure(bg="#040405")
        self.parent = parent

        self.users = UserManagement.load_data(USER_DATA_FILE)
        title_label = tk.Label(self, text="Current Users", font=("Arial", 16, "bold"), bg="#040405", fg="white")
        title_label.pack(pady=10)

        self.listbox = tk.Listbox(self, selectmode=tk.SINGLE, font=("Arial", 12), bg="black", fg="white", height=10,
                                  width=50, highlightbackground="white")  # Adjusted Listbox width
        self.update_user_listbox()
        self.listbox.pack(pady=10)

        button_frame = tk.Frame(self, bg="#040405")
        tk.Button(button_frame, text="Back to Menu", command=self.destroy, font=("Arial", 12), bg="#e74c3c", fg="white",
                  relief=tk.GROOVE, width=15).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="Delete User", command=self.delete_user, font=("Arial", 12), bg="#3498db",
                  fg="white", relief=tk.GROOVE, width=15).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="View Details", command=self.view_user_details, font=("Arial", 12), bg="#3498db",
                  fg="white", relief=tk.GROOVE, width=15).pack(side=tk.LEFT, padx=5)
        button_frame.pack(pady=10)

        self.status_label = tk.Label(self, text="", font=("Arial", 12), fg="#e74c3c", bg="#040405")
        self.status_label.pack(pady=5)

    def update_user_listbox(self):
        self.listbox.delete(0, tk.END)
        for user in self.users:
            padding = f"{user['username']:^110}"
            self.listbox.insert(tk.END, padding)

    def delete_user(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_user = self.users[selected_index[0]]
            username = selected_user.get('username')
            self.users.remove(selected_user)
            UserManagement.save_data(self.users, USER_DATA_FILE)
            self.update_user_listbox()
            self.status_label.config(text=f"{username} deleted successfully.")
        else:
            self.status_label.config(text="Please select a user to delete.")

    def view_user_details(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_user = self.users[selected_index[0]]
            full_name = selected_user.get('fullname', 'N/A')
            details_dialog = tk.Toplevel(self)
            details_dialog.title("User Details")
            details_dialog.geometry("400x300")
            details_dialog.configure(bg="#040405")
            tk.Label(details_dialog, text=f"Username: {selected_user.get('username', 'N/A')}", font=("Arial", 12),
                     bg="#040405", fg="white").pack(pady=5)

            tk.Label(details_dialog, text=f"Full Name: {full_name}", font=("Arial", 12), bg="#040405", fg="white").pack(
                pady=5)

            security_question = selected_user.get('security_question', 'N/A')
            tk.Label(details_dialog, text=f"Security Question: {security_question}", font=("Arial", 12),
                     bg="#040405", fg="white").pack(pady=5)

            favorite_genre = selected_user.get('favorite_genre', 'N/A')
            tk.Label(details_dialog, text=f"Favorite Genre: {favorite_genre}", font=("Arial", 12),
                     bg="#040405", fg="white").pack(pady=5)

            watchlist_label = tk.Label(details_dialog, text="Watchlist:", font=("Arial", 14, "bold"), bg="#040405",
                                       fg="white")
            watchlist_label.pack(pady=10)

            watchlist_listbox = tk.Listbox(details_dialog, selectmode=tk.SINGLE, font=("Arial", 12), bg="black",
                                           fg="white",
                                           selectbackground="white", height=5, width=40, highlightbackground="white")
            watchlist_listbox.pack(pady=10)
            watchlist = selected_user.get('watchlist', [])
            for movie in watchlist:
                watchlist_listbox.insert(tk.END, movie)
        else:
            self.status_label.config(text="Please select a user to view details.")


class Main(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('1200x800')
        self.resizable(False, False)
        self.title("Movie Management System (Haroon Maqbool)")
        self.movies = UserManagement.get_movies()
        self.message_var = tk.StringVar()
        self.current_user = None
        self.manage_movies_button = None
        self.manage_users_button = None
        self.watchlist_button = None
        self.search_button = None
        self.rate_button = None
        self.recommend_button = None
        self.logout_button = None
        self.welcome_displayed = False

        background_frame = Image.open('background.png')
        background_frame = background_frame.resize((1200, 800))
        picture = ImageTk.PhotoImage(background_frame)
        self.background = tk.Label(self, image=picture)
        self.background.image = picture
        self.background.pack(fill='both', expand=True)

        # Login Frame
        self.login_frame = tk.Frame(bg='#040405', width=800, height=600)
        self.login_frame.place(x=200, y=100)

        # Logo Image
        logo_image = Image.open('logo.png')
        logo_image = logo_image.resize((105, 105))
        logo = ImageTk.PhotoImage(logo_image)
        self.logo_label = tk.Label(self.login_frame, image=logo, bg='#040405')
        self.logo_label.image = logo
        self.logo_label.place(x=35, y=20)

        # Heading
        self.heading = tk.Label(self.login_frame, text="Movie Management System", font=('yu gothic ui', 25, "bold"),
                                bg="#040405", fg='red', bd=5)
        self.heading.place(x=190, y=15, width=450, height=60)

        # Sign In Label
        self.sign_in_label = tk.Label(self.login_frame, text="Sign In", bg="#040405", fg="white",
                                      font=("yu gothic ui", 18, "bold"))
        self.sign_in_label.place(x=370, y=100)

        # Username
        self.username_label = tk.Label(self.login_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                       font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=260, y=200)

        self.username_entry = tk.Entry(self.login_frame, relief=tk.FLAT, bg="#040405", fg="#6b6a69",
                                       font=("yu gothic ui ", 12, "bold"), insertbackground='#6b6a69')
        self.username_entry.place(x=290, y=243, width=270)

        self.username_line = tk.Canvas(self.login_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=262, y=266)

        self.username_icon = Image.open('username_icon.png')
        picture = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = tk.Label(self.login_frame, image=picture, bg='#040405')
        self.username_icon_label.image = picture
        self.username_icon_label.place(x=260, y=240)

        # Password
        self.password_label = tk.Label(self.login_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                       font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=260, y=300)

        self.password_entry = tk.Entry(self.login_frame, highlightthickness=0, relief=tk.FLAT, bg="#040405",
                                       fg="#6b6a69", font=("yu gothic ui", 12, "bold"), show="*",
                                       insertbackground='#6b6a69')
        self.password_entry.place(x=290, y=343, width=270)

        self.password_line = tk.Canvas(self.login_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=262, y=366)

        # Password icon
        self.password_icon = Image.open('password_icon.png')
        picture = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = tk.Label(self.login_frame, image=picture, bg='#040405')
        self.password_icon_label.image = picture
        self.password_icon_label.place(x=260, y=340)

        # Login button
        self.login_button = Image.open('login.png')
        picture = ImageTk.PhotoImage(self.login_button)
        self.login_button_label = tk.Label(self.login_frame, image=picture, bg='#040405')
        self.login_button_label.image = picture
        self.login_button_label.place(x=260, y=413)

        self.login_button = tk.Button(self.login_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"),
                                      width=25, bd=0,
                                      bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',
                                      command=self.login)
        self.login_button.place(x=20, y=10)

        # Show/Hide Password
        self.show_image = ImageTk.PhotoImage(file='show.png')
        self.hide_image = ImageTk.PhotoImage(file='hide.png')

        self.show_button = tk.Button(self.login_frame, image=self.show_image, command=self.show,
                                     activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=545, y=347)

        self.hide_button = tk.Button(self.login_frame, image=self.show_image, command=self.show,
                                     activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=545, y=347)

        # Forgot password button
        self.forgot_button = tk.Button(self.login_frame, text="Forgot Password ?",
                                       font=("yu gothic ui", 11, "bold underline"),
                                       fg="white", activebackground="#040405", borderwidth=0, background="#040405",
                                       cursor="hand2", command=self.forget_password)

        self.forgot_button.place(x=341, y=480)

        # Sign Up button
        self.sign_label = tk.Label(self.login_frame, text='No account yet?', font=("yu gothic ui", 11, "bold"),
                                   borderwidth=0, background="#040405", fg='white')
        self.sign_label.place(x=270, y=540)
        self.signup_button = tk.Button(self.login_frame, text="Sign Up",
                                       font=("yu gothic ui", 11, "bold underline"), fg="white",
                                       activebackground="#040405", borderwidth=0, background="#040405",
                                       cursor="hand2", command=self.show_register)
        self.signup_button.place(x=436, y=536)

    def show(self):
        self.show_button = tk.Button(self.login_frame, image=self.hide_image, command=self.hide,
                                     activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=545, y=347)
        self.password_entry.config(show='')

    def hide(self):
        self.hide_button = tk.Button(self.login_frame, image=self.show_image, command=self.show,
                                     activebackground="white", borderwidth=0, background="white", cursor="hand2")
        self.hide_button.place(x=545, y=347)
        self.password_entry.config(show='*')

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            self.current_user = {'username': 'admin', 'role': 'admin'}
            self.login_frame.pack_forget()
            self.display()
        else:
            user_management = UserManagement()
            user = user_management.login_user(username, password)
            if user:
                self.current_user = user
                self.current_user.setdefault('watchlist', [])
                self.login_frame.pack_forget()
                self.display()
            else:
                error_label = tk.Label(self, text="Incorrect username or password. Please try again.",
                                       font=("Arial", 10), fg="red", bg="#040405")
                error_label.place(x=464, y=487)
                self.after(3000, lambda: error_label.destroy())

    def forget_password(self):
        username = self.username_entry.get()
        users = UserManagement.load_data(USER_DATA_FILE)
        user_data = None
        for user in users:
            if user['username'] == username:
                user_data = user
                break
        if not user_data or 'security_question' not in user_data:
            return

        security_question = user_data['security_question']
        forget_password_dialog = tk.Toplevel(self)
        forget_password_dialog.title("Forgot Password")
        forget_password_dialog.geometry("400x250")
        forget_password_dialog.configure(bg="#040405")

        answer_entry_label = tk.Label(forget_password_dialog, text="Your Question:", font=("Arial", 10), fg="white",
                                      bg="#040405")
        answer_entry_label.pack(pady=5)

        tk.Label(forget_password_dialog, text=security_question, font=("Arial", 10), fg="white", bg="#040405").pack(
            pady=10)

        answer_entry_label = tk.Label(forget_password_dialog, text="Your Answer:", font=("Arial", 10), fg="white",
                                      bg="#040405")
        answer_entry_label.pack(pady=5)

        answer_entry = tk.Entry(forget_password_dialog, show="*", width=30)
        answer_entry.pack(pady=5)

        tk.Button(forget_password_dialog, text="Verify",
                  command=lambda: self.confirm_security_question(answer_entry.get(), user_data, forget_password_dialog),
                  bg="#3498db", fg="white", relief=tk.GROOVE, width=15, font=("Arial", 12)).pack(pady=10)

    def confirm_security_question(self, user_answer, user_data, dialog):
        correct_answer = user_data.get('security_answer', '')

        if user_answer.lower() == correct_answer.lower():
            self.new_password(user_data, dialog)
        else:
            error_label = tk.Label(dialog, text="Incorrect Answer. Please try again.", font=("Arial", 10), fg="red",
                                   bg="#040405")
            error_label.pack(pady=10)
            self.after(3000, lambda: error_label.destroy())

    def new_password(self, user_data, dialog):
        dialog.destroy()
        new_password_dialog = tk.Toplevel(self)
        new_password_dialog.title("New Password")
        new_password_dialog.geometry("400x180")
        new_password_dialog.configure(bg="#040405")

        new_password_label = tk.Label(new_password_dialog, text="New Password:", font=("Arial", 10), fg="white",
                                      bg="#040405")
        new_password_label.pack(pady=5)

        new_password_entry = tk.Entry(new_password_dialog, width=30)
        new_password_entry.pack(pady=5)

        tk.Button(new_password_dialog, text="Submit",
                  command=lambda: self.update_password(new_password_entry.get(), user_data, new_password_dialog),
                  bg="#2ecc71", fg="white", relief=tk.GROOVE, width=15, font=("Arial", 12)).pack(pady=10)

    def update_password(self, new_password, user_data, dialog):
        if new_password:
            users = UserManagement.load_data(USER_DATA_FILE)

            for user in users:
                if user['username'] == user_data['username']:
                    user['password'] = new_password
                    UserManagement.save_data(users, USER_DATA_FILE)
                    success_label = tk.Label(dialog,
                                             text="Password Update: Your password has been updated successfully.",
                                             bg="#040405",
                                             font=("Arial", 10), fg="green")
                    success_label.pack(pady=10)
                    self.after(3000, lambda: success_label.destroy())
                    dialog.destroy()
                    return
        error_label = tk.Label(dialog, text="Empty New Password. Please try again.", font=("Arial", 10), fg="red",
                               bg="#040405")
        error_label.pack(pady=10)
        self.after(3000, lambda: error_label.destroy())

    def display(self):
        menu_window = tk.Toplevel(self)
        menu_window.geometry('1000x600')
        menu_window.configure(bg="#040405")
        menu_window.title('Movie')

        if not self.welcome_displayed:
            welcome_message = f"Welcome, {self.current_user['username']}!"
            tk.Label(menu_window, text=welcome_message, font=("Arial", 16, "bold"), bg="#040405", fg="white").pack(
                pady=20)
            self.welcome_displayed = True

        if self.current_user and self.current_user.get('role') == 'admin':
            tk.Button(menu_window, text="Manage Movies", command=self.manage_movies,
                      font=("Arial", 14), bg="#3498db", fg="white", relief=tk.GROOVE,
                      width=40).pack(pady=15)

            tk.Button(menu_window, text="Manage Users", command=self.manage_users,
                      font=("Arial", 14), bg="#3498db", fg="white", relief=tk.GROOVE,
                      width=40).pack(pady=15)

            tk.Button(menu_window, text="Logout", command=self.logout, font=("Arial", 14),
                      bg="#e74c3c", fg="white", relief=tk.GROOVE, width=40).pack(pady=15)

        else:
            tk.Button(menu_window, text="Search and Filter Movies", command=self.show_movies, font=("Arial", 14),
                      bg="#3498db", fg="white", relief=tk.GROOVE, width=40).pack(pady=15)

            tk.Button(menu_window, text="Rate and Review Movies", command=self.show_rating_and_review,
                      font=("Arial", 14), bg="#3498db", fg="white", relief=tk.GROOVE, width=40).pack(pady=15)

            tk.Button(menu_window, text="Get Movie Recommendations", command=self.show_recommendation,
                      font=("Arial", 14), bg="#3498db", fg="white", relief=tk.GROOVE, width=40).pack(pady=15)

            tk.Button(menu_window, text="Show Watchlist", command=self.show_watchlist, font=("Arial", 14),
                      bg="#3498db", fg="white", relief=tk.GROOVE, width=40).pack(pady=15)

            tk.Button(menu_window, text="Logout", command=self.logout, font=("Arial", 14), bg="#e74c3c", fg="white",
                      relief=tk.GROOVE, width=40).pack(pady=15)

    def logout(self):
        self.destroy()

    def show_movies(self):
        movies_dialog = FilterSortMenu(self, self.movies)
        self.wait_window(movies_dialog)

    def show_register(self):
        RegisterWindow(self)

    def show_rating_and_review(self):
        predefined_movies = UserManagement.get_movies()
        rate_review_dialog = RatingMenu(self, predefined_movies)
        self.wait_window(rate_review_dialog)

    def show_recommendation(self):
        if self.current_user and 'username' in self.current_user:
            username = self.current_user['username']
            users = UserManagement.load_data(USER_DATA_FILE)
            user_preferences = {}
            for user in users:
                if user['username'] == username:
                    user_preferences = user
                    break
            recommendations_dialog = RecommendationMenu(self, self.movies, user_preferences)
            recommendations_dialog.set_recommendations()
            self.wait_window(recommendations_dialog)

    def show_watchlist(self):
        if self.current_user and 'watchlist' in self.current_user:
            watchlist_dialog = WatchListMenu(self, self.current_user['watchlist'])
            self.wait_window(watchlist_dialog)

            users = UserManagement.load_data(USER_DATA_FILE)
            for user in users:
                if user['username'] == self.current_user['username']:
                    user['watchlist'] = self.current_user['watchlist']
                    UserManagement.save_data(users, USER_DATA_FILE)
                    break

    def manage_movies(self):
        movies_management_dialog = ManageMoviesMenu(self)
        self.wait_window(movies_management_dialog)

    def manage_users(self):
        users_management_dialog = ManageUserMenu(self)
        self.wait_window(users_management_dialog)


MovieManagementSystem = Main()
MovieManagementSystem.mainloop()
