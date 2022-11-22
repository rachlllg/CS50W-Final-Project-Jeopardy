# CS50W - Final Project - Jeopardy
This is the final project for CS50's Web Programming with Python and Javascript class. I chose to create a web-based single-player jeopardy game where players can play jeopardy games and keep track of the score (no registration required). Players can also register and log-in which allows them to contribute to the database and create their own Jeopardy games for other people to play. The games are single-players only and only one person can play a game at a time, the games can be reset after each play. 

See link below to a Youtube video demonstrating the functionalities:
https://youtu.be/MF1RfGBrm8Y


## Distinctiveness and Complexity
This Jeopardy web-based game differs in nature from any other projects within the cource and drastically differs from social network or e-commerce. The game function is somewhat limited at the moment as it it single player only but I plan to continue improve it as I continue improving my skills.

#### Database:
The game utilizes django models in the backend to store the jeopardy games created by the admin or the logged-in users. There are four models in addition to the User model:

- Subject: This model stores all subjects any game could be based on, right now we have shows, movies, and sports. Only admin can create new subjects.

- Jeopardy: This model is the baseline to creating a new jeopardy game. The owner can select a subject (by using the foreignkey reference to Subject model) and assign a name to their game. The owner is auto-assigned based on the request user (by using the foreignkey reference to User model) and the creation date is also auto assigned within the model. Each game has a unique ID.

- Category: Once a new game has been created in the Jeopardy model, the owner can create up to 5 categories for that jeopardy game (by using the foreignkey reference to Jeopardy model). Each category must be unique and is assigned a unique ID.

- Question: Once the player has created the categorys for their game, they can add up to 5 clues, each with different clue values to that category (by using the foreignkey reference to Category model). Each clue contains the clue itself, the cluevalue (selected from dropdown), the answer, and 3 choices for players to select. At least one of the choices must match the answer and each clue must be unique and is assigned a unique ID.

#### Game play:
The home page shows all subjects the player may select, selecting a subject will take the player to the subject page where the player will be presented with all jeopardy games within the selected subject. Once the player select the game they wish to play, they will be taken to the game page where they are presented with the game, the score, and a reset button to reset the game. 

The player can play the game by selecting a cluevalue within a category which would render a pop-up clue card (using javascript) which shows the clue and the three choices for the player to choose, this clue clard is dynamically rendered using ajax by utilizing json to fetch the clue/choices from the django model within the same page as the game page (ie, same url), no refresh or redirect of the page occurs.

Once a clue is selected and the pop-up shows up, the player cannot select any other clues until the selected clue is answered. Once the clue is answered, the clues change to green or red to indicate the correct or wrong answers. If the player selected the correct answer (using json to fetch the player selection to compare to the answer stored in django model), the cluevalue for that clue will be added to the score on top and a close button is presented to the player so they may close the pop-up clue card. Once a clue has been answered, that clue turns to grey and if clicked on again, the pop-up clue card will show a message for the player to select a different clue so they cannot answer the same clue twice. 

Once the player is done playing, they can use the reset button to reset the game play so the game can be played again.

All style changes within the game play are achieved using javascript with the click eventlisteners.

Currently, the game only supports single player mode so only one player can play a game at a time. Any player can play the games, log-in is not required.

#### Contribute to database:
A player can choose to register and log-in in order to contribute to the database. They may click on the Contribute button on the main menu to contribute a new jeopardy game to the database for other players to play.

Once within the contribute menu, the user will be asked to select a subject and give their game a name. A subject must be selected and a game must have a unique name, the user is auto-assigned as the owner of the game and only the owner has the right to access the contribute pages for that particular game. 

Once the game has been added, the user is directed to the page to add categories to their game, a game can have up to 5 categories. Once a category is added, it show ups in the list within the page where the user may click on each category to add clues for that category.

Once the user is directed to the add clues page for the category selected, they may select a clue value and add the clue, answer, and three choices for that clue. Each category can have up to 5 clues, only one clue may be added for each clue value, each clue must be unique, and at least one of the choices must match the answer. Once a clue is successfully added, the clue along with all its information shows up in the list within the page where the user may keep track of the clues. The user can return to the category page to add more clues to other categories any time they wish.

If the user cannot finish building the game in one sitting, they may click on username's game button within the menu to be taken to their profile page where they are presented with all games owned by the user. The user may click on the game they wish to continue adding and be taken back to the contribute page for that game.

As soon as a game has been added by assigning a subject and name, the game becomes available in the game play. The game play is adjusted to accomodate the number of categories and clues the game has.


## What's contained in each file
Only the files which I made changes to are discussed here, the django files included as part of the django module to which I didn't make changes are not discussed here.

#### Django:
- README.md: Summarizes the details of the program and how to run the program
- urls.py: All urls for the program, including API routes for json data fetch for the game play
- models.py: All models to store the user and game information, see above on details for each model
- admin.py: Register the models with admin for admin to make neccessary changes to the models
- forms.py: Model forms derived from models to take new game contributions and store to models
- views.py: All python functions that takes the user requests and renders the requested pages or responds to the json requests

#### static:
- favicon.ico: Icon for the website
- script.js: All javascript functions that changes the display & information displayed based on user request, using eventlisteners and ajax
- styles.css: All styles to the website in addition to the default bootstrap styles utilized

#### templates: 
##### home page & game play:
- layout.html: Sets the overall layout of the website
- index.html: Home page of the website
- subject.html: Shows all jeopardy games for the requested subject
- jeopardy.html: Shows the jeopardy game play requested

##### user management:
- register.html: Allow user to register for an account in order to contribute to the database
- login.html: Allow registered users to log-in to their account in order to contribute to the database

##### contribute to database:
- add.html: Allow a logged-in user to add a new jeopardy game for the selected subject to Jeopardy model via NewJeopardyForm
- addcat.html: Allow a logged-in user to add new categories of the new jeopardy game to Category model via NewCategoryForm
- addques.html: Allow a logged-in user to add new clues to the new categories of the new jeopardy game to Question model via NewQuestionForm
- profile.html: A logged-in user may retrieve information regarding the games they contributed or continue a new contribution if not finished


## How to run the application
1. Clone the repo to local directory
2. Within the directory, install Django using: python3 -m pip install Django
3. Within the directory, run server using: python3 manage.py runserver
4. Open the development server

