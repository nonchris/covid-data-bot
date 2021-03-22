# covid-update-telegram-bot
This bot sends automated updates via telegram, when new covid-numbers are published on the local website.

## Functions
* Choose which locations you want to be updated about
* Get graphs on demand using `show (location)`

### Process
To do this the bot excecutes the following steps:  
* requests the latest covid-19 numbers from the specified website
* reads html table and fits it into a json if data is from 'today'
* generates data tables using the saved jsons and `pandas`
* creates plots for each location from those tables
* automatical dispatch of the generated images to those who are subscribed

### Note
The whole process is written to handle data from the _Kreis Ahrweiler_ in Rheinland-Pfalz, Germany.  
This is also why the bots output is in german.  
It might be simpler to write a new bot than porting this to you local governments website.  
But feel free to copy some blocks of code you like, as long as your code stays open source :)
