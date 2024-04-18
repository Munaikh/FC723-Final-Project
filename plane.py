from seat import Seat


class Plane:
    """
    Represents a plane with seats.

    Attributes:
        seats (list): A 2D list representing the seat map of the plane.

    Methods:
        create_seat_map() -- Creates a seat map for the plane
        print_seat_map() -- Prints the seat map of the plane
    """

    def __init__(self) -> None:
        self.seats = self.create_seat_map()

    def create_seat_map(self):
        """
        Creates a seat map for the plane.

        Returns:
            list: A 2D list representing the seat map.
        """
        seat_map = []

        # Create a 2D list of seats, 80 rows and 7 columns
        for row in range(1, 81):
            row_chairs = []
            for column in range(7):
                row_chairs.append(Seat(column, row))
            seat_map.append(row_chairs)
        return seat_map

    def print_seat_map(self):
        """
        Prints the seat map of the plane.
        """
        for row in self.seats:
            for seat in row:
                print(seat, end=" ")
            print()
