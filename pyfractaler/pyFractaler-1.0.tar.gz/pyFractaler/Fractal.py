import turtle


class Fractal:

    def __init__(self, codegen, angle, inter):
        self.wn = turtle.Screen()
        self.t = turtle.Turtle()
        self.wn.title("pyFractal window")
        self.t.getscreen().bgcolor("black")
        self.t.pencolor("white")
        self.t.pensize(3)
        self.t.speed(0)
        self.codegen = codegen
        self.angle = angle
        self.inter = inter
        self.size = 10

    def start(self):
        for i in range(self.inter):
            for cmd in self.codegen:
                if cmd == 'F':
                    self.t.forward(self.size)
                elif cmd == '+':
                    self.t.right(self.angle)
                elif cmd == '-':
                    self.t.left(self.angle)
        self.wn.exitonclick()

    def set_size(self, size):
        self.size = size

class RuledFractal:

    def __init__(self, codegen, angle, inter, rule):
        self.wn = turtle.Screen()
        self.t = turtle.Turtle()
        self.wn.title("pyFractal window")
        self.t.getscreen().bgcolor("black")
        self.t.pencolor("white")
        self.t.pensize(3)
        self.t.speed(0)
        self.codegen = codegen
        self.angle = angle
        self.inter = inter
        self.rule = rule
        self.size = 10

    def start(self):
        self.codegen = self.generate_code()
        for cmd in self.codegen:
            if cmd == 'F':
                self.t.forward(self.size)
            elif cmd == '+':
                self.t.right(self.angle)
            elif cmd == '-':
                self.t.left(self.angle)
        self.wn.exitonclick()

    def generate_code(self):
        start_string = self.codegen
        if self.inter == 0:
            return self.codegen
        end_string = ""
        for _ in range(self.inter):
            end_string = "".join(self.rule[i] if i in self.rule else i for i in start_string)
            start_string = end_string

        return end_string

    def set_size(self, size):
        self.size = size