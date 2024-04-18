import os
import re
import random
import string

from plane import Plane
from seat import Seat, SeatStatus


class BookingSystem:
    """A command line interface application for the seat booking

    Attributes: None

    Methods:
    instructions() -- Display instructions for the user
    get_user_input(message: str) -> str -- Get user input
    get_seat(row: int, column: int) -> Seat -- Get the seat object based on row and column numbers
    get_seat_number_from_user() -> Seat -- Get seat number from the user and return the corresponding seat object
    generate_booking_reference() -> str -- Generate a unique booking reference
    availability_of_seat() -- Check the availability of a seat and print its status
    book_seat() -- Book a seat if it is available
    free_seat() -- Free a seat if it is already reserved
    show_booking_state() -- Show the current booking state of all seats
    mainloop() -- Main loop for the application where the user can interact with the system
    """

    def __init__(self):
        """
        Initializes a new instance of the class.
        """

        # Create a new plane object and create the seat map
        self.plane = Plane()
        self.plane.create_seat_map()

        # Initialize the set of booking references and the dictionary of bookings
        self.booking_references = set()
        self.bookings = {}

    def instructions(self):
        """Display instructions for the user"""
        instructions = """
1. Check availability of seat
2. Book a seat
3. Free a seat
4. Show booking state 
5. Exit program
    """
        print(instructions)

    def get_user_input(self, message: str):
        """
        Prompts the user for input with the given message and returns the user's input.

        Args:
            message (str): The message to display to the user.

        Returns:
            str: The user's input.
        """
        user_input = input(message)
        return user_input

    def get_seat(self, row: int, column: int) -> Seat:
        """
        Retrieves the seat at the specified row and column from the plane.

        Args:
            row (int): The row number of the seat.
            column (int): The column number of the seat.

        Returns:
            Seat: The seat at the specified row and column.
        """
        return self.plane.seats[row][column]

    def get_seat_number_from_user(self) -> Seat:
        """
        Asks the user to enter a seat number and returns the corresponding Seat object.

        Returns:
            Seat: The Seat object corresponding to the user-entered seat number.
        """
        # Initialise the row number and column letter
        row_num = 1
        column_letter = "A"

        # List of column letters
        seats_letters = ["F", "E", "D", "X", "C", "B", "A"]
        while True:
            # Get user input for seat number
            user_seat = self.get_user_input("Please enter the seat number: ").upper()
            # Use regular expression to match seat number format e.g 22D
            match = re.search(r"(\d+)([A-F])", user_seat)
            if not match:
                # Print error message if seat number is invalid e.g 22G or ABCD
                print("Invalid seat name")
                continue
            # Extract the row number and column letter from the match
            row_num = int(match.group(1))
            column_letter = seats_letters.index(match.group(2))

            if not 1 <= row_num <= 80:
                # Print error message if row number is invalid e.g 0 or 81
                print("Invalid row number")
                continue
            break

        # Return the corresponding seat object based on row and column numbers
        return self.get_seat(row_num - 1, column_letter)

    def generate_booking_reference(self):
        """
        Generates a unique booking reference of eight alphanumeric characters.

        The function generates a random string of eight alphanumeric characters. It then checks if this string is already
        in the set of existing booking references. If it is, the function generates a new string. This process continues
        until a unique string is generated. The unique string is then added to the set of existing booking references and
        returned.

        Returns:
        str: A unique booking reference of eight alphanumeric characters.
        """
        while True:
            # Generate a random string of 8 alphanumeric characters
            # using the ascii_uppercase (a list of all uppercase letters) and digits (a list of all the digits)
            alphanumeric_characters = string.ascii_uppercase + string.digits
            reference = "".join(random.choices(alphanumeric_characters, k=8))

            # If the reference is unique, add it to the set of existing references and return it
            if reference not in self.booking_references:
                self.booking_references.add(reference)
                return reference

    def availability_of_seat(self):
        """Check the availability of a seat and print its status"""
        seat = self.get_seat_number_from_user()
        print(seat.status)

    def book_seat(self, customer_data: dict):
        """
        Book a seat if it is available and store the booking reference and customer data.

        Args:
        customer_data (dict): A dictionary containing customer data.
        """
        seat = self.get_seat_number_from_user()
        if seat.status == "F":
            # If the seat is available, change the status to reserved
            seat.status = SeatStatus.RESERVED

            # Generate a booking reference and store the booking details
            booking_reference = self.generate_booking_reference()
            self.bookings[booking_reference] = {
                "customer_data": customer_data,
                "seat": seat.seat_to_dict(),
            }
            print(
                f"Seat booked successfully. Your booking reference is: {booking_reference}"
            )
        else:
            print("Seat cannot be booked. It is already reserved or not available.")

    def free_seat(self, booking_reference: str):
        """
        Free a seat if it is already reserved and remove the booking details from the database.

        Args:
        booking_reference (str): The booking reference of the seat to be freed.
        """
        if booking_reference in self.bookings:
            # If the booking reference is available, get the seat object from the bookings dict
            seat = self.bookings[booking_reference]["seat"]
            # Get the seat object based on the row and column numbers
            # row -1 because the rows starts from 1 but the index starts from 0
            seat_object = self.get_seat(seat["row"] - 1, seat["column"])

            if seat_object.status == "R":
                # If the seat is reserved, change the status to empty
                # and remove the booking details
                seat_object.status = SeatStatus.EMPTY
                del self.bookings[booking_reference]
                print("Seat freed successfully")
            else:
                print("Seat cannot be freed. It is not reserved or not available.")
        else:
            print("Invalid booking reference")

    def show_booking_state(self):
        """Show the current booking state of all seats"""

        menu = """
1. Show your booking details
2. Show all seats map

"""
        print(menu)

        # Get user input for the command number
        user_input = input("Enter a command number from the above menu: ")
        if user_input == "1":
            # Get the booking reference from the user
            booking_reference = self.get_user_input("Enter your booking reference: ")
            if booking_reference in self.bookings:
                # If the booking reference is available, print the booking details
                booking = self.bookings[booking_reference]
                print(f"First name: {booking['customer_data']['first_name']}")
                print(f"Last name: {booking['customer_data']['last_name']}")
                print(f"Passport number: {booking['customer_data']['passport_number']}")
                print(
                    f"Booked Seat: {self.get_seat(booking['seat']['row']-1, booking['seat']['column']).get_seat_number()}"
                )
            else:
                print("Invalid booking reference")
        elif user_input == "2":
            # Print the seat map of the plane

            # Print the column letters
            print('    F   E   D   X   C   B   A ')
            for row in self.plane.seats:
                # Print the row number
                if row[0].row < 10:
                    print(f"{row[0].row} ", end=" ")
                else:
                    print(f"{row[0].row}", end=" ")

                # Print the status of each seat in the row
                for seat in row:
                    print(f"[{seat.status}]", end=" ")
                print()
        else:
            print("Invalid command")

    def mainloop(self):
        """Main loop for the application where the user can interact with the system"""

        # Clear the terminal
        os.system("cls" if os.name == "nt" else "clear")

        print("\nWelcome to the booking system!")
        self.instructions()
        while True:
            # Get user input for the command number
            user_input = self.get_user_input(
                "\nEnter a command number, or type (help): "
            )
            if user_input == "1":
                self.availability_of_seat()
            elif user_input == "2":
                # Get customer data from the user and book the seat
                customer_data = {
                    "first_name": self.get_user_input("Enter your first name: "),
                    "last_name": self.get_user_input("Enter your last name: "),
                    "passport_number": self.get_user_input(
                        "Enter your passport number (e.g P123456): "
                    ),
                }
                self.book_seat(customer_data)
            elif user_input == "3":
                # Free a seat based on the booking reference
                self.free_seat(self.get_user_input("Enter your booking reference: "))
            elif user_input == "4":
                # Show the current booking state of all seats or show the booking details
                self.show_booking_state()
            elif user_input == "5":
                print("Goodbye!")
                break
            elif user_input.lower() == "help":
                # Display the instructions
                self.instructions()
            else:
                print("Invalid command")


if __name__ == "__main__":
    app = BookingSystem()
    app.mainloop()
