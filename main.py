# Version 0.3


import os
import time
import random



# variables


game_vars = {
    'day': 1,
    'energy': 10,
    'money': 20,
    'bag': {},
    'error_count': 0
}


game_vars_start = {
    'day': 1,
    'energy': 10,
    'money': 20,
    'bag': {},
    'error_count': 0
}


seed_list = ['LET', 'POT', 'CAU']

seeds = {
    'LET': {'name': 'Lettuce', 
    'price': 2,
    'growth_time': 2,
    'growth_time': 2,
    'crop_price': 3
    },
    
    'POT': {'name': 'Potato',
            'price': 3,
            'growth_time': 3,
            'crop_price': 6
    },

    'CAU': {'name': 'Cauliflower',
            'price': 5,
            'growth_time': 6,
            'crop_price': 14
    }

}


original_cp = {
    'LET': 2,
    'POT': 6,
    'CAU': 14
}


farm = [ 
    [None, None, None, None, None],
    [None, None, None, None, None],
    [None, None, 'House', None, None],
    [None, None, None, None, None],
    [None, None, None, None, None] 

]

farm_default = [ 
    [None, None, None, None, None],
    [None, None, None, None, None],
    [None, None, 'House', None, None],
    [None, None, None, None, None],
    [None, None, None, None, None] 
    
]



# in_town(game_vars) function
# goals:
# 1. Visit the shop to buy seeds.                              [*]
# 2. Visit the farm to plant seeds and harvest crops.          [*]
# 3. End the day, resetting Energy and allowing crops to grow. [*]


# 9. Save the game                [ ]
# 0. Exit the game without saving [*]


def in_town(game_vars, farm):

    while True:

        show_stats(game_vars)

        if game_vars['day'] > 20:

            # checks if player wins or loses
            # $50 in 20 days is a win, if not then a loss
            if game_vars['money'] >= 50:
                print("You've paid off your debt. \nYou win!")
                with open('Leaderboard.txt', 'a') as leader_file:
                    leader_file.write(time.ctime(time.time()) + ';' + str(game_vars['money']))
                break

            else:
                print('You lost!')
            
            farm = farm_defualt
            game_vars = game_vars_start

        choice = input('''You are in the town of Prixia

-------------------------
1) Visit Shop
2) Visit Farm
3) End Day

9) Save Game (incomplete)
0) Exit Game 
-------------------------
>''')

        if choice == '1':
            game_vars = in_shop(game_vars)

        
        elif choice == '2':
            game_vars, farm = in_farm(game_vars, farm)


        elif choice == '3':
            game_vars, farm = end_day(game_vars, farm)
        
        elif choice == '0':
            print('See you soon!')
            exit()

        else:
            print('Invalid Input.')
            game_vars['error_count'] += 1













# in_shop(game_vars) function
# goals:
# Show the menu of the seed shop, and allow players to buy seeds
# Seeds can be bought if player has enough money
# Ends when player selects to leave the shop
#
def in_shop(game_vars):
    print("Welcome to Ionix's Seed Shop!\n")
    

    while True:
        show_stats(game_vars)

        print(f'''What would you like to buy?
{'Seed':<17}{'Price':<7}{'Days to Grow':<14}{'Crop Prices':<10}
''')

        for a, b in enumerate(seeds.values()): # Order, seed details

            print(f"{a+1:>2}) {b['name']:<15}{b['price']:<10}{b['growth_time']:<13}{b['crop_price']}")
        
        print('\n 0) Leave','\n' + '-' * 50)

        # input validation
        try:
            choice = int(input('Your choice? ')) - 1
            if choice + 1 == 0:

                print('See you soon!')
                break

            elif not(0 < choice + 1 <= len(seed_list)):

                print('Invalid input')
                game_vars['error_count'] += 1
                continue

        except ValueError: 
            print('Invalid input!')
            game_vars['error_count']+=1
            continue

        
        #ask player the amount of seed that they want to purchase
        try:
            amount = int(input(f'You have ${game_vars['money']}\nHow many do you wish to buy? '))
            
            if amount < 0 :
                print('Invalid input!')
                game_vars['error_count'] += 1
                continue
            
        except ValueError: 
            print('Invalid input!')
            game_vars['error_count'] += 1
            continue

        # check cost and record in dict
        cost = seeds[seed_list[choice]]['price'] * amount

        if cost > game_vars['money']:
            print("You can't afford that")
        else: 
            game_vars['money'] -= cost

            #number of seeds
            b = game_vars['bag'].get(seed_list[choice])
            game_vars['bag'].update({seed_list[choice]:(0 if b == None else b) + amount})

            print(f'You bought {amount} {seeds[seed_list[choice]]['name']} seeds.')

    return game_vars
















