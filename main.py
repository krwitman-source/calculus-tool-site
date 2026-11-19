from dataclasses import dataclass
from bakery import assert_equal
from drafter import *
import sympy as sp
import matplotlib.pyplot as plt

"""
sympy as sp allows variables such as 'x' to be understood.
"""

set_website_title("Calculus Graphing and Calculating")
set_site_information(
    author="Kamryn Witman",
    description="Graph and calculate derivatives and critical numbers.",
    sources="",
    planning=["Final Project Pick a Problem.pdf", "Final Project LLM.pdf", "Final Project Design.pdf", "fullrec-2026-11-13-15-17-20.webm"],
    links=[]
)
hide_debug_information()
set_website_framed(False)

set_website_style("sakura")

@dataclass
class Calculation:
    """
    Stores a calculation performed by the user, including
    its type, original function, and resulting answer. 
    """
    calculation_type: str
    function: str
    result: str

@dataclass
class State:
    """
    Attributes:
        function: The mathematical function entered by the user.
        calculation: The type of calculation selected by the user.
        calculations: A history of Calculation objects previously performed.
        calculation_count: Total number of calculations completed.
        show_grid: Whether graph gridlines should be displayed
    """
    function: str
    calculation: str
    calculations: list[Calculation]
    calculation_count: int
    show_grid: bool

@route
def index(state: State) -> Page:
    """
    Welcome page. Users use the Get Started button to move onto the next page.
    """
    return Page(state, [
        Header("Calculus Calculator and Graphing Tool"),
        Paragraph("Welcome! Use this website to explore derivatives and critical numbers."),
        Button("Get Started", enter_function)
    ])


@route
def enter_function(state: State) -> Page:
    """
    The user is provided a TextBox to type their mathematical function, a
    SelectBox to choose their calculation type, a CheckBox to choose
    whether the graph will show gridlines, and a Submit button to move to the
    next page. 
    """
    return Page(state, [
        Header("Enter Your Function"),
        Paragraph(
        "Exponents should be input using ** (ex: x**2). "
        "When entering a constant before x use * between them (ex: 2*x)."),
        Paragraph("Enter a mathematical function of x below:"),
        TextBox("function", state.function),
        
        "Choose what you want to calculate:",
        SelectBox("calculation", [
            "First Derivative",
            "Second Derivative",
            "Critical Numbers"
            ], state.calculation),
        
        Paragraph("Show Gridlines on Graph? (Checkbox next to 'Submit')"),
        CheckBox("show_grid", state.show_grid),
        
        Button("Submit", graph_function)
    ])


@route
def graph_function(state: State, function: str, calculation: str, show_grid: bool) -> Page:
    """
    Checks that the user entered an input, updates the program state, generates
    a graph of the function using Matplotlib, and displays the graph. Based on the
    selected calculation type, a button is displayed that directs the user to the
    corresponding page of first derivative, second derivative, or critical numbers.
    """
    if function == "":
        return Page(state, [
            Header("Error"),
            Paragraph("Please enter a function first."),
            Button("Back", enter_function)
        ])
    
    state.function = function
    state.calculation = calculation
    state.show_grid = show_grid
    
    """
    Try tells Python to attempt the code.
    sp.sympify(function) tries to convert the user's text into a mathematical expression.
    exept catches certain errors if SymPy cannont understand the expression.
    The return will display and error message.
    """    
    x = sp.symbols('x')
    
    try:
        # SymPy converts the user's text into a mathematical expression.
        f = sp.sympify(function)
        
            
        graph_x = []
        graph_y = []
    
        for number in range(-10,11):
            graph_x.append(number)
            graph_y.append(float(f.subs(x, number)))
        

    except(sp.SympifyError, SyntaxError, TypeError, ValueError):
        return Page(state, [
            Header("Invalid Function"),
            Paragraph("Sorry, we couldn't understand your function."),
            Paragraph("Remember to use * between numbers and variables. "
                      "Please enter a mathematical functin such as x**2 or 2*x."),
            Button("Try Again", enter_function)
            ])
    # Matplotlib creates a graph using the x and y values.    
    plt.plot(graph_x, graph_y)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Graph of Your Function")
        
    if show_grid: 
        plt.grid()
    else:
        plt.grid(False)
        
    if calculation == "First Derivative":
         button = Button("Calculate First Derivative", first_derivative,
                   [Argument("function", function)])
                
    elif calculation == "Second Derivative":
         button = Button("Calculate Second Derivative", second_derivative,
                         [Argument("function", function)])
                         
    elif calculation == "Critical Numbers":
         button = Button("Find Critical Numbers", critical_numbers,
                         [Argument("function", function)])
    
    return Page(state, [
            Header("Your Function's Graph"),
            MatPlotLibPlot(),
            button
            ])
        
