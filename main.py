# Aditya Iyer SI 507 FINAL PROJECT
# importing necessary libraries.
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import sqlite3
from matplotlib import pyplot as plt
# initializing the list of all variables. These variables store the data of all the states.
states_name = []
states_abbr = []
capital = []
established = []
population = []
total_area = []
land_area = []
water_area = []
abbrUrl=[]
#Database Utilities
def checkBothTables(conn):
    sql_for_overall_table = ''' CREATE TABLE IF NOT EXISTS overall(
        state_name text,
        state_abbr text PRIMARY KEY,
        state_capital text,
        state_established int,
        state_population text,
        state_total_area text,
        state_land_area text,
        state_water_area text
    ); '''
    try:
        c = conn.cursor()
        c.execute(sql_for_overall_table)
    except ValueError:
        print("error")
    sql_for_link_table = """ CREATE TABLE IF NOT EXISTS links (
                                    state_abbr text PRIMARY KEY,
                                    link text,
                                    FOREIGN KEY (state_abbr) REFERENCES overall (state_abbr)
                                );"""
    try:
        c = conn.cursor()
        c.execute(sql_for_link_table)
    except ValueError:
        print("error")
    truncate_link_table = 'Delete from links where 1'
    try:
        c = conn.cursor()
        c.execute(truncate_link_table)
        conn.commit()
    except ValueError:
        print("error")
    truncate_overall_table = 'Delete from overall where 1'
    try:
        c = conn.cursor()
        c.execute(truncate_overall_table)
        conn.commit()
    except ValueError:
        print("error")
    conn.commit()
def create_connection(db_fie):
    conn = None
    try:
        conn = sqlite3.connect(db_fie)
    except ValueError:
        print("error")
    return conn

def create_overall_table(conn, overallData):
    cursor = conn.execute("SELECT state_abbr from overall where state_abbr ='"+ overallData[1] +"' ")
    if len(cursor.fetchall()) ==0:
        sql = ''' INSERT  INTO overall(state_name,state_abbr,state_capital,state_established,state_population,state_total_area,state_land_area,state_water_area) 
        VALUES(?,?,?,?,?,?,?,?)'''
        cur = conn.cursor()
        cur.execute(sql,overallData)
        conn.commit()
        return cur.lastrowid
    else:
        sql = "Update overall set state_name = '"+overallData[0] +"', state_capital = '"+overallData[2]+"', state_established = '"+overallData[3]+"',state_population = '"+overallData[4]+"',state_total_area = '"+overallData[5]+"',state_land_area = '"+overallData[6]+"',state_water_area  = '"+overallData[7]+"'  where state_abbr='"+overallData[1]+"' "
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        return cur.lastrowid
    
def create_links_table(conn,link):
    cursor = conn.execute("SELECT link from links where state_abbr = '"+ link[0]+"' ")
    cursor_result = cursor.fetchall()
    if len(cursor_result) ==0:
        sql = ''' INSERT  INTO links(state_abbr,link) 
        VALUES(?,?)'''
        cur = conn.cursor()
        cur.execute(sql,link)
        conn.commit()
        return cur.lastrowid
    else:
        sql = "update links set link = '"+link[1]+"'  where state_abbr = '"+link[0]+"'"
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        return cur.lastrowid
# This function is used to extract the data of all the states from wikipedia it stores, name, abbrevation, capital, established, capital, population
# and total area, land area, water area of all the states.
# It returns the list of lists named "to_return", Each element of the list denotes the data of a state.
def overall_states():
    global states_name
    global states_abbr
    global capital
    global established
    global population
    global total_area
    global land_area
    global water_area

    # Making the connection with the page, opening the url and creating the Beautiful soup object.
    page = urlopen('https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States')
    soup = bs(page, 'lxml')

    # Extracting the data.
    all_states = soup.find("table",class_ = "wikitable")
    states = all_states.find_all('tr')
    to_return = []
    j = 0

    # Iterating the list of all states.
    for each in states:
        if j != 0 and j != 1:
            row = []
            states_n= each.find_all('th')
            states_a = each.find_all('td')
            for i in states_n:
                states_name.append(i.text.strip().strip("[E]").strip("[F]").replace(" ","_"))
                row.append(i.text.strip())
                # print(i.find('a').get('href'))
                abbrUrl.append(i.find('a').get('href'))
            k = states_a
            if len(states_a) == 12:
                states_abbr.append(k[0].text.strip())
                capital.append(k[1].text.strip())
                established.append(k[3].text.strip())
                population.append(k[4].text.strip())
                total_area.append(k[6].text.strip())
                land_area.append(k[8].text.strip())
                water_area.append(k[10].text.strip())
                row.extend([k[0].text.strip(), k[1].text.strip(), k[3].text.strip(), k[4].text.strip(), k[6].text.strip(), k[8].text.strip(), k[10].text.strip()])
            elif len(states_a) == 11:
                states_abbr.append(k[0].text.strip())
                capital.append(k[1].text.strip())
                established.append(k[2].text.strip())
                population.append(k[3].text.strip())
                total_area.append(k[5].text.strip())
                land_area.append(k[7].text.strip())
                water_area.append(k[9].text.strip())
                row.extend([k[0].text.strip(), k[1].text.strip(), k[2].text.strip(), k[3].text.strip(), k[5].text.strip(), k[7].text.strip(), k[9].text.strip()])
            to_return.append(row)
        j += 1
    database = "sqlite.db"
    conn = create_connection(database)
    #with conn: #change this back
    checkBothTables(conn)
    for i in range (len(states_abbr)):
        newdata = (states_name[i], states_abbr[i], capital[i], established[i], population[i], total_area[i], land_area[i], water_area[i])
        create_overall_table(conn,newdata)
        linkdata = (states_abbr[i], 'https://en.wikipedia.org' + abbrUrl[i])
        create_links_table(conn,linkdata)
    return to_return