# draw_farm(farm, farmer_row, farmer_col) function
# goals:
# Draw farm and house on the grid
#
def draw_farm(farm, farmer_row, farmer_col):
    
    # drawing the farm by row
    for row in range(len(farm)):

        print('+-----' * len(farm[row]), end='+\n')
        # name/seed name display
        for a in farm[row]:
            try:
                if 'House' != a :
                    print(f'| {a[0]:<3} ', end='')
                else: 
                    print(f'| HSE ', end='')
            
            except TypeError:
                print('|     ', end='')
        print('|')
        
        # print player position
        for b in range(len(farm[row])):

            if b == farmer_col and row == farmer_row:
                print('|  X  ', end = '')
            else: 
                print('|     ', end='')
        print('|')

        # print days for seed to grow
        for a in farm[row]:
            try:
                if 'House' != a :
                    print(f'|  {a[1]:<2} ', end='')
                else: print('|     ', end='')
            
            except TypeError:
                print('|     ', end='')
        print('|')

    print('+-----' * len(farm[row]), end='+\n')





# in_farm(game_vars, farm) function
# goals:
# Move by typing in W, A, S, D to move th player
# Reduce energy by 1 when moving
# Plant crops
# Harvest crops
# Return to town (does not cost energy)
#
#
def in_farm(game_vars, farm):


    # starting coordinates of the player
    pos_x, pos_y = 2, 2

    while True:
        energy = game_vars['energy']
        batch_h = False # variable for checking if person can harvest 2x2
        draw_farm(farm,pos_y,pos_x)

        # prevent people from planting over and also allow harvest functionality
        if farm[pos_y][pos_x] == None:
            string_a = '\nP)lant seed'

        elif (farm[pos_y][pos_x] == 'House') or farm[pos_y][pos_x][1] != 0: 
            string_a = ''

        # check if user can harvest 2x2 grid
        elif farm[pos_y][pos_x] == farm[pos_y + 1][pos_x + 1] == farm[pos_y + 1][pos_x] == farm[pos_y][pos_x + 1] and (pos_x > len(farm) - 1 and pos_y > len(farm)-1):

            batch_h = True
            # ask user if wants to harvest
            string_a = '\nH)arvest '+seeds[farm[pos_y][pos_x][0]]['name'] +' for $' + str(seeds[farm[pos_y][pos_x][0]]['price'] * 4)

        else: 
            
            string_a = '\nH)arvest ' + seeds[farm[pos_y][pos_x][0]]['name'] + ' for $' + str(seeds[farm[pos_y][pos_x][0]]['price'])

        choice = input(f'''Energy: {energy}
[WASD] Move {string_a}
R)eturn to Town
Your choice? ''').lower()

        # input validation
        if (farm[pos_y][pos_x] == 'House' and choice in 'ph') or (farm[pos_y][pos_x] == None and choice == 'h') or (farm[pos_y][pos_x] != None and choice == 'p'):
            print('Invalid input!')
            game_vars['error_count'] += 1
            continue
        
        # match input to what user selected
        
        if choice == 'w': 
            if pos_y > 0 and energy > 0: 
                pos_y -= 1
                game_vars['energy'] -= 1 
            
            else:
                print('Too tired')
        elif choice == 'a':

            if pos_x > 0 and energy > 0: 
                pos_x -= 1
                game_vars['energy'] -= 1
                
            else:
                print('Too tired')
            
        elif choice == 's':
            if pos_y < len(farm) - 1 and energy > 0: 
                pos_y +=1
                game_vars['energy'] -= 1

            else:
                print('Too tired')
            
        elif choice == 'd':
            if pos_x < len(farm) - 1 and energy > 0: 
                pos_x += 1
                game_vars['energy'] -= 1
                
            else:
                print('Too tired')

        elif choice == 'h': # harvest

            game_vars['energy'] -= 1
            plant = farm[pos_y][pos_x]
            # check for 2x2 squares of harvestable farm
            if batch_h:
                    
                print(f'You harvest the {seeds[plant[0]]['name']} and sold it for ${seeds[plant[0]]['crop_price'] * 4}!')
                game_vars['money'] += seeds[plant[0]]['crop_price'] * 4

                farm[pos_y][pos_x] = None
                farm[pos_y+1][pos_x] = None
                farm[pos_y][pos_x+1] = None
                farm[pos_y+1][pos_x+1] = None
                print(f'You now have ${game_vars['money']}!')

            elif farm[pos_y][pos_x][1] == 0:

                print(f'You harvest the {seeds[plant[0]]['name']} and sold it for ${seeds[plant[0]]['crop_price']}!')
                game_vars['money'] += seeds[plant[0]]['crop_price']
                farm[pos_y][pos_x] = None
                print(f'You now have ${game_vars['money']}!')

            else: 
                print('Your harvest failed! This is reality kid.')
                farm[pos_y][pos_x] = None

        elif choice == 'p': # plant

            print(f'''What do you wish to plant?
{'-'*53}
    Seed{'Days to Grow':>20}{'Crop Price':>15}{'Avaliable':>12}
{'-'*53}''')    
            # check if bag is empty
            if game_vars['bag'] == {}:
                print('You have no seeds.')
                print('\n 0) Leave', '\n' + '-' * 53)
                continue
                
            else:
                for a, b in enumerate(game_vars['bag'].keys()):
                    print(f"{a+1:>2}) {seeds[b]['name']:<17}{seeds[b]['growth_time']:<16}{seeds[b]['crop_price']:<13}{game_vars['bag'][b]}")
                
            print('\n 0) Leave','\n'+'-'*53)

            # input validation
            try: 
                choice_2 = int(input('Your choice? ')) - 1
                if 0 <= choice_2 <= len(game_vars['bag']):
                    pass
                else: 
                    print('Invalid Input!')
                    game_vars['error_count'] += 1
                    continue
            
            except ValueError:
                print('Invalid input!')
                game_vars['error_count']+=1
                continue

            if choice_2 + 1 == 0: 
                continue # check if player wants to leave

            seed_sel = list(game_vars['bag'].keys())[choice_2]
            seed_quan = game_vars['bag'][seed_sel]

            # update map
            if farm[pos_y][pos_x] == None:

                if seed_quan > 1:
                    game_vars['bag'][seed_sel] -= 1
                    farm[pos_y][pos_x] = [seed_sel,seeds[seed_sel]['growth_time']]
                    
                else:
                    del game_vars['bag'][seed_sel]
                    farm[pos_y][pos_x] = [seed_sel,seeds[seed_sel]['growth_time']]

                game_vars['energy'] -= 1
                
                # prevent players from planting on occupied places
            elif farm[pos_y][pos_x].lower == 'house': 
                print('You can\' plant here!')
            else: 
                print('This spot has been taken')

        elif choice == 'r':
                break
        
        else:
            print('Invalid Input.')     
    
    return game_vars, farm    



