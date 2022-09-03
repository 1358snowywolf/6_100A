import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    print("Loading word list from file.")
    
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = line.split()
    
    print(len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    Returns True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for i in range(len(secret_word)):
        if not secret_word[i] in letters_guessed:
            return False
    
    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    current_guess = ""
    
    for i in range(len(secret_word)):
        if secret_word[i] in letters_guessed: 
            current_guess += secret_word[i]
        else:
            current_guess += "_ "
    
    return current_guess


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = string.ascii_lowercase
    
    for i in range (len(letters_guessed)):
        available_letters = available_letters.replace(letters_guessed[i], '')
    
    return available_letters

def unique_letters(secret_word):
    letters = set()
    
    for i in range (len(secret_word)):
        letters.add(secret_word[i])
    
    return len(letters)

def hangman(secret_word):
    '''
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    
    secret_word = choose_word(load_words())
    letters_guessed = []
    guesses_left = 6
    warnings_left = 3
    won = False
    
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is " + str(len(secret_word)) + " letters long.")
    
    while(guesses_left > 0):
        available_letters = get_available_letters(letters_guessed)
    
        #get new letter
        print("-------------")
        print("You have " + str(guesses_left) + " guesses left.")
        print("Available letters: " + available_letters)
        current_letter = input("Please guess a letter: ")
        
        #current letter is not valid
        if(not current_letter in available_letters or not current_letter.isalpha()):
            if(warnings_left > 0):
                warnings_left -= 1
                
                if(not current_letter.isalpha()):
                    print("Oops! That is not a valid letter. You have " + str(warnings_left) + " warnings left: " + get_guessed_word(secret_word, letters_guessed))
                else:
                    print("Oops! You've already guessed that letter. You have " + str(warnings_left) + " warnings left: " + get_guessed_word(secret_word, letters_guessed))
            else:
                guesses_left -= 1
                
                if(not  current_letter.isalpha()):
                    print("Oops! That is not a valid letter. You have no warnings left so you lose one guess: " + get_guessed_word(secret_word, letters_guessed))
                else:
                    print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess: " + get_guessed_word(secret_word, letters_guessed))
            
            continue
        
        letters_guessed.append(current_letter)
        
        #determine if good or not
        if(current_letter in secret_word):
            print("Good guess: " + get_guessed_word(secret_word, letters_guessed))
        else:
            print("Oops! That letter is not in my word: " + get_guessed_word(secret_word, letters_guessed))
            
            if(current_letter in "aeiou"):
                guesses_left -= 2
            else:
                guesses_left -= 1
            
        if(is_word_guessed(secret_word, letters_guessed)):
            won = True
            break
    
    if(won):
        score = guesses_left * unique_letters(secret_word)
        print("Congratulations, you won!")
        print("Your total score for this game is: " + str(score))
    else:
        print("Sorry, you ran out of guesses. The word was " + secret_word)

def match_with_gaps(my_word, other_word):
    '''
    returns True if all the actual letters of my_word match the 
    corresponding letters of other_word, or the letter is the special symbol
    _ , and my_word and other_word are of the same length;
    False otherwise
    '''
    if(len(my_word) < len(other_word)):
        return False
    
    i = 0
    j = 0
    
    while(i < len(my_word)):
        if(my_word[i] == "_"):
            if(other_word[j] in my_word):
                return False
            
            i += 1
        else:
            if(my_word[i] != other_word[j]):
                return False
        
        j += 1
        i += 1
    
        if(j >= len(other_word) and i < len(my_word)):
            return False
    
    return j == len(other_word)

def show_possible_matches(my_word):
    '''
    print out every word in wordlist that matches my_word
    Keep in mind that in hangman when a letter is guessed, all the positions
    at which that letter occurs in the secret word are revealed.
    Therefore, the hidden letter(_ ) cannot be one of the letters in the word
    that has already been revealed.
    '''
    matches = []
    
    for i in range(len(wordlist)):
        if(match_with_gaps(my_word, wordlist[i])):
            matches.append(wordlist[i])
    
    print(len(matches))
    return matches


def hangman_with_hints(secret_word):
    '''
    Starts up an interactive game of Hangman w/ hints this time
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    
    secret_word = choose_word(load_words())
    letters_guessed = []
    guesses_left = 6
    warnings_left = 3
    won = False
    
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is " + str(len(secret_word)) + " letters long.")
    
    while(guesses_left > 0):
        available_letters = get_available_letters(letters_guessed)
    
        #get new letter
        print("-------------")
        print("You have " + str(guesses_left) + " guesses left.")
        print("Available letters: " + available_letters)
        current_letter = input("Please guess a letter: ")
        
        #want hint
        if(current_letter == "*"):
            print("Possible word matches are:")
            print(show_possible_matches(get_guessed_word(secret_word, letters_guessed)))
            continue
        
        #current letter is not valid
        if(not current_letter in available_letters or not current_letter.isalpha()):
            if(warnings_left > 0):
                warnings_left -= 1
                
                if(not current_letter.isalpha()):
                    print("Oops! That is not a valid letter. You have " + str(warnings_left) + " warnings left: " + get_guessed_word(secret_word, letters_guessed))
                else:
                    print("Oops! You've already guessed that letter. You have " + str(warnings_left) + " warnings left: " + get_guessed_word(secret_word, letters_guessed))
            else:
                guesses_left -= 1
                
                if(not  current_letter.isalpha()):
                    print("Oops! That is not a valid letter. You have no warnings left so you lose one guess: " + get_guessed_word(secret_word, letters_guessed))
                else:
                    print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess: " + get_guessed_word(secret_word, letters_guessed))
            
            continue
        
        letters_guessed.append(current_letter)
        
        #determine if good or not
        if(current_letter in secret_word):
            print("Good guess: " + get_guessed_word(secret_word, letters_guessed))
        else:
            print("Oops! That letter is not in my word: " + get_guessed_word(secret_word, letters_guessed))
            
            if(current_letter in "aeiou"):
                guesses_left -= 2
            else:
                guesses_left -= 1
            
        if(is_word_guessed(secret_word, letters_guessed)):
            won = True
            break
    
    if(won):
        score = guesses_left * unique_letters(secret_word)
        print("Congratulations, you won!")
        print("Your total score for this game is: " + str(score))
    else:
        print("Sorry, you ran out of guesses. The word was " + secret_word)

if __name__ == "__main__":
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
