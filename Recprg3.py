def MSEARCH(states):
    m_states = []
    for state in states:
        if state.startswith('M'):
            m_states.append(state)
    return m_states

def remove_letter(sentence, letter):
    new_sentence = sentence.replace(letter, "")
    return new_sentence

def count_words(sentence):
    words = sentence.split()
    return len(words)

while True:
    print("Please choose an option:")
    print("1. Search for states starting with 'M'")
    print("2. Remove a letter from a string")
    print("3. Count words in a string")
    print("4. Exit")

    choice = int(input("Enter your choice ~ "))

    if choice == 1:
        states = input("Enter a list of states separated by commas ~ ").split(",")
        m_states = MSEARCH(states)
        print("States starting with 'M' ~ ", m_states)

    elif choice == 2:
        sentence = input("Enter a sentence ~ ")
        letter = input("Enter a letter to remove ~ ")
        new_sentence = remove_letter(sentence, letter)
        print("New sentence ~ ", new_sentence)

    elif choice == 3:
        sentence = input("Enter a sentence ~ ")
        word_count = count_words(sentence)
        print("Number of words ~ ", word_count)

    elif choice == 4:
        print("Exiting program...")
        break

    else:
        print("Invalid choice, please try again.")
