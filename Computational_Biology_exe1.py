# Or Itzhaki and Tal Ishon

import sys
import tkinter as tk
import random

############
# Globals: #
############

GRID_SIZE = 100
P = 0.5  # uniform distribution parameter
L = 2  # number of generations to wait for continue spread rumor
ITER_LIMIT = 200
generation = 0

# types of skepticism - (skepticism level, probability of spreading rumor)
S1 = (1, 1)
S2 = (2, 2 / 3)
S3 = (3, 1 / 3)
S4 = (4, 0)
S_list = [S1, S2, S3, S4]

S = [0.7, 0.1, 0.1, 0.1]  # determined the percent of the population that are from S1 S2 S3 S4 correspondingly

MESSAGE = None

root = None
generation_label = None
canvas = None

############


def validate_user_input(p, l, s1, s2, s3, s4, iter_lim):
    """
    Take the user input and validate it.
    If the input is valid - take user's input, otherwise take default globals
    """
    global P, L, S, ITER_LIMIT

    try:
        if p <= 0 or p > 1:
            print("Invalid Input - Default parameters")
            return False
        if iter_lim <= 0:
            print("Invalid Input - Default parameters")
            return False
        if l < 0 or l > iter_lim:
            print("Invalid Input - Default parameters")
            return False
        s = [s1, s2, s3, s4]
        sum = 0.0
        for i in s:
            if i < 0 or i > 1:
                print("Invalid Input - Default parameters")
                return False
            sum += i
        epsilon = 0.0001
        if sum + epsilon > 1.0001 or sum + epsilon < 1:
            print("Invalid Input - Default parameters")
            return False
    except Exception:
        print("Invalid Input - Default parameters")
        return False

    # after validation - can assign user input
    P = float(p)
    L = int(l)
    S = [float(f) for f in s]
    ITER_LIMIT = int(iter_lim)

    print("Valid Input - User parameters")
    return True


class UserInput(tk.Tk):
    def __init__(self):
        super().__init__()

        self.is_valid = True  # flag to check if user inputs are valid numbers and not char types

        self.title("PLEASE INSERT YOUR SIMULATION VALUES")

        x = int((self.winfo_screenwidth() - self.winfo_reqwidth()) / 2)
        y = int((self.winfo_screenheight() - self.winfo_reqheight()) / 2)

        self.geometry(f"+{x}+{y}")

        text_font = ("Comic Sans MS", 12)

        self.Welcome = tk.Label(self, text="WELCOME!", font=("Comic Sans MS", 20, "bold"), background="darkseagreen1")
        self.Welcome.pack(fill="both")

        self.second_welcome = tk.Label(self, text="CHOOSE AND SET ALL SIMULATION VALUES!",
                                       font=("Comic Sans MS", 15, "bold"), background="darkseagreen1")
        self.second_welcome.pack(fill="both")

        self.P_label = tk.Label(self,
                                text="People population density - P (0-1):",
                                font=text_font)
        self.P_label.pack()

        self.P_entry = tk.Entry(self)
        self.P_entry.pack()

        self.L_label = tk.Label(self,
                                text="Generations to wait till can spread rumor again - L:",
                                font=text_font)
        self.L_label.pack()

        self.L_entry = tk.Entry(self)
        self.L_entry.pack()

        self.s1_label = tk.Label(self,
                                 text="Number of people with skepticism level S1 (0-1):",
                                 font=text_font)
        self.s1_label.pack()

        self.s1_entry = tk.Entry(self)
        self.s1_entry.pack()

        self.s2_label = tk.Label(self,
                                 text="Number of people with skepticism level S2 (0-1):",
                                 font=text_font)
        self.s2_label.pack()

        self.s2_entry = tk.Entry(self)
        self.s2_entry.pack()

        self.s3_label = tk.Label(self,
                                 text="Number of people with skepticism level S3 (0-1):",
                                 font=text_font)
        self.s3_label.pack()

        self.s3_entry = tk.Entry(self)
        self.s3_entry.pack()

        self.s4_label = tk.Label(self,
                                 text="Number of people with skepticism level S4 (0-1):",
                                 font=text_font)
        self.s4_label.pack()

        self.s4_entry = tk.Entry(self)
        self.s4_entry.pack()

        self.IterLim_label = tk.Label(self,
                                      text="Limit for game generations:",
                                      font=text_font)
        self.IterLim_label.pack()

        self.IterLim_entry = tk.Entry(self)
        self.IterLim_entry.pack()

        self.submit_button = tk.Button(self,
                                       text="Submit",
                                       command=self.submit,
                                       font=("Comic Sans MS", 10),
                                       cursor="hand2",
                                       activebackground="gold1",
                                       activeforeground="white",
                                       background="darkseagreen1")
        self.submit_button.pack()

    def submit(self):
        global P, L, S, ITER_LIMIT, MESSAGE

        p, l, s1, s2, s3, s4, iter = [None] * 7  # initialize all optional variables with None
        try:
            p = float(self.P_entry.get())
            l = int(self.L_entry.get())
            s1 = float(self.s1_entry.get())
            s2 = float(self.s2_entry.get())
            s3 = float(self.s3_entry.get())
            s4 = float(self.s4_entry.get())
            iter = int(self.IterLim_entry.get())
        except Exception:
            # user input couldn't be cast to their values type
            self.is_valid = False

        if validate_user_input(p, l, s1, s2, s3, s4, iter) and self.is_valid:
            MESSAGE = "User Values Used: " \
                      "P = {}, L = {}, S1 = {}, S2 = {}, S3 = {}, S4 = {}, LIMIT = {}" \
                .format(p, l, s1, s2, s3, s4, iter)

        else:
            MESSAGE = "Default Values Used: " \
                      "P = {}, L = {}, S1 = {}, S2 = {}, S3 = {}, S4 = {}, LIMIT = {}" \
                .format(P, L, S[0], S[1], S[2], S[3], ITER_LIMIT)

        self.quit()