def calculate_first_derivative(function: str) -> str:
    """
    Calculates and returns the first dervative of a function.
    """        
    x = sp.symbols('x')
    f = sp.sympify(function)
    #sp.diff calculates the derivative of the expression.
    return str(sp.diff(f, x))

assert_equal(calculate_first_derivative("x**2"), "2*x")
assert_equal(calculate_first_derivative("x**3"), "3*x**2")

        
@route
def first_derivative(state: State, function: str) -> Page:
    """
    Calculates the first derivative of the user's function,
    stores the result in history, and displays the result.
    """
    result = calculate_first_derivative(function)
    
    new_calculation = Calculation(
        "First Derivative",
        function, result)

    state.calculations.append(new_calculation)
    state.calculation_count = state.calculation_count + 1
    
    
    return Page(state, [
    Header("First Derivative"),
    Paragraph("Your first derivative is: " + result),
    Button("Back to Graph", graph_function,
        [Argument("function", function),
        Argument("calculation", "First Derivative"),
         Argument("show_grid", state.show_grid)
         ]),
    Button("Enter a New Function", enter_function),
    Button("History", history)
    ])


def calculate_second_derivative(function: str) -> str:
    """
    Calculates and returns the second dervative of a function.
    """        
    x = sp.symbols('x')
    f = sp.sympify(function)
    #Calculates the second derivative.
    return str(sp.diff(f, x, 2))

assert_equal(calculate_second_derivative("x**2"), "2")
assert_equal(calculate_second_derivative("x**3"), "6*x")

@route
def second_derivative(state: State, function: str) -> Page:
    """
    Calculates the second derivative of the user's function,
    stores the result in history, and displays the result.
    """
    result = calculate_second_derivative(function)
    
    new_calculation = Calculation(
        "Second Derivative",
        function, result)
        
    state.calculations.append(new_calculation)
    state.calculation_count += 1

    
    return Page(state, [
        Header("Second Derivative"),
        Paragraph("Your second derivative is: " + str(result)),
        Button("Back to Graph", graph_function,
            [Argument("function", function),
            Argument("calculation", "Second Derivative"),
         Argument("show_grid", state.show_grid)
             ]),
        Button("Enter a New Function", enter_function),
        Button("History", history)
    ])


def find_critical_numbers(function: str) -> str:
    """
    Calculates and returns the critical numbers of the function.
    """
    x = sp.symbols('x')
    f = sp.sympify(function)
    derivative = sp.diff(f, x)
    #Finds critical numbers by setting the derivative to 0 and solving for x.
    return str(sp.solve(derivative, x))
    
assert_equal(find_critical_numbers("x**2"), "[0]")
assert_equal(find_critical_numbers("x**2 - 4*x"), "[2]")
assert_equal(find_critical_numbers("x**3"), "[0]")

@route
def critical_numbers(state: State, function: str) -> Page:
    """
    Finds the critical numbers of the user's function,
    stores the result in history, and displays the result.
    """
    result = find_critical_numbers(function) 
     
    new_calculation = Calculation(
        "Critical Numbers",
        function,
        result)
    
    state.calculations.append(new_calculation)
    state.calculation_count += 1

    
    return Page(state, [
        Header("Critical Numbers"),
        Paragraph("Your critical numbers are: " + str(result)),
        Button("Back to Graph", graph_function,
               [Argument("function", function),
                Argument("calculation", "Critical Numbers"),
         Argument("show_grid", state.show_grid)]),
        Button("Enter a New Function", enter_function),
        Button("History", history)
    ])

@route
def history(state: State) -> Page:
    """
    Stores the users past function inputs with their corresponding
    type of calculation, and result.
    If the user would attempt to view the history before they made any
    calculations, they would receive an error message.
    """
    history_items = []
    
    if len(state.calculations) == 0:
        history_items.append("You have not made any calculations yet.")
    
    for calculation in state.calculations:
        history_items.append(
            calculation.calculation_type
             + " of "
             + calculation.function
             + " = "
             + calculation.result
            )
        
    return Page(state, [
        Header("Calculation History"),
        Paragraph("Total calculations: " + str(state.calculation_count)),
        BulletedList(history_items),
        Button("Back to Home", index),
        Button("Clear History", clear_function)
        ])

@route
def clear_function(state: State) -> Page:
    """
    Removes the data stored and shown on the history page and graph.
    """
    state.calculations = []
    state.calculation_count = 0
    state.function = ""
    state.calculation = "First Derivative"
    state.show_grid = True
    # Clears the current graph.
    plt.clf()
    
    return Page(state, [
        Header("History Cleared"),
        Paragraph("All calculations history has been cleared!"),
        Button("Back to Home", index)
    ])

start_server(State("", "First Derivative", [], 0, True))
