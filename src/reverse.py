from .funcs import Sin, Cos, Times, X, Y, PI


def from_string(expression):
    """Convert a string representation to its corresponding mathematical expression."""

    # Remove any whitespace from the string
    expression = expression.replace(" ", "")

    def parse_binary_operation(index):
        """Helper function to parse binary operations like multiplication."""

        lhs, index = parse_primary(index)

        # Handle multiplication
        while index < len(expression) and expression[index] == "*":
            index += 1  # Skip the "*"
            rhs, index = parse_primary(index)
            lhs = Times(lhs=lhs, rhs=rhs, new=False)

        return lhs, index

    def parse_primary(index):
        """Helper function to parse primary expressions and unary operations."""

        if expression[index : index + 3] == "sin":
            index += 4  # Skip the "sin("
            arg, index = parse_binary_operation(index)
            index += 1  # Skip the ")"
            return Sin(arg, new=False), index

        elif expression[index : index + 3] == "cos":
            index += 4  # Skip the "cos("
            arg, index = parse_binary_operation(index)
            index += 1  # Skip the ")"
            return Cos(arg, new=False), index

        elif expression[index] == "x":
            return X(), index + 1

        elif expression[index] == "y":
            return Y(), index + 1

        elif expression[index : index + 2] == "pi":
            return PI(), index + 2

        elif expression[index] == "(":
            index += 1  # Skip the "("
            expr, index = parse_binary_operation(index)
            if expression[index] != ")":
                raise ValueError(
                    f"Expected ')' at index {index} but found '{expression[index]}'"
                )
            index += 1  # Skip the ")"
            return expr, index

        else:
            raise ValueError(
                f"Unexpected character at index {index}: {expression[index]}"
            )

    expr, _ = parse_binary_operation(0)
    return expr


def test_from_string():
    """Test cases to validate the from_string function."""

    test_expressions = [
        "x",
        "y",
        "pi",
        "cos(x)",
        "sin(y)",
        "cos(x*y)",
        "sin(pi*x)",
        "cos(pi*y)",
        "sin(x*y)*cos(x)",
        "sin(x*y)*cos(x*pi)",
        "sin(x*y)*cos(x*pi*cos(y))",
        "sin(x*y)*cos(x*pi*cos(y*cos(x*pi*y)))",
        "sin(pi*cos(y)*sin(pi*sin(pi*sin(cos(pi*y))))*sin(pi*x))",
        "cos(pi*cos(pi*cos(pi*sin(pi*sin(y))*y*x)))",
        "cos(pi*sin(pi*cos(cos(pi*cos(pi*y)))*cos(pi*cos(pi*sin(pi*y)))*sin(cos(y))*sin(pi*sin(pi))*y))",
    ]

    for test_expr in test_expressions:
        result = from_string(test_expr)
        assert (
            str(result) == test_expr
        ), f"For {test_expr}, expected {test_expr} but got {result}"


if __name__ == "__main__":
    test_from_string()
