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
# 2. Visit the farm to plant seeds and harvest crops.          [ ]
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
2) Visit Farm (incomplete)
3) End Day

9) Save Game (incomplete)
0) Exit Game 
-------------------------
>''')

        if choice == '1':
            game_vars = in_shop(game_vars)
        
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
# def draw_farm(game_vars):



# in_farm(game_vars, farm) function
# goals:
# Move by typing in W, A, S, D to move th player
# Reduce energy by 1 when moving
# Plant crops
# Harvest crops
# Return to town (does not cost energy)
#
#
# def in_farm(game_vars):



# show_stats(game_vars) function
# goals:
# Displays:
#   - Day
#   - Energy
#   - Money
#   - Contents of seed bag
#
def show_stats(game_vars):
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
        #sorting contents before printing the leaderboard
        with open('Leaderboard.txt','r') as reader:
            contents = reader.readlines()
            contents = [line.strip().split(';') for line in contents]

            contents = bubble_sort(contents)
        print('Rank Amount Time')
        if len(contents) > 5:
            for i in range(5):
                print(i+1,'$'+str(contents[i][1]),contents[i][0])
        else:
            for i in range(len(contents)):
                print(i+1,'$'+str(contents[i][1]),contents[i][0])

        contents = [str(a[0])+';'+str(a[1]) for a in contents]

        with open('Leaderboard.txt', 'w') as writer:
            for m in contents:
                writer.writelines(m+'\n')


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
3) Leaderboard (incomplete)

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
