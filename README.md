Pokemon API

This is This is a small program that lets you look at, add, change, and delete Pokemon data using an API.

There are 15 Pokemon in here that I typed in myself (Thank you sir Ian for teaching database), each one has a name, a type, and some stats (hp, attack, defense, speed).

How to run it on your computer

Download this project and unzip it if needed.
Open PowerShell on Windows and go into the project folder.
Type this and press enter, it installs the one thing this needs to run: pip install -r requirements.txt
Type this and press enter, it starts the program: python app.py
Then Leave that terminal open. Open the browser and go to: http://127.0.0.1:5000.

The methods and stuff (Backend)

To Get the full list of Pokemon Just visit or send a request to: http://127.0.0.1:5000/pokemon It gives you back all 15 Pokemon.

To Get one single Pokemon Add the id number to the end, like: http://127.0.0.1:5000/pokemon/1 It gives you back just that one.

To Add a new Pokemon You send a request with the new Pokemon's info (name, type, hp, attack, defense, speed) to http://127.0.0.1:5000/pokemon If you forget one of those pieces of info, it will tell you what's missing instead.

To Change an existing Pokemon You send a request to http://127.0.0.1:5000/pokemon/1 (or whatever id) with just the part you want to change, like just a new hp number.

To Delete a Pokemon You send a request to http://127.0.0.1:5000/pokemon/1 (or whatever id) and it removes that one from the list.

The codes it gives back When something works, it tells you 200. When you send bad info, like forgetting a field or something, it tells you 400. When you ask for a Pokemon id that doesn't exist, it tells you 404.

Methods (Frontend)
Follow the previous step except open the browser and go to: http://127.0.0.1:5000/static/index.html

The full list is displayed when opening the website.

To Add a Pokemon to the database, click the top right button saying add pokemon, insert the necessary values and click save changes.

To Change an existing Pokemon in the database, search for the pokemon using the search bar or manually look for it, click the edit button and change the values as needed and then click save changes.

To Delete a Pokemon in the database, click the delete button on your selected pokemon, A popup will appear asking confirmation if you want to delete it, press OK to delete it.


Note: The charizard and update.json are there because I can't use POST or PUT in curl to add or update it
