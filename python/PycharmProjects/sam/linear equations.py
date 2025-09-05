import numpy as np


def find_linear_equation(x_values, y_values):
    n = len(x_values)

    # Calculate the sums of x, y, x^2, and xy
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_x_squared = sum(x ** 2 for x in x_values)
    sum_xy = sum(x * y for x, y in zip(x_values, y_values))

    # Calculate the slope (m) and the y-intercept (b) of the linear equation
    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x ** 2)
    b = (sum_y - m * sum_x) / n

    return np.poly1d([m, b])  # Return a NumPy polynomial object


def find_polynomial_equation(x_values, y_values, degree):
    coefficients = np.polyfit(x_values, y_values, degree)
    equation = np.poly1d(coefficients)
    return equation


def get_user_input():
    x_values = []
    y_values = []

    while True:
        x_input = input("Enter an x value (or 'done' to finish): ")
        if x_input.lower() == "done":
            break

        y_input = input("Enter the corresponding y value: ")

        try:
            x = float(x_input)
            y = float(y_input)
            x_values.append(x)
            y_values.append(y)
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    return x_values, y_values


def calculate_r_squared(y_values, predicted_values):
    y_mean = np.mean(y_values)
    ss_total = sum((y - y_mean) ** 2 for y in y_values)
    ss_residual = sum((y - p) ** 2 for y, p in zip(y_values, predicted_values))
    r_squared = 1.0 - (ss_residual / ss_total)
    return r_squared


def main():
    print("Welcome to the Equation Finder!")
    print("Please enter x and y values. Type 'done' when you're finished.")

    x_values, y_values = get_user_input()

    if len(x_values) < 2:
        print("You need to enter at least two data points.")
    else:
        degree = 1  # Assume linear initially
        linear_equation = find_linear_equation(x_values, y_values)
        linear_predicted_values = linear_equation(x_values)
        linear_r_squared = calculate_r_squared(y_values, linear_predicted_values)

        for d in range(2, len(x_values)):
            polynomial_equation = find_polynomial_equation(x_values, y_values, d)
            polynomial_predicted_values = polynomial_equation(x_values)
            polynomial_r_squared = calculate_r_squared(y_values, polynomial_predicted_values)

            if polynomial_r_squared > linear_r_squared:
                degree = d
                linear_r_squared = polynomial_r_squared

        if degree == 1:
            print(f"The data appears to follow a linear pattern.")
            print(f"The linear equation that fits your data is: {linear_equation}")
        else:
            polynomial_equation = find_polynomial_equation(x_values, y_values, degree)
            print(f"The data appears to follow a non-linear pattern.")
            print(f"The polynomial equation that fits your data is: {polynomial_equation}")


if __name__ == "__main__":
    main()