# show_stats(game_vars) function
# goals:
# Displays:
#   - Day
#   - Energy
#   - Money
#   - Contents of seed bag
#
def show_stats(game_vars):
    
    try:
        os.system('clear')
    except Exception:
        os.system('cls')


    print('+' + '-' * 50 + '+')
    
    # print days
    print(f'|{' Day ' + str(game_vars['day']):<15}{'Energy: ' + str(game_vars['energy']):<18}{'Money: $' + str(game_vars['money']):<17}|')
    
    # check if bag contains seeds then print them
    if len(game_vars['bag']) == 0:
        print(f'| {'You have no seeds.'}{' ':>30} |')

    else: 
        
        print(f"|{' Your seeds:':<20}{' ':>30}|")
        for a, b in game_vars['bag'].items():
            print(f'| \t{seeds[a].get('name') + ': ' + str(b):<20}{' ':>22} |')
    
    print('+' + '-' * 50 + '+')


# end_day(game_vars) function
# goals:
# Ends the day, increasing day by 1, reducing crop waiting 
# time by 1, and resetting energy
#
def end_day(game_vars, farm):
    game_vars['day'] += 1
    game_vars['energy'] = 10

    # decrease the time for the plants
    for row in farm:
        for col in row:

            if col == None or col == 'House' or col[1] <= 0:
                pass
            else:
                col[1] -= 1

    for a in seeds.keys():
        seeds[a]['crop_price'] = random.randint(original_cp[a] - 2, original_cp[a] + 2)

    return game_vars, farm 


