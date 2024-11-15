class BigNumber:
    def __init__(self, num_str):
        self.sign = 1
        if num_str[0] == '-':
            self.sign = -1
            num_str = num_str[1:]
        if isinstance(num_str, str):
            self.digits = [int(digit) for digit in reversed(num_str)]
        elif isinstance(num_str, int):
            self.digits = [int(digit) for digit in str(num_str)]
        else:
            raise TypeError("Input must be string or integer")

    def __str__(self):
        if self.sign == -1:
            return '-' + ''.join(map(str, reversed(self.digits)))
        else:
            return ''.join(map(str, reversed(self.digits)))

    def __lt__(self, other):
        if self.sign != other.sign:
            return self.sign < other.sign
        if len(self.digits) != len(other.digits):
            return len(self.digits) < len(other.digits)
        for i in range(len(self.digits)):
            if self.digits[i] != other.digits[i]:
                return self.digits[i] < other.digits[i]
        return False

    def __ge__(self, other):
        if self.sign != other.sign:
            return self.sign > other.sign
        if len(self.digits) != len(other.digits):
            return len(self.digits) > len(other.digits)
        for i in range(len(self.digits)):
            if self.digits[i] != other.digits[i]:
                return self.digits[i] > other.digits[i]
        return True

    def add(self, other):
        result = []
        carry = 0
        i, j = len(self.digits) - 1, len(other.digits) - 1
        while i >= 0 or j >= 0 or carry:
            digit_sum = carry
            if i >= 0:
                digit_sum += self.digits[i]
            if j >= 0:
                digit_sum += other.digits[j]
            result.append(digit_sum % 10)
            carry = digit_sum // 10
            i -= 1
            j -= 1
        result.reverse()
        return BigNumber(''.join(map(str, result)))
    def negate(self):
        return BigNumber('-' + str(self))

    def subtract(self, other):
        if self.sign != other.sign:
            return self.add(other.negate())
            # return self.add(other * -1)

        if self < other:
            return other.subtract(self).negate()
            # return other.subtract(self) * -1

        result = []
        borrow = 0
        i, j = len(self.digits) - 1, len(other.digits) - 1
        while i >= 0 or j >= 0:
            diff = borrow
            if i >= 0:
                diff += self.digits[i]
            if j >= 0:
                diff -= other.digits[j]
            result.append((diff + 10) % 10)
            borrow = -1 if diff < 0 else 0
            i -= 1
            j -= 1
        while result and result[-1] == 0:
            result.pop()
        if borrow:
            result.insert(0, -1)
        result.reverse()
        return BigNumber(''.join(map(str, result)))

    def multiply(self, other):
        def karatsuba_iterative(x, y):
            stack = [(tuple(x), tuple(y))]
            results = {}

            while stack:
                x, y = stack.pop()

                if len(x) == 1 and len(y) == 1:
                    result = x[0] * y[0]
                    # Handle negative signs
                    if (x[0] < 0 and y[0] >= 0) or (x[0] >= 0 and y[0] < 0):
                        result *= -1
                    results[(x, y)] = result
                    continue

                n = max(len(x), len(y))
                n_half = n // 2

                a, b = x[:n_half], x[n_half:]
                c, d = y[:n_half], y[n_half:]

                stack.append((tuple(a), tuple(c)))
                stack.append((tuple(b), tuple(d)))
                stack.append((tuple(a + b), tuple(c + d)))

            while stack:
                x, y = stack.pop()
                if (x, y) in results:
                    continue

                ac = results[(a, c)]
                bd = results[(b, d)]
                ad_bc = results[(a + b, c + d)] - ac - bd

                results[(x, y)] = ac * 10 ** n + ad_bc * 10 ** (n // 2) + bd

            return results[(x, y)]

        result = karatsuba_iterative(self.digits, other.digits)
        # Handle signs
        if (self.sign == -1 and other.sign == 1) or (self.sign == 1 and other.sign == -1):
            result *= -1
        return BigNumber(str(result))


    # def multiply(self, other):
    #     result = [0] * (len(self.digits) + len(other.digits))
    #     for i in range(len(self.digits)):
    #         carry = 0
    #         for j in range(len(other.digits)):
    #             product = self.digits[i] * other.digits[j] + carry + result[i + j]
    #             result[i + j] = product % 10
    #             carry = product // 10
    #         result[i + len(other.digits)] += carry
    #     while result and result[-1] == 0:
    #         result.pop()
    #     result.reverse()
    #     return BigNumber(''.join(map(str, result)))

    def power(self, n):
        if n == 0:
            return BigNumber('1')
        elif n == 1:
            return self
        elif n % 2 == 0:
            temp = self.power(n // 2)
            return temp.multiply(temp)
        else:
            temp = self.power(n // 2)
            return temp.multiply(temp).multiply(self)

    def shift_left(self, n):
        return BigNumber(''.join(map(str, self.digits + [0] * n)))

    def shift_right(self, n):
        return BigNumber(''.join(map(str, self.digits[0:len(self.digits) - n])))

    def factorial(self, n):
        if n == 0:
            return BigNumber('1')
        else:
            return self.multiply(self.factorial(n - 1))

    def divide(self, other):
        if other == BigNumber('0'):
            raise ZeroDivisionError("Division by zero")

        quotient = BigNumber('0')
        remainder = self.copy()
        divisor = other.copy()

        while remainder >= divisor:
            shift = 0
            while divisor.shift_left(shift) <= remainder:
                shift += 1
            divisor = divisor.shift_left(shift - 1)
            quotient = quotient.add(BigNumber('1').shift_left(shift - 1))
            remainder = remainder.subtract(divisor)

        return quotient, remainder

    def copy(self):
        return BigNumber(str(self))

# Example usage
# num1 = BigNumber('21')
# num2 = BigNumber('133')
#
# result_add = num1.add(num2)
# print("Addition:", result_add)
#
# result_sub = num1.subtract(num2)
# print("Subtraction:", result_sub)

# result_mul = num1.multiply(num2)
# print("Multiplication:", result_mul)

# result_div, remainder = num1.divide(num2)
# print("Division:", result_div)
# print("Remainder:", remainder)
#
# result_pow = num1.power(2)
# print("Power:", result_pow)
#
# result_factorial = BigNumber('5').factorial(5)
# print("Factorial:", result_factorial)
#
# result_shift_left = num1.shift_left(3)
# print("Shift Left:", result_shift_left)
#
# result_shift_right = num1.shift_right(3)
# print("Shift Right:", result_shift_right)