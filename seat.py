class SeatStatus:
    """
    A class that represents the status of a seat.

    Attributes:
        EMPTY (str): Represents an empty seat.
        RESERVED (str): Represents a reserved seat.
        ISLES (str): Represents an aisle seat.
        STORAGE (str): Represents a seat used for storage.
    """

    EMPTY = "F"
    RESERVED = "R"
    ISLES = "X"
    STORAGE = "S"


class Seat:
    """
    Represents a seat in a seating arrangement.

    Attributes:
        column (int): The column number of the seat.
        row (int): The row number of the seat.
        status (SeatStatus): The status of the seat (ISLES, STORAGE, or EMPTY).

    Methods:
        get_seat_number() -- Get the seat number based on the column and row.
    """

    def __init__(self, column: int, row: int) -> None:
        self.column = column
        self.row = row
        seat_number = self.get_seat_number()
        if seat_number == "X":
            self.status = SeatStatus.ISLES
        elif seat_number == "S":
            self.status = SeatStatus.STORAGE
        else:
            self.status = SeatStatus.EMPTY

    def __str__(self) -> str:
        return self.get_seat_number()

    def get_seat_number(self) -> str:
        """
        Get the seat number based on the column and row.

        Returns:
            str: The seat number.
        """
        seats_letters = ["F", "E", "D", "X", "C", "B", "A"]
        current_seat_letter = seats_letters[self.column]

        if current_seat_letter == "X":
            return "X"
        elif self.row in [77, 78] and current_seat_letter in ["F", "E", "D"]:
            return "S"
        else:
            return f"{self.row}{seats_letters[self.column]}"
