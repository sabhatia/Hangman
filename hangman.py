'''
Play a hangman game with the computer
Initial version is a text based version with 2 players
'''
import pwinput

def get_player_names():
    name1 = input("Enter Player 1 name: ").strip().title()
    name2 = input("Enter Player 2 name: ").strip().title()

    return name1, name2

def get_guess_word(player):
    print(f'{player}\'s turn')
    user_word = pwinput.pwinput('Enter your word: ', mask = '*')
    return user_word

'''
Asks the user to guess a character in the word
Does some sanity checks to ensure user entered valid input.
'''
def get_guess_char(player, all_guesses):
    valid_guess = False

    # User has to guess something not already tried
    while valid_guess == False:
        user_guess = input(f'Guess a letter, {player}: ').strip().lower()

        # Check if we got a character or string
        if len(user_guess) <= 0:
            print(f'System didn\'t detect valid input. Please try again.')
            continue
        
        # Let's pick the first character of the string
        char_guess = user_guess[0]

        # Is this character already one user guessed earlier?
        if char_guess in all_guesses:
            # Player already guessed this letter. Try again.
            print(f"You already guessed {char_guess}. Try again.")
            continue

        # All checks passed. Record the character and break the loop.
        valid_guess = True
        all_guesses.append(char_guess)

    # return the last character we added
    return all_guesses[-1]
        
''' 
Displays how far the word has been guessed
Known characters are displayed, and unknown ones are represented by '*'
Returns a list representation and a count of unknown characters
'''  
def evaluate_word(actual_word, good_guess):
    curr_display = [x if x in good_guess else '*' for x in actual_word]
    return curr_display, curr_display.count('*')
    
def play_one_round(round_id, playerA, playerB):

    # Setup some initial variables    
    turns = 'HANGMAN'
    MAX_BAD_TURNS = len(turns)
    bad_turns = 0
    all_guess, good_guess, bad_guess = [], [], []

    # Print a header
    print('=' * 20)
    print(f'\tRound {round_id}')
    print('=' * 20)

    # Get the word we want to guess from the user
    turn_word = get_guess_word(playerA)

    # Play a turn by the other user
    while bad_turns < MAX_BAD_TURNS:

        # Ask the user to guess a character
        curr_guess = get_guess_char(playerB, all_guess)

        # Check the status of the guess
        if curr_guess in turn_word:
            # Good guess - highlight it 
            print(f'Yay. Good guess.')
            good_guess.append(curr_guess)
            # To-do: Do more stuff here
        else:
            # Bad guess - increment turn count
            print(f"Ouch! Sorry, {curr_guess} does not in the word.")
            bad_turns += 1
            bad_guess.append(curr_guess)

        # Dislay the result of the turn
        evaluated_word, remaining_chars = evaluate_word(turn_word, good_guess)
        print(f"Guessed word: {''.join(evaluated_word)}")
        print(f"You are at: {turns[:bad_turns]}") 

        # Check and report the result of the round
        if remaining_chars == 0:
            break

    if bad_turns >= MAX_BAD_TURNS:
        print(f"{playerB} wasn't able to guess {turn_word} correctly.")
        print(f"{playerA} wins this round.")
        score = [1,0]
    else:
        print(f"{playerB} guessed {turn_word} correctly!")
        print(f'{playerB} wins this round.')
        score = [0,1]

    return score

def play_another_round():
    yn_response = input("Continue playing (Y/N): ").strip().lower()
    if len(yn_response) > 0 and yn_response[0] == 'y':
        # Gonna assume user meant yes
        return True
    
    return False


if __name__ == '__main__':
    print('Welcome to hangman!')
    
    # Initialize Game
    first_player, second_player = get_player_names()
    player_scores = [0,0]
    round_id = 1

    continue_playing = True
    print(f'Game Score\t{first_player}: {player_scores[0]}, {second_player}: {player_scores[1]}')

    while continue_playing:
        # Play one round of the game
        turn_score = play_one_round(round_id, first_player, second_player)
        player_scores = [a+b for a,b in zip(player_scores, turn_score)]
        print(f'Game Score\t{first_player}: {player_scores[0]}, {second_player}: {player_scores[1]}')

        # Switch the players turn
        first_player, second_player = second_player, first_player
        player_scores = player_scores[::-1]

        # Check if players wanna try again
        continue_playing = play_another_round()
        round_id += 1
