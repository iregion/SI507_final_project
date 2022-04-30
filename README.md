# SI507_final_project
Destiny2 perk searcher v1.0

So far, it supports two languages, English and Chinese.

d2manifest.py is for the reqeust URL and cache the data. The API-key is also in this file and it can be directly used after downloading. But you still can use your own bungie API-key if you have one. Part of the code in it is the demo code from Bungie wiki. The link is https://github.com/vpzed/Destiny2-API-Info-wiki

final_project.py is the main part of code. It extracts the data by sqlite3 and then process and reorganize the data. The user interface is also in it.

The first time running will consume a little bit longer. It needs to download a 150MB SQL database.




