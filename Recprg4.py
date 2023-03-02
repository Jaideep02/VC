def maximum(lst):
    max_elem = lst[0]
    for elem in lst:
        if elem > max_elem:
            max_elem = elem
    return max_elem

def minimum(lst):
    min_elem = lst[0]
    for elem in lst:
        if elem < min_elem:
            min_elem = elem
    return min_elem

def sum_elements(lst):
    sum_elem = 0
    for elem in lst:
        sum_elem += elem
    return sum_elem

while True:
    print("Please choose an option:")
    print("1. Find the maximum element")
    print("2. Find the minimum element")
    print("3. Find the sum of elements")
    print("4. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        lst = input("Enter a list of numbers separated by commas: ").split(",")
        lst = [int(i) for i in lst]
        max_elem = maximum(lst)
        print("Maximum element: ", max_elem)

    elif choice == 2:
        lst = input("Enter a list of numbers separated by commas: ").split(",")
        lst = [int(i) for i in lst]
        min_elem = minimum(lst)
        print("Minimum element: ", min_elem)

    elif choice == 3:
        lst = input("Enter a list of numbers separated by commas: ").split(",")
        lst = [int(i) for i in lst]
        sum_elem = sum_elements(lst)
        print("Sum of elements: ", sum_elem)

    elif choice == 4:
        print("Exiting program...")
        break

    else:
        print("Invalid choice, please try again.")