for i, j, k, l, m, n, o, p in zip(states_name, states_abbr, capital, established, population, total_area, land_area, water_area):
    print(i, j, k, l, m, n, o, p)

# This function is used to extract the historical information of population of a particular state.
# This function takes the state abbrevation as argument. It returns two lists.
# First list is named "hist_op", it is a list of list, here each inner data denotes the information of the state.
# Second list denotes the the header of the information extracted in the first list.
def poptrend(abbr):
    global states_name
    global states_abbr

    # Making the url requestl and opening the page.
    page = urlopen('https://en.wikipedia.org/wiki/List_of_states_and_territories_of_the_United_States')
    soup = bs(page, 'lxml')

    soup.find
    hist_pop = []
    ind = states_abbr.index(abbr)
    
    page = urlopen('https://en.wikipedia.org' + abbrUrl[ind])
    soup = bs(page, 'lxml')
    table = soup.find('table', class_= "toccolours")
    each_row = table.find_all('tr')
    i = 0
    length = len(each_row)
    for each in range(length):
        if i != 0:
            if i == 1:
                e = each_row[each].find_all('th')
                row_head = []
                for j in e:
                    if len(j.text.strip()) > 0:
                        row_head.append(j.text.strip())
            else:
                items = each_row[each].find_all('td')
                if each != length - 1 and each != length - 2:
                    row = []
                    for j in items[0]:
                        row.append(j.text)
                    row.append(items[1].text)
                    if items[3].text == "—":
                        row.append(0)
                    else:
                        row.append(items[3].text)
                    hist_pop.append(row)
        i += 1
    return hist_pop, row_head


# This function is used to extract the racial trends information of population of a particular state.
# This function takes the state abbrevation as argument. It returns two lists.
# First list is named "hist_op", it is a list of list, here each inner data denotes the information of the state.
# Second list denotes the the header of the information extracted in the first list.
def popstats(abbr):
    global states_name
    global states_abbr
    hist_pop = []
    row_head=[]
    ind = states_abbr.index(abbr)
    # Making the url requestl and opening the page.
    page = urlopen('https://en.wikipedia.org' + abbrUrl[ind])
    soup = bs(page, 'lxml')
    table = soup.find_all('table')
    for each_table in table:
        t = each_table.find('caption')
        if t:
            if "racial" in t.text.strip().lower():
                row_head = []
                head_tr = each_table.find('tr')
                head_th = head_tr.find_all('th')
                for each in enumerate(head_th):
                    if each[0] != 0:
                        row_head.append(str(each[1].text)[0:4])
                    else:
                        row_head.append(str(each[1].text))
                each_row = each_table.find_all('tbody')
                for each in each_row:
                    items = each.find_all('tr')
                    for k in items:
                        j = k.find_all('td')
                        if len(j) > 0:
                            row = []
                            for k in j:
                                if k.text.strip() == "—":
                                    row.append("0%")
                                else:
                                    row.append(k.text.strip())
                            hist_pop.append(row)
            continue     
    return hist_pop, row_head


#pie cahrt of racial breakdown of population of a state
def piechart(race_list, parameter_list, year):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = race_list
    sizes = parameter_list
    index = parameter_list.index(max(parameter_list))

    explode_list = []
    for i in range(len(labels)):
        if i != index:
            explode_list.append(0)
        else:
            explode_list.append(0.1)
    explode = tuple(explode_list)


    plt.axis('equal')

    # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Racial breakdown in '+ year + "\n\n\n\n")
    patches, texts = plt.pie(sizes, startangle=90, shadow=True)
    plt.legend(patches, labels, loc = "best")
    plt.show()


# This function is used to plot the bar_graph.
def plot_bar(x_coord, y_coord, x_label, y_label, state_name):
    # this is for plotting purpose
    index = np.arange(len(x_coord))
    plt.bar(x_coord, y_coord)
    plt.xlabel(x_label, fontsize=5)
    plt.ylabel(y_label, fontsize=5)
    plt.xticks(index, x_coord, fontsize=5, rotation=30)
    plt.title('Historical population growth of ' + state_name)
    plt.show()


