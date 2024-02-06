# CS50Movie
#### Video Demo:  <https://youtu.be/FvmRyu9_rSc>
#### Description:

### CS50
This is my final project for CS50x, introduction to programming course
### Built With:
        Flask
        Bootstrap
        SQLite3
        CS50
I've used flask web framework based in on Python, and have used SQLite3 to manage SQL data and some helper functions provided by CS50

### API used:

The webpage use OMDb API to fetch details about the movies.
OMDb link: https://www.omdbapi.com/


## Explaining the project

My final projecct is a movie searching website that allows user to search for any movie and get basic detail about it. The users can also add and remove movie from their watchlist, to do that they need to have an account.

All informations about users, and their watchlist is stored in cinema.db

### How the webpage works?

Users can search for any movies without having an account. They only need an account if they want to use the watchlist funtionality.

The search bar lets user search for any name and gives them the list of movies/series matching that name if any exist.
From there user can open the desired result and see more details about it. The details page give small detail about the plot and names of writer, director and actors as well as other basic details and also the poster of that movie.

#### User Account

If the user wishes to use the watchlist feature, then they must login first.
The user is given to option to login, first, direct login if they already have registered themselves, if they've not then they can create a new account and register themselves. The account creation is very simple. All they need to do is provide a unique username and password, they also need to confirm their password. After successfully registering they'll be able to use they watchlist funtion.

User password is encrypted and stored as hash in the database

Two users cannot have same username.


#### Searching

All the user need to do is enter a valid name in search bar, the name will then be matched with movies in the OMDb database using an API call, all the movies matching the name will be then show on the result page. The user can open details page for any given result. The result page contains all the basic details about the movie and has a poster and title for it. From that screen user, if they're logged in, can choose to add the movie to their watchlist.

#### Watchlist

Watchlist contains a list of all the movie that the user has added to their watchlist. They are sorted in time of adding order. They also have an option to delete any movie from their watchlist. The user can also directly go to the movie details page from watchlist when they click on the movie title in the page.