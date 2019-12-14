# SI_507_Final_Project
Project Overview:

The project scrapes data from the top level List of States Wikipedia page on demographics, then crawls 
onto the subsequent pages of each state given user desired state and scrapes information on the state
specific demographics. After this presentation of the data is through tabular, pie chart and x-y scatter 
plot.

1) Data source : Wikipedia of List of states for the demographic information - scraped
 User access: https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_Sta
tes
Data source: Wikipedia of each US state to obtain refined demographic information pertaining to each state - scraped
User access: https://en.wikipedia.org/wiki/+ "state of interest" - in the program this was done through - crawling onto the next page. 

2) Information needed to run the program: 
If the desired input is not known - just enter 'help' in lowercase and the different options will pop-up
Always close open plots or graphs prior to proceeding with new commands to ensure program runs smoothly
Ensure needed packages - pandas, numpy, matplotlib, lxml are downloaded and ready to go

3) Code Structure and vital functions:

The code is structured with first list declarations to ensure necessary lists are present (eg states_abbr 
is a list that stores states abbreviations, capital is a list that stores capital information for the 
specific state, total_area gives information on the total area for the specific state). Then function
1) overall_states() extracts the data of all the states from wikipedia and it stores, name, abbrevation, capital, established, capital, population using for loops to append the lists->important. 
The rest of thecode is divided into distinct functions with another important function 2) poptrend() serving to extract the historical information of population of a particular state. It takes the state abbrevation as an argument. It returns two lists. First list is named "hist_op", it is a list of list, here each inner data denotes the information of the state. Second list denotes the the header of the information extracted in the first list. 
Another vital function is popstats() which extracts the racial trends information of population of a particular state. This function takes the state abbrevation as argument. It returns two lists. First list is named "hist_op", it is a list of list, here each inner data denotes the information of the state. Second list denotes the the header of the information extracted in the first list.
Other functions like piechart, scatter_plot and plot_bar create the presentation visuals that show the data. 

4) User Guide:

The program begins with 'Enter Your command (help for instructions):'
Here, command is initially unknown so enter 'help'

The following options come up:
''' 1) Enter refresh to refresh the database.
    2) Enter info to display the information about all states.
    3) Enter poptrend<state_abbr> to display the population trends of a state.
    4) Enter popstats<state_abbr> to display the racial population trends of a state
    5) Enter exit to leave.
    Enter Your command (help for instructions):'''
If you want to refresh the database to obtain a fresh database table - enter 'refresh'
If you want to obtain tabulated info of all 50 US states enter 'info'
If you desire a Pie-chart of the specific state of interest's demographic distribution, enter the popstats <state abbreviation here>:
eg: 'popstats<AL>' for Pie chart of Alabama's population. It will also give you a table with the demographic
breakdown
If you desire to obtain a scatter plot of the specific state of interest's demographic distribution, enter the poptrend <state abbreviation here>:
eg: 'poptrend<AL>' for a scatter plot of Alabama's population over the years.
If you are done with the program and desire to exit and leave - enter 'exit' and it will bring you outside
of the program's environment. 