#scatter plot of historical population (time vs population) of a state.
def scatter_plot(time, population, state_name):
    plt.scatter(time, population, alpha=0.5)
    plt.title('Scatter plot historical population (Population vs Time) of ' + state_name)
    plt.xlabel('Year')
    plt.ylabel('Population')
    plt.show()


#  This function is used to refresh the overall information of all the states.
# It also creates the dataframe of the data and also creates a csv file named "Overall_data.csv".
def refresh_overall():
    overall = overall_states()
    df = pd.DataFrame(overall, columns=["State Name", "State Abbr.", "Capital", "Establised", "Population", "Total Area", "Land Area", "Water Area"])
    df.to_csv("Overall_data.csv")


# This function is used to refresh the data of a particular state.
# It also creates the dataframe of the data.
# It also creates 2 csv files named "state_abbr_racial.csv", state_abbr_historical.csv.
def refresh_state(abbr):
    historical_pop, head = poptrend(abbr)
    state = pd.DataFrame(historical_pop, columns= head)
    state.to_csv("{}_historical.csv".format(abbr))
    racial_stats, head = popstats(abbr)
    state = pd.DataFrame(racial_stats, columns= head)
    state.to_csv("{}_racial.csv".format(abbr))


# This is the main function which contains the choosing  menu and all other functionalities.
def main():
    global states_abbr
    global states_name
    choice = "1"
    while choice != "exit":
        print("Enter Your command (help for instructions):")
        choice = input()
        if choice == "refresh":
            print("Enter 1 to refresh the database of all states")
            print("Enter 2 to refresh the data of a particular state.")
            i = 0
            while i not in ["1", "2"]:
                i = input()
            if i == "1":
                refresh_overall()
                print("Database refreshed.")
            else:
                print("Enter the state abbrevation.")
                print("Enter the Sate Abbrevation in upper_case")
                s = ""
                while s not in states_abbr:
                    s = input()
                refresh_state(s)
                print("Data is refreshed.")
        elif choice == "info":
            try:
                df = pd.read_csv("Overall_data.csv", index_col = False)
                print(df)
            except:
                #if no saved file is present.
                print("No Database found.")
                print("Please refresh the database.")
        elif choice=="exit":
            exit
        elif choice == "help":
            print("1) Enter refresh to refresh the database.")
            print("2) Enter info to display the information about all states.")
            print("3) Enter poptrend<state_abbr> to display the population trends of a state.")
            print("4) Enter popstats<state_abbr> to display the racial population trends of a state")
            print("5) Enter exit to leave.")
        elif "poptrend" in choice :
            s = choice[9:11]
            while s not in states_abbr:
                print("Enter the valid Sate Abbrevation in upper_case")
                s = input()
            try:
                df = pd.read_csv("{}_historical.csv".format(s))
                year = list(df['Census'])
                popul = list(df['Pop.'])
                n = len(year)
                for i in range(n):
                    year[i] = int(year[i])
                    popul[i] = int(str(popul[i]).replace(",",""))
                name = states_name[states_abbr.index(s)]
                scatter_plot(year, popul, name)
                print(df)
            except:
                print('NO DATABASE FOUND. Loading the data, it may take some time.')
                data, head = poptrend(s)
                df = pd.DataFrame(data, columns= head)
                df.to_csv("{}_historical.csv".format(s))
                year = []
                popu = []
                for each in data:
                    year.append(int(each[0]))
                    popu.append(int(str(each[1]).replace(",","")))
                name = states_name[states_abbr.index(s)]
                scatter_plot(year, popu, name)
                print(df)
        elif "popstats" in choice:
            print("Enter the state abbrevation.")
            s = choice[9:11]
            while s not in states_abbr:
                print("Enter the valid Sate Abbrevation in upper_case")
                s = input()
            try:
                df = pd.read_csv("{}_racial.csv".format(s))
                races = list(df['Racial composition'])
                col_name = list(df.columns)
                columns = len(col_name)
                for i in range(2, columns):
                    percentage = list(df[col_name[i]].values)
                    n = len(percentage)
                    for j in range(n):
                        if str(percentage[j]) == "–":
                            percentage[j] = "0%"
                        percentage[j] = float(str(percentage[j]).replace("%", ""))
                    piechart(races, percentage, col_name[i])
                print(df)
            except:
                print('NO DATABASE FOUND. Loading the data, it may take some time.')
                data, head = popstats(s)
                if len(data) == 0 or states_name[states_abbr.index(s)] == 'California':
                    print("Appropriate information does not exist for the entered request")
                    continue
                df = pd.DataFrame(data, columns= head)
                df.to_csv("{}_racial.csv".format(s))
                nn = len(data[0])
                n = len(data)
                races = []
                for i in range(n):
                    races.append(data[i][0])
                for j in range(1, nn):
                    percentage = []
                    for i in range(n):
                        val = str(data[i][j]).strip()
                        if val == "–":
                            val = "0%"
                        if val == "N/A":
                            val = "0%"
                        percentage.append(float(val.replace("%", "")))
                    piechart(races, percentage, head[j])
                print(df)
        else:
            print("Invalid entry")
            continue

overall_states()
if __name__ == '__main__':
    main()

