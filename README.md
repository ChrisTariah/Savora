# Savora
This is the GitHub repository for Savora, by The Hungry Coders.
## Database
The database is an SQLite local disk database created from scratch using the script [setup_database.py](./static/setup_database.py) and the file [Base_Schema.sql](./static/Base_Schema.sql). Within [setup_database.py](./static/setup_database.py) is the list of files that will be run to build the database. This list must always include [Base_Schema.sql](./static/Base_Schema.sql) and may include additional files to modify or populate the database such as [Test_Data.sql](./static/Test_Data.sql):
``` python
SQL_FILES = [
    "static/Base_Schema.sql",
    "static/Test_Data.sql" 
] 
```

Permanent changes to the database should be added to the [Base_Schema.sql](./static/Base_Schema.sql) file, rather than in a new separate file, but temporary changes for testing should remain in separate files and added to the SQL_FILE list in [setup_database.py](./static/setup_database.py).

#### Query Library
The file [Query_Library.sql](./static/Query_Library.sql) that has some queries that may be useful to the site, such as filtering by price or showing only recipes the user has ingredients for. More queries can be added by request. Note that each query will have a line with a comment stating where a variable should be used like:
``` sql
AND Fridge.userID = 1 -- Replace with desired user 
```
This is the search parameter or filter being applied and should be set by user interaction or account information (userID).

#### Query Database With A Terminal Session
The file [database_terminal_session.py](./database_terminal_session.py) will allow you to open the [Savora.db](./Savora.db) file and interact with it using SQLite commands for testing and development purposes.

#### Recipes Via API 
The file [get_recipes.py](./RecipeAPI/get_recipes.py) is a script that will pull recipes from a [free api](https://www.themealdb.com/) and add them to the database. The script checks for existing recipes before adding them, so it can be run at any point with no need to rebuild the database (unlike when running [setup_database.py](./static/setup_database.py)). This API is only free for non-commercial use. 
Currently the script can only parse about 50% of the 500 or so recipes. If more are needed this could be improved. However, the code is really quite bad. If the script will need frequent maintenance it would worthwhile to refactor the whole thing.

## Set Up
The following is a guide to setting up the project. Note that this only is confirmed to work in VS Code on Windows. As this project uses python to run the server, python will need to be [installed on your machine](https://www.python.org/downloads/).

### Dependencies
Once the repository is cloned several python libraries will need to be installed. To do this, first create a virtual environment by either running:
```Powershell
python -m venv .venv
```
or in VS Code opening the command pallet (ctrl+shift+P), selecting "Python: Select Interpreter" then "+ Create Virtual Environment", and using the most up to date version of python from those listed when prompted (at least 3.13.1). A .venv directory should now be in the root directory. If not automatically activated by VS Code (indicated by a <span style="color:green">(.venv)</span> before the prompt in the terminal), do so by running:
```Powershell
 .venv\Scripts\\.\Activate.ps1 
 ```
 If you get an error about not having permission to run scripts, enter the command: 
 ```Powershell
 set-executionpolicy remotesigned
 ```
 Lastly, install the dependencies by running:
 ```Powershell
 pip install -r requirements.txt
 ```
 Note that if you add new dependencies, you must add them to requirements by running:
 ```Powershell
 pip freeze > requirements.txt
 ```
 ### Running the Server
 Run the file server.py either by opening it in vs code or navigating to the Savora directory in the terminal and running:
 ```Powershell
 python server.py
 ```
 This will host the website on [localhost:8000](http://localhost:8000). Navigating to this in your browser or clicking the outputted link while holding control will bring you to the home page.
 ## Front End
 
### Overview
The front end is a multi-page vanilla HTML/CSS/JS application served as static files by `server.py`. All pages share a single stylesheet (`static/style.css`) and a set of shared JavaScript files.
 
### Pages
| File | Route | Description |
|---|---|---|
| `index.html` | `/static/index.html` | Home / landing page |
| `login.html` | `/static/login.html` | Login form |
| `register.html` | `/static/register.html` | Registration form |
| `forgot-password.html` | `/static/forgot-password.html` | Password reset request |
| `recipes.html` | `/static/recipes.html` | Recipe browser with search |
| `recipe.html` | `/static/recipe.html?id=N` | Single recipe detail view |
| `profile.html` | `/static/profile.html` | User profile, create recipe, fridge |
 
### JavaScript Files
| File | Purpose |
|---|---|
| `app.js` | Auth functions (`login`, `logout`, `registerUser`), shared `loadNavbar()`, shared `toggleChat()` |
| `ai.js` | AI chat widget — wires the chat button and handles sending/receiving messages |
| `recipes.js` | Fetches and renders all recipes; `filterRecipes()` handles client-side search |
| `recipe.js` | Fetches and renders a single recipe by `?id=` query param |
| `profile.js` | Recipe creation form, ingredient search autocomplete, fridge management |
| `script.js` | Legacy toggle/validation file (largely superseded by `app.js`) |
 
### Stylesheet (`style.css`)
The stylesheet uses CSS custom properties (variables) defined in `:root` for consistent theming:
```css
--orange, --orange-dark, --orange-light  /* primary brand colour */
--cream, --parchment                      /* background tones */
--text, --text-muted                      /* typography */
--card-bg, --border                       /* surfaces */
--shadow-sm, --shadow-md, --shadow-lg    /* elevation */
--radius, --radius-sm                     /* border radii */
--transition                              /* animation timing */
```
Google Fonts are loaded at the top of the stylesheet:
- **Playfair Display** (700, 900) — headings and the Savora wordmark
- **DM Sans** (400, 500, 600) — body copy and UI elements
 
### Navigation Bar
All pages include `<div class="nav" id="nav-links"></div>` inside `<header>`. The `loadNavbar()` function in `app.js` populates this div on `DOMContentLoaded` by hitting `/me`. It renders a logged-in or logged-out set of links automatically, so every page stays consistent without duplicating HTML.
 
Logged-out links: Home · Recipes · Login · **Register** (CTA pill)  
Logged-in links: Home · Recipes · Profile · **Logout** (CTA pill)
 
### Recipe Search
`recipes.html` includes a search input (`id="recipe-search"`). The `filterRecipes()` function in `recipes.js` filters the in-memory `allRecipes` array client-side — no additional server requests. It matches against both recipe **name** and **tags**, and shows a "no results" message when nothing matches.
 
### AI Chat Widget
The chat button (`id="ai-btn"`) and chat box (`id="ai-chat"`) are present on `recipes.html`, `recipe.html`, and `profile.html`. The toggle is handled by `toggleChat()` in `app.js`. Messages are sent to the `POST /chat` endpoint and displayed as styled bubbles. The Enter key also triggers sending.
 
### Design Notes
- The home page hero uses CSS `@keyframes fadeUp` with staggered `animation-delay` for a sequenced entrance effect.
- Floating food emoji decorations on the home page use `@keyframes floatBob` for a gentle floating motion.
- Recipe cards use a flex column layout so the "View Recipe" button always aligns to the bottom of each card regardless of content height.
- Tag pills are rendered as inline `<span class="tag-pill">` elements with an orange tint.
- The header uses `backdrop-filter: blur()` for a frosted-glass effect as you scroll past content.
 