class Grid:

    def __init__(self):
        self.person_color = None
        self.rumor_color = None
        self.non_person_color = None
        self.population_grid = None
        self.people = None

    def grid_initialization(self, person_color="purple", rumor_color="yellow", non_person_color="white"):
        """
        Create a grid size 100*100.
        According to P initiate the grid s.t. person_color (purple by default) represents a cell in grid with a person
        and non_person_color (white by default) otherwise.
        """
        global P
        self.person_color = person_color
        self.rumor_color = rumor_color
        self.non_person_color = non_person_color

        g_size = GRID_SIZE ** 2
        num_cells_with_person = int(round(P * g_size))
        population = [person_color] * num_cells_with_person + [non_person_color] * (g_size - num_cells_with_person)

        random.shuffle(population)

        self.population_grid = [population[i:i + GRID_SIZE] for i in range(0, len(population), GRID_SIZE)]

        # save all the people coordinates on the grid
        person_cells = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.population_grid[i][j] == person_color:
                    person_cells.append((i, j))

        random.shuffle(person_cells)
        self.people = person_cells

    def get_people(self):
        return self.people

    def update_grid(self, people):
        """
        update grid according to state (that is determined from rumor spread).
        People that has True in state attribute will become rumor_color and all others stay person_color

        :param: people: all people on grid with their attributes (Person object).
        """

        for person in people:
            i, j = person.ID
            global generation
            if person.state:
                self.population_grid[i][j] = self.rumor_color
            else:
                self.population_grid[i][j] = self.person_color

                ############################
                # CODE FOR QUESTION PART 2:#
                ############################
                # if person.skepticism[0] == 1:
                #     self.population_grid[i][j] = "red"
                # if person.skepticism[0] == 2:
                #     self.population_grid[i][j] = "pink"
                # if person.skepticism[0] == 3:
                #     self.population_grid[i][j] = "orange"
                # if person.skepticism[0] == 4:
                #     self.population_grid[i][j] = "magenta"

    def draw_grid(self, begin=False):
        """
        draw grid according to rumor spread.

        """

        global generation, generation_label
        canvas.delete("all")
        cell_size = 7

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                x0 = i * cell_size
                y0 = j * cell_size
                x1 = x0 + cell_size
                y1 = y0 + cell_size

                color = self.population_grid[i][j]
                canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
                # Update generation counter
                if not begin:
                    generation_label.config(text="Generation: {}".format(generation), font=("Segoe Print", 15, "bold"))
                else:
                    generation_label.config(text="SIMULATION BEGINNING - will start in a few seconds", font=("Segoe Print", 15, "bold"))

class Person:
    """
    Define a person as a class.

    :param: ID - a tuple represents person's (i, j) coordinates on grid.
            state - True if person has heard a rumor and is going to spread it, False o.w
            skepticism - represents the odds a person believes a rumor and is willing to spread it.
            could be one of the 4 [S1, S2, S3, S4].
            neighbors - list of all person's neighbors.
            cant_spread - indicates how many generations to wait if a person already spread a rumor.
            rumor - indicates how many times a person got a rumor to spread.
    """

    def __init__(self, ID, skepticism, neighbors):
        self.ID = ID
        self.state = False
        self.skepticism = skepticism
        self.neighbors = neighbors
        self.cant_spread = 0
        self.rumor = 0

    def spread_neighbors(self):
        for neighbor in self.neighbors:
            # validate if neighbor can spread rumor
            if neighbor.cant_spread == 0:
                neighbor.rumor += 1  # neighbor now has a rumor to spread

        # make sure person can't spread another rumor for the next L generations
        self.cant_spread = L
        self.state = False

    def get_skepticism_level(self):
        """
        :return: odds to spread a rumor
        """
        return self.skepticism

    def change_state(self, S):
        """
        :param S: represents the 'skepticism level' to change state accordingly.
        """
        probability = S_list[S - 1][1]
        if random.random() < probability:
            self.state = True


