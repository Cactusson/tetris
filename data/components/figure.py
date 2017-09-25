class Figure:
    def __init__(self, forms):
        self.forms = forms
        self.matrix = self.forms[0]
        self.index = 0

    def rotate(self, clockwise):
        if clockwise:
            if self.matrix == self.forms[-1]:
                self.matrix = self.forms[0]
                self.index = 0
            else:
                self.matrix = self.forms[self.forms.index(self.matrix) + 1]
                self.index += 1
        else:
            if self.matrix == self.forms[0]:
                self.matrix = self.forms[-1]
                self.index = len(self.forms) - 1
            else:
                self.matrix = self.forms[self.forms.index(self.matrix) - 1]
                self.index -= 1
