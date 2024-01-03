import csv
from operator import itemgetter
import os

###########################################################
    #  Computer Project #8
    # read through provided csv files
    #  display banner and prompt the menu to the user at the beginning of main(). open_file will open the file succesfully otherwise it will run the except. There will be three main functions.
    # read_file goes thrpugh the data and iterates through the required rows and then appends the requirements. Heavy usage of .split
    # in_year will go through the required rows and find the games that came out in the year that was input by the user. It will also sort it alphabetically. 
    # by_dev will return a list of games made by a certain developer which the user had input. No need to worry about month or day.
    # use function calls in the the respective option choices as stated to in the Project 8 pdf. 
    # if user input option '1' '2' '3 '4' '5' or '6'run the respective block of code
    # if user input '7' then display then display the dismiss message and quit the program

    ###########################################################

MENU = '''\nSelect from the option: 
        1.Games in a certain year 
        2. Games by a Developer 
        3. Games of a Genre 
        4. Games by a developer in a year 
        5. Games of a Genre with no discount 
        6. Games by a developer with discount 
        7. Exit 
        Option: '''
        
      
        
def open_file(s):
    '''Opens a file with the specified filename and returns a file object. If the file with the specified name does not exist it will execute the except.'''
    while True:
        filename = input("\nEnter {} file: ".format(s))
        try:
            fp = open(filename, encoding='UTF-8')
            return fp
        except FileNotFoundError:
            print("\nNo Such file")
    pass   # remove this line

def read_file(fp_games):
    '''Reads game data from the file and returns a dictionary. returns games_dict (dict) -> A dictionary mapping game names to their data.'''
    reader = csv.reader(fp_games)
    next(reader)  # skip header row
    games_dict = {}
    for row in reader:
        name = row[0]
        release_date = row[1]
        developer = row[2].split(';')
        genre = row[3].split(';')
        modes = row[4].split(';')
        mode = 0 if modes[0].lower() == 'multi-player' else 1
        try:
            price = float(row[5].replace(',', '')) * 0.012
        except ValueError:
            price = 0.0
        overall_reviews = row[6]
        reviews = int(row[7])
        percent_positive = int(row[8].replace('%', ''))
        support = []
        if row[9] == '1':
            support.append('win_support')
        if row[10] == '1':
            support.append('mac_support')
        if row[11] == '1':
            support.append('lin_support')
        games_dict[name] = [release_date, developer, genre, mode, price, overall_reviews, reviews, percent_positive, support]
    return games_dict
    
    pass   # remove this line

def read_discount(fp_discount):
    '''Reads game discounts from a file and returns a dictionary. Returns discount_dict. A dictionary mapping game names to their discount'''
    reader = csv.reader(fp_discount)
    next(reader) # skip header row
    discount_dict = {}
    for row in reader:
        game_name = row[0]
        discount = round(float(row[1]), 2)
        discount_dict[game_name] = discount
    return discount_dict
    pass   # remove this line

def in_year(master_D,year):
    '''Returns a sorted list of games released in a given year. The function also takes an int parameter year which represents the year to filter games by. '''
    games_in_year = []
    for game, data in master_D.items():
        release_year = int(data[0].split("/")[-1])
        if release_year == year:
            games_in_year.append(game)
    return sorted(games_in_year)
    

def by_genre(master_D,genre): 
    '''genre_games (list). A sorted list of game names in the given genre, sorted by their percent positive reviews.'''
    genre_games = []
    for game, data in master_D.items():
        if genre in data[2]:
            genre_games.append((game, data[7]))
    genre_games.sort(key=itemgetter(1), reverse=True)
    return [game[0] for game in genre_games]
    pass   # remove this line
        
def by_dev(master_D,developer): 
    '''returns a sorted list of games by a given developer, sorted by release year. master_D (dict) -> A dictionary mapping game names to their data. developer (str) -> The developer to filter games by.'''
    dev_games = []
    list_of_games = []
    for game, data in master_D.items():
        pull_developer = data[1]
        if developer in pull_developer:
            dev_games.append((game, data[0][-4:]))
    dev_games.sort(key=itemgetter(1),reverse = True)

    for i in dev_games:
        list_of_games.append(i[0])
    return list_of_games

    dev_games.sort(key=itemgetter(1, 0), reverse=True)
    return [game[0] for game in dev_games]
    pass   # remove this line

