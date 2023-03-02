# Function to create a text file with several lines of text
def create_text_file():
    try:
        with open("data.txt", "w") as f:
            f.write("The quick brown fox jumps over the lazy dog.\n")
            f.write("She sells seashells by the seashore.\n")
            f.write("How much wood would a woodchuck chuck,\n")
            f.write("If a woodchuck could chuck wood?\n")
            print("File created successfully.")
    except:
        print("Error creating file.")

# Function to copy words starting with vowels to another file
def copy_vowel_word():
    vowel_words = []  # Initialize the variable here
    try:
        with open("data.txt", "r") as f, open("vowel.txt", "w") as f_vowel:
            for line in f:
                words = line.split()
                for word in words:
                    if word[0].lower() in "aeiou":
                        f_vowel.write(word + "\n")
                        vowel_words.append(word)
            print("File created successfully.")
            return vowel_words
    except FileNotFoundError:
        print("File not found.")
        return []

# Function to read and display the contents of both files
def display_files():
    try:
        with open("data.txt", "r") as f, open("vowel.txt", "r") as f_vowel:
            print("Contents of 'data.txt':")
            print(f.read())
            print("Contents of 'vowel.txt':")
            print(f_vowel.read())
    except FileNotFoundError:
        print("File not found.")

# Function to display the total number of words starting with vowel
def display_vowel_count(vowel_words):
    vowel_count = len(vowel_words)
    print(f"Total number of words starting with vowel: {vowel_count}")

vowel_words = []
# Menu-driven program
while True:
    print("Please choose an option:")
    print("1. Create a text file with several lines of text")
    print("2. Copy words starting with vowels to another file")
    print("3. Read and display the contents of both files")
    print("4. Display the total number of words starting with vowel")
    print("5. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        create_text_file()

    elif choice == 2:
        vowel_words = copy_vowel_word()

    elif choice == 3:
        display_files()

    elif choice == 4:
        display_vowel_count(vowel_words)

    elif choice == 5:
        print("Exiting program...")
        break

    else:
        print("Invalid choice, please try again.")
