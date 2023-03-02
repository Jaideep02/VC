# Function to read and display the text file content line by line with each word separated by '$'
def display_file_content(file_name):
    try:
        with open(file_name, 'r') as f:
            for line in f:
                words = line.split()
                words = [word.strip() for word in words]
                line_text = "$".join(words)
                print(line_text)
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")

# Function to remove lines that contain 'a' and write to another file
def remove_lines_with_a(file_name, new_file_name):
    try:
        with open(file_name, 'r') as f, open(new_file_name, 'w') as f_new:
            for line in f:
                if 'a' not in line:
                    f_new.write(line)
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")

# Menu-driven program
while True:
    print("Please choose an option:")
    print("1. Read and display the file content with words separated by '$'")
    print("2. Remove lines that contain 'a' and write to another file")
    print("3. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        file_name = input("Enter the file name: ")
        display_file_content(file_name)

    elif choice == 2:
        file_name = input("Enter the file name: ")
        new_file_name = input("Enter the new file name: ")
        remove_lines_with_a(file_name, new_file_name)
        print(f"Lines containing 'a' removed from '{file_name}' and saved to '{new_file_name}'")

    elif choice == 3:
        print("Exiting program...")
        break

    else:
        print("Invalid choice, please try again.")
