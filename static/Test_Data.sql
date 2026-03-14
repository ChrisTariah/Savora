-- Users
INSERT INTO User (ID, username, password, privilege)
VALUES 
(0, "Trevor", "password", "admin"),
(1, "All_Ingredients_Guy", "password", "premium"),
(2, "Some_Ingredients_Gal", "password", "premium"),
(3, "No_Ingredients_Man", "password", "premium");

-- Data from Trevor's gusto recipe collection --------------------------------------------
-- Recipes
-- No image links yet
INSERT INTO Recipe (ID, userID, name, instructions)
VALUES 
(1, 0, "Red Wine Pork Shoulder With Garlic Crushed Potatoes", 
"Instructions for 2 [for 3] [for 4]
Before you begin....
This recipe takes around 5-10 min to prep, so get your casserole dish and all your ingredients ready, then wash your fruit and veg
Note: Make sure your dish is oven-proof and safe to use on the hob. Don't have one? Start cooking in a large, wide-based pan then transfer to an oven-proof dish and cover tightly with foil
Now, let's get started!
Preheat the oven to 200°C/180°C (fan)/ gas 6 and boil a kettle Heat a large, wide-based hob-safe oven-proof casserole dish with a matching lid with a drizzle of vegetable oil over a high heat Once hot, add your diced pork shoulder with 1 tsp [11/2 tsp) [2 tsp) flour and cook for 2-3 min or until lightly browned
6
Meanwhile, chop your potatoes in half
Top, tail, peel and slice your carrot[s] into discs on the diagonal
Peel and chop your red onion[s] into wedges
Wash your shredded kale
Add the shredded kale to a large piece of tin foil with a generous splash of cold water and a large knob of butter
Scrunch the foll around the kale to form a tightly sealed parcel
Tip: Cooking for 3 or more? Make 2 separate parcels!
8
Once the pork is slightly browned, reduce the to high and add the onion wedges and carrot discs with your ground paprika, tomato paste and bay leaf(ves]
Add your chicken stock mix with your red wine paste and 400ml [500ml] [700ml] boiled water and bring to the bail over a high heat
Cover with the lid and put the dish in the oven for 55 min or until the sauce has thickened and the pork is cooked through - this is your red wine braised pork shoulder
Add the chopped potato to a baking tray (or two) with a large piece of tin foil, then drizzle over a large splash of boiled water Scrunch the foll around the potato to form a tightly sealed parcel
Tip: Cooking for 4 or more? Make 2 separate parcels!
Put the tray[s] in the oven for 55 min or until the potato is tender
4
Once the pork has had 45 min, remove the baking tray[s] from the oven, add the shredded kale foil parcel to the other side and return the tray(s) to the oven for 10-12 min or until the kale is tender
Once the potatoes are tender, remove the tray[s] from the oven and transfer the cooked potato to a heatproof bowl with your roasted garlic paste, a knob of butter and a pinch of salt and pepper, then crush lightly with a fork-these are your roasted garlic crushed potatoes
Discard the bay leaf[ves]
Serve the red wine braised pork shoulder with the roasted garlic crushed potatoes, and buttery shredded kale to the side Dig in!"),
(2, 0, "Baked Saffron, King Prawn & Pea Risotto With Lemon",
"Instructions for 2 (for 4)
Before you begin...
This recipe takes around 5 min (10 min) to prep, so get your casserole dish and all your ingredients ready, then wash your fruit and veg
Note: Make sure your dish is oven-proof and safe to use on the hob. Don't have one? Start cooking in a large, wide-based pan then transfer to an oven-proof dish and cover tightly with foll
Now, let's get started!
Preheat the oven to 200°C/180°C (fon)/gas 6
Boil a kettle
Heat a large, wide-based hob-safe oven-proof casserole dish with a matching lid with a drizzle of olive oil over a medium-high heat
5
Crush the garlic cloves open by squashing them with the side of a knife
Remove the skins and discard, then chop the garlic roughly
Add the chopped garlic, arborio rice and saffron to the dish and cook for 30 secs
7
Stir in the vegetable stock mix and add 550ml [1.11] boiled water
Bring to the boil over a high heat
Once boiling, cover with a lid and put the dish in the oven for an initial 20 min or until most of the water has absorbed and the rice is almost cooked
8
Use this time to clear up, set the table, have a cup of tea or simply chill
Drain the king prawns
After 20 min, remove the dish from the oven and add the drained king prawns, blanched peas and a small splash of water
Stir it all up, cover with the lid and return the dish to the oven for a further 8-10 min or until the prawns are cooked through
Once done, add the juice of 1/2 [1] lemon, half of the grated Italian hard cheese (save some for garnish!) and a grind of black pepper then stir it all up this is your oven-baked saffron, king prawn & pea risotto
Cut the remaining lemon into wedges
Wash the rocket, then pat it dry with kitchen paper
To serve, sprinkle the remaining grated Italian hard cheese all over the risotto and top with the rocket
Garnish with the lemon wedges, drizzle with some olive oil and season with a grind of black pepper Let everyone dig in");

-- Ingredient (alphabetical)
-- No API fields yet
INSERT INTO Ingredient (ID, name, unit_type)
VALUES 
-- Added with recipe 1
(1, "Bay leaf", "cnt"),
(2, "Carrot", "cnt"),
(3, "Chicken stock mix", "g"),
(4, "Garlic paste", "g"),
(5, "Kale", "g"),
(6, "Paprika", "tsp"),
(7, "Pork shoulder", "g"),
(8, "Potato", "cnt"),
(9, "Red Onion", "cnt"),
(10, "Red wine paste", "g"),
(11, "Tomato paste", "g"),
-- Added with recipe 2
(12, "Arborio rice", "g"),
(13, "Garlic cloves", "cnt"),
(14, "Italian hard cheese", "g"),
(15, "King prawns", "g"),
(16, "Lemon", "cnt"),
(17, "Peas", "g"),
(18, "Rocket", "g"),
(19, "Saffron", "cnt"),
(20, "Vegetable stock mix", "g"),
-- Not found in any recipe
(999, "Milk", "ml");

-- Ingredient Lines (by recipe)
INSERT INTO Ingredient_Line (recipeID, ingredientID, quantity)
VALUES
(1, 2, 1),
(1, 3, 5.5),
(1, 7, 250),
(1, 1, 2),
(1, 6, 1),
(1, 9, 1),
(1, 10, 10),
(1, 4, 15),
(1, 5, 120),
(1, 11, 32),
(1, 8, 3),
(2, 16, 1),
(2, 19, 1),
(2, 13, 2),
(2, 18, 20),
(2, 17, 160),
(2, 20, 11),
(2, 15, 171),
(2, 14, 30),
(2, 12, 160);

-- Fridge
INSERT INTO Fridge (userID, ingredientID, quantity)
VALUES
-- User with all ingredients for recipe 1
(1, 1, 999),
(1, 2, 999),
(1, 3, 999),
(1, 4, 999),
(1, 5, 999),
(1, 6, 999),
(1, 7, 999),
(1, 8, 999),
(1, 9, 999),
(1, 10, 999),
(1, 11, 999),
-- User with some ingredients for recipe 1
(2, 1, 999),
(2, 2, 999),
(2, 3, 999),
(2, 4, 999),
(2, 5, 0.1),
(2, 6, 0.1),
-- User with no ingredients for recipe 1
(3, 999, 999);