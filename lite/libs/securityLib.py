from .colorLib import *

def wait_for_enter(function):
    if not callable(function):
        raise TypeError("Due to security reasons the input of this function must be another function...")

    while True:
        user_input = input(f"Type '{color_red_fg("q")}' to return home or press {color_green_fg('Enter')} to continue: ")
        if user_input == 'q' or user_input == 'Q':
            break
        if user_input == '':
            # Execute the function safely
            function()  # Direct function call - much safer than exec()
            return True
        else:
            printt(f"Type '{color_yellow_bg("q")}' to return home or\nPress {color_yellow_bg('Enter')} to continue: ")
            continue

# Example usage:
def my_function():
    print("Function executed!")

if __name__ == '__main__':
    # Correct usage
    wait_for_enter(my_function)
