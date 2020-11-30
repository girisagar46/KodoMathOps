from decimal import Decimal

from asteval import Interpreter


class SubmissionEvaluator:
    """A helper class to evaluate if submission if correct or not.

    """

    def __init__(self, expression, submitted_result):
        self.expression = expression
        self.submitted_result = submitted_result

    # https://stackoverflow.com/a/18769210/4494547
    @staticmethod
    def remove_exponent(num):
        """To remove trailing zeros form a floating point number

        Args:
            num: Decimal object
        Returns:
            Decimal object with 2 decimal places if there is no trailing zero

        Example:
            >>> SubmissionEvaluator.remove_exponent(Decimal(1.01))
                1.010000000000000008881784197

            >>> SubmissionEvaluator.remove_exponent(Decimal(1.0))
                1
        """
        return num.quantize(Decimal(1)) if num == num.to_integral() else num.normalize()

    def evaluate(self):
        """A helper method to check if submitted answer for the provided question is correct or not.

        This helper function uses asteval to perform check
        """
        expression_interpreter = Interpreter()
        correct = SubmissionEvaluator.remove_exponent(
            Decimal("{:.3f}".format(expression_interpreter(self.expression))[:-1])
        )
        return str(correct) == self.submitted_result