def update_neighbors(people_obj):
    """
    for each person created, create a group of people that are their immediate neighbors according to potential neighbors coordinates.
    """
    for person in people_obj:
        person.neighbors = [p for p in people_obj if p.ID in person.neighbors]


def get_skepticism(number_of_people):
    """
    Create a list that will hold all the skepticism levels according to their amount in population
    :param number_of_people: used as a param to get the percent of population of each skepticism level
    :return: shuffled skepticism list
    """
    skepticism = (S1,) * round(S[0] * number_of_people) + (S2,) * round(S[1] * number_of_people) + (S3,) * round(
        S[2] * number_of_people) + (S4,) * round(S[3] * number_of_people)

    # each person has a skepticism level - odds a person believes a rumor
    # we will shuffle the list in order to later assign randomly the person's skepticism level.
    skept_list = list(skepticism)
    random.shuffle(skept_list)
    skepticism = tuple(skept_list)

    return skepticism


def create_people_list(grid):
    """
    Initiate new personalities according to person cells coordinates which are the person's ID.
    Each person will be initiated with its skepticism level and its neighbors.
    :param grid: represents the world population lives in
    :return: initiated people list
    """
    people = []
    s = get_skepticism(len(grid.people))

    skept_list = []
    for k, p in enumerate(grid.people):
        i = p[0]
        j = p[1]
        person = Person(p, s[k],
                        [(i - 1, j - 1), (i - 1, j), (i - 1, j + 1), (i, j - 1), (i, j + 1), (i + 1, j - 1),
                         (i + 1, j), (i + 1, j + 1)])
        # choose the first four different skepticism levels as beginners:
        if person.skepticism[0] not in skept_list:
            skept_list.append(person.skepticism[0])
            person.state = True
        people.append(person)
    return people


def start_rumor(grid, people):
    """
    To start the program we will randomly choose a person from each skepticism level to start a rumor.
    """
    global generation
    grid.update_grid(people)
    grid.draw_grid()

    # Stop the simulation if there are no more rumors to spread or got to 100th generation
    if not any(person.state for person in people) or generation == ITER_LIMIT:
        root.destroy()
        return

    oldyellow = []
    neighbors = []
    # for the people with a rumor to spread, spread to neighbors:
    for person in people:
        if person.state:
            oldyellow.append(person)
            person.spread_neighbors()
            neighbors.append(person.neighbors)

    neighbors = [element for sublist in neighbors for element in sublist]

    # only former neighbors can potentially spread the rumor
    for neighbor in neighbors:
        # make sure there is a rumor to spread and the person can spread (spread = 0)
        if neighbor.rumor and not neighbor.cant_spread:
            if neighbor.rumor == 1 or neighbor.get_skepticism_level()[0] == 1:
                neighbor.change_state(neighbor.get_skepticism_level()[0])
            else:
                neighbor.change_state(neighbor.get_skepticism_level()[0] - 1)
        neighbor.rumor = 0
        # update L values
        if neighbor not in oldyellow and neighbor.cant_spread != 0:  # if someone can spread and have a rumor
            neighbor.cant_spread -= 1

    generation += 1

    root.update()
    root.after(0, start_rumor(grid, people))


def get_user_input():
    """
    Open a window to get user input and initialize the grid and simulation rules according to it.
    """
    user_input_window = UserInput()
    user_input_window.mainloop()

    user_input_window.destroy()


def initialize_simulation_window():
    global root, generation_label, canvas, MESSAGE
    # Create the Tkinter window
    root = tk.Tk()
    root.title("Rumor Spreading")

    # Create a label to display the generation number
    generation_label = tk.Label(root, text="BEGINNING SIMULATION", font=("Segoe Print", 10), background="lightgrey")
    generation_label.pack(fill="both")

    # Create a label to display the generation number
    input_label = tk.Label(root, text=MESSAGE, font=("Segoe Print", 10, "bold"), background="lightgrey")
    input_label.pack(fill="both")

    # Create the Tkinter canvas
    canvas = tk.Canvas(root, width=GRID_SIZE * 7, height=GRID_SIZE * 7, borderwidth=0, highlightthickness=0)
    canvas.pack()


def main():
    # get user input to initialize the simulation values
    get_user_input()

    # according to values user entered initialize grid (if values were valid - use user input)
    initialize_simulation_window()

    # initiate game grid
    grid = Grid()
    grid.grid_initialization()

    # initialize people:
    people = create_people_list(grid)

    grid.update_grid(people)
    grid.draw_grid(begin=True)
    root.update()

    update_neighbors(people)

    # start spreading rumors
    start_rumor(grid, people)

    # Run the Tkinter mainloop
    root.mainloop()
    sys.exit()


if __name__ == '__main__':
    main()