def per_discount(master_D,games,discount_D): 
    '''The function per_discount calculates the discounted price of a list of games based on a discount dictionary. The function returns a list of discounted prices corresponding to each game in the games list. If a game is not in the discount_D dictionary, the original price from master_D is returned.'''
    discounted_prices = []
    for game in games:
        if game in discount_D:
            discount = discount_D[game]
            original_price = master_D[game][4]
            discounted_price = round((1 - discount / 100) * original_price, 6)
            discounted_prices.append(discounted_price)
        else:
            discounted_prices.append(master_D[game][4])
    return discounted_prices

    pass   # remove this line

def by_dev_year(master_D,discount_D,developer,year):
    '''The function by_dev_year returns a sorted list of game names released in a given year by a given developer, sorted by the discounted price of the game. The function calls the per_discount function to calculate the discounted prices of the games. returns a list of game names sorted by discounted price and game name.'''
    games_in_year = []
    for game, data in master_D.items():
        if developer in data[1] and data[0][-4:] == str(year):
            games_in_year.append(game)

    discounted_prices = per_discount(master_D, games_in_year, discount_D)
    game_prices = [(game, discounted_prices[i]) for i, game in enumerate(games_in_year)]
    game_prices.sort(key=itemgetter(1, 0))
    return [game[0] for game in game_prices]
    pass   # remove this line
          
def by_genre_no_disc(master_D,discount_D,genre):
    '''returns a sorted list of games in the given genre, which are not discounted. genre : str -> a string representing the genre to search for.'''
    genre_games = by_genre(master_D, genre)
    #filter out games with discounts
    non_discounted_games = []

    for game in genre_games:
        #if game not in discount_D:
        non_discounted_games.append((game, master_D[game][4]))

    non_discounted_games = sorted(non_discounted_games, key = itemgetter(1))

    out_discounted_games = []
    for item in non_discounted_games:
        if item[0] not in discount_D:
            out_discounted_games.append(item[0])

    return out_discounted_games 
   

def by_dev_with_disc(master_D,discount_D,developer):
    '''Parameters: master_D (dict), discount_D (dict), developer (str). This function returns a sorted list of games that are discounted and developed by the specified developer.'''
    dev_games = by_dev(master_D, developer)
    discounted_games = []
    for game_name in dev_games:
        if game_name in discount_D:
            discounted_games.append(game_name)
         
    return sorted(discounted_games)
             
def main():
    fp = open_file("games")
    discount_fp = open_file("discount")
    games = read_file(fp)
    discount = read_discount(discount_fp)
    while True:
        option = input(MENU)
        if option == "1":
            year = input('\nWhich year: ')
            while True:
                try:
                    year = int(year)
                    break
                except:
                    print("\nPlease enter a valid year")
                    year = input('\nWhich year: ')
            games_year = in_year(games, int(year))
            if games_year:
                print("\nGames released in {}:".format(year))
                in_year_games = ", ".join(games_year)
                print(in_year_games)
            else:
                print("\nNothing to print")
        elif option == "2":
            developer = input('\nWhich developer: ')
            dev_games = ", ".join(by_dev(games, developer))
            if dev_games == "":
                print("\nNothing to print")
            else:
                print("\nGames made by {}:".format(developer))
                print(dev_games)
        elif option == "3":
            genre = input('\nWhich genre: ' )
            genre_games = ", ".join(by_genre(games, genre))
            if genre_games == "":
                print("\nNothing to print")
            else:
                print("\nGames with {} genre:".format(genre))
                print(genre_games)
        elif option == "4":
            developer = input('\nWhich developer: ')
            year = input('\nWhich year: ')
            while True:
                try:
                    year = int(year)
                    break
                except:
                    print("\nPlease enter a valid year")
                    year = input('\nWhich year: ')
            dev_year = by_dev_year(games,discount,developer,year)
            dev_year = ", ".join(dev_year)
            if dev_year == "":
                print("\nNothing to print")
            else:
                print("\nGames made by {} and released in {}:".format(developer, year))
                print(dev_year)
        elif option == "5":
            genre = input('\nWhich genre: ')
            genre_without_dis = ", ".join(by_genre_no_disc(games,discount,genre))
            if genre_without_dis == "":
                print("\nNothing to print")
            else:
                print("\nGames with {} genre and without a discount:".format(genre))
                print(genre_without_dis)
        elif option == "6":
            developer = input('\nWhich developer: ')
            developer_disc = ", ".join(by_dev_with_disc(games,discount,developer))
            if developer_disc == "":
                print("\nNothing to print")
            else:
                print("\nGames made by {} which offer discount:".format(developer))
                print(developer_disc)
        elif option == "7":
            print("\nThank you.")
            break
        else:
            print("\nInvalid option")
            continue
    pass   # remove this line

if __name__ == "__main__":
    main()
