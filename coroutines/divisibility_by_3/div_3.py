'''
Francesco Giraudo
Classe 5A ROB

Finite State Machine to check if a number is divisible by 3.
'''

class DivisibleByThree_FSM:
    def __init__(self):
        self.start = self._create_start()
        self.q0 = self._create_q0()
        self.q1 = self._create_q1()
        self.q2 = self._create_q2()

        self.current_state = self.start

        self.stopped = False

        self.start.send(None)
        self.q0.send(None)
        self.q1.send(None)
        self.q2.send(None)

    def divisible(self):
        try:
            return self.current_state == self.q0
        except:
            return 'Error'
    
    def send(self, n):
        try:
            n = int(n)
            self.current_state.send(n)
        except StopIteration:
            self.stopped = True
        except ValueError:
            print(f'Error: {n} must be a number.')

    def _create_start(self):
        while True:
            n = yield
            if n in [0, 3, 6, 9]:
                self.current_state = self.q0
            elif n in [1, 4, 7]:
                self.current_state = self.q1
            elif n in [2, 5, 8]:
                self.current_state = self.q2
            else:
                break
    
    def _create_q0(self):
        while True:
            n = yield
            if n in [0, 3, 6, 9]:
                self.current_state = self.q0
            elif n in [1, 4, 7]:
                self.current_state = self.q1
            elif n in [2, 5, 8]:
                self.current_state = self.q2
            else:
                break

    def _create_q1(self):
        while True:
            n = yield
            if n in [0, 3, 6, 9]:
                self.current_state = self.q1
            elif n in [1, 4, 7]:
                self.current_state = self.q2
            elif n in [2, 5, 8]:
                self.current_state = self.q0
            else:
                break

    def _create_q2(self):
        while True:
            n = yield
            if n in [0, 3, 6, 9]:
                self.current_state = self.q2
            elif n in [1, 4, 7]:
                self.current_state = self.q0
            elif n in [2, 5, 8]:
                self.current_state = self.q1
            else:
                break