# in_shop(game_vars) function
# goals:
# Show the menu of the seed shop, and allow players to buy seeds
# Seeds can be bought if player has enough money
# Ends when player selects to leave the shop
#
# def in_shop(game_vars):




def bubble_sort(lista):

    n = len(lista)

    for i in range(n):
        swapped = False

        for a in range(0, n-i-1):

            if lista[a][1] < lista[a+1][1]:
                lista[a][1], lista[a+1][1] = lista[a+1][1], lista[a][1]
                swapped = True
        if (swapped == False):
            break

    return lista



def leader_board():
    
    try:
        print('----------------------------------------------------------')

        # sorting contents before printing the leaderboard
        with open('Leaderboard.txt', 'r') as reader:
            contents = reader.readlines()
            contents = [line.strip().split(';') for line in contents]

            contents = bubble_sort(contents)
        print('Rank Amount Time')
        if len(contents) > 5:
            for i in range(5):
                print(i + 1, '$' + str(contents[i][1]), contents[i][0])
        else:
            for i in range(len(contents)):
                print(i + 1, '$' + str(contents[i][1]), contents[i][0])

        contents = [str(a[0]) + ';' + str(a[1]) for a in contents]

        with open('Leaderboard.txt', 'w') as writer:
            for m in contents:
                writer.writelines(m + '\n')


        k = input('Press any key to leave\n')
            
    except FileNotFoundError:
        print('No Entry Yet.')
        k = input('\nPress any key to leave\n')

#----------------------------------------------------------------------
#    Main Game Loop
#----------------------------------------------------------------------
def main(game_vars, seeds, seed_list, farm):

    for a in seeds.keys():
        seeds[a]['crop_price'] = random.randint(original_cp[a] - 2, original_cp[a] + 2)
    while True:

        print('''----------------------------------------------------------

Welcome to Sunshine Farm!

You took out a loan to buy a small farm in the town of Prixia.
You have 20 days to pay off your debt of $50.
How successful will you be?

----------------------------------------------------------''')
    
        options_txt = '''1) Start a new game
2) Load Your saved game (incomplete)
3) Leaderboard

0) Exit Game
> '''

        choice = input(options_txt)

        if choice == '1':
            in_town(game_vars,farm)

        elif choice == '2':
            game_vars, farm, check = load_game(game_vars,farm)

            if check:
                in_town(game_vars,farm)
            
        elif choice == '3':
            leader_board()

            
        elif choice == '0':
            print('See you next time!')
            exit()
        
        else:
            print('Invalid Input.')

# Write your main game loop here

main(game_vars,seeds,seed_list,farm)
