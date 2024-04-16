import os
from plane import Plane
import re

from seat import Seat, SeatStatus


class BookingSystem:
    """A command line interface application for the seat booking

    Attributes: None

    Methods:
    instructions() -- Display instructions for the user
    get_user_input(message: str) -> str -- Get user input
    get_seat(row: int, column: int) -> Seat -- Get the seat object based on row and column numbers
    get_seat_number_from_user() -> Seat -- Get seat number from the user and return the corresponding seat object
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
        self.plane = Plane()
        self.plane.create_seat_map()

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
        Retrieves the seat at the specified row and column.

        Args:
            row (int): The row number of the seat.
            column (int): The column number of the seat.

        Returns:
            Seat: The seat at the specified row and column.
        """
        return self.plane.seats[row][column]

    def get_seat_number_from_user(self) -> Seat:
        """
        Prompts the user to enter a seat number and returns the corresponding Seat object.

        Returns:
            Seat: The Seat object corresponding to the user-entered seat number.
        """
        # Initialise the row number
        row_num = 1
        # Initialise the column letter
        column_letter = "A"
        # List of column letters
        seats_letters = ["F", "E", "D", "X", "C", "B", "A"]
        while True:
            # Get user input for seat number
            user_seat = self.get_user_input("Please enter the seat number: ").upper()
            # Use regular expression to match seat number format e.g 22D
            match = re.search(r"(\d+)([A-F])", user_seat)
            if not match:
                # Print error message if seat number is invalid
                print("Invalid seat name")
                continue
            # Extract the row number from the match
            row_num = int(match.group(1))
            # Extract the column letter from the match
            column_letter = seats_letters.index(match.group(2))
            if not 1 <= row_num <= 80:
                # Print error message if row number is invalid
                print("Invalid row number")
                continue
            break

        # Return the corresponding seat object based on row and column numbers
        return self.get_seat(row_num - 1, column_letter)

    def availability_of_seat(self):
        """Check the availability of a seat and print its status"""
        seat = self.get_seat_number_from_user()
        print(seat.status)

    def book_seat(self):
        """Book a seat if it is available"""
        seat = self.get_seat_number_from_user()
        if seat.status == "F":
            seat.status = SeatStatus.RESERVED
            print("Seat booked successfully")
        else:
            print("Seat is already reserved")

    def free_seat(self):
        """Free a seat if it is already reserved"""
        seat = self.get_seat_number_from_user()
        if seat.status == "R":
            seat.status = SeatStatus.EMPTY
            print("Seat freed successfully")
        else:
            print("Seat is already free")

    def show_booking_state(self):
        """Show the current booking state of all seats"""
        for row in self.plane.seats:
            for seat in row:
                print(f"[{seat.status}]", end="")
            print()

    def mainloop(self):
        """Main loop for the application where the user can interact with the system"""

        # Clear the terminal
        os.system("cls" if os.name == "nt" else "clear")

        print("\nWelcome to the booking system!")
        self.instructions()
        while True:
            user_input = self.get_user_input(
                "\nEnter a command number, or type (help): "
            )
            if user_input == "1":
                self.availability_of_seat()
            elif user_input == "2":
                self.book_seat()
            elif user_input == "3":
                self.free_seat()
            elif user_input == "4":
                self.show_booking_state()
            elif user_input == "5":
                print("Goodbye!")
                break
            elif user_input.lower() == "help":
                self.instructions()
            else:
                print("Invalid command")


if __name__ == "__main__":
    app = BookingSystem()
    app.mainloop()
