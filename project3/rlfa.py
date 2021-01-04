from csp import *
from datetime import datetime

# input-file paths
inputs = ["./rlfap/var2-f24.txt",
          "./rlfap/var2-f25.txt",
          "./rlfap/var3-f10.txt",
          "./rlfap/var3-f11.txt",
          "./rlfap/var6-w2.txt",
          "./rlfap/var7-w1-f4.txt",
          "./rlfap/var7-w1-f5.txt",
          "./rlfap/var8-f10.txt",
          "./rlfap/var8-f11.txt",
          "./rlfap/var11.txt",
          "./rlfap/var14-f27.txt",
          "./rlfap/var14-f28.txt",
          "./rlfap/ctr2-f24.txt",
          "./rlfap/ctr2-f25.txt",
          "./rlfap/ctr3-f10.txt",
          "./rlfap/ctr3-f11.txt",
          "./rlfap/ctr6-w2.txt",
          "./rlfap/ctr7-w1-f4.txt",
          "./rlfap/ctr7-w1-f5.txt",
          "./rlfap/ctr8-f10.txt",
          "./rlfap/ctr8-f11.txt",
          "./rlfap/ctr11.txt",
          "./rlfap/ctr14-f27.txt",
          "./rlfap/ctr14-f28.txt",
          "./rlfap/dom2-f24.txt",
          "./rlfap/dom2-f25.txt",
          "./rlfap/dom3-f10.txt",
          "./rlfap/dom3-f11.txt",
          "./rlfap/dom6-w2.txt",
          "./rlfap/dom7-w1-f4.txt",
          "./rlfap/dom7-w1-f5.txt",
          "./rlfap/dom8-f10.txt",
          "./rlfap/dom8-f11.txt",
          "./rlfap/dom11.txt",
          "./rlfap/dom14-f27.txt",
          "./rlfap/dom14-f28.txt"
]

class RLFA(CSP):

    def __init__(self, input, input1, input2):

        self.variables = list()         #variables of the problem
        self.domains = dict()           #domains of variables
        self.op_constraints = dict()    #constraint's operation symbol
        self.neighbours = dict()
        self.k_constraints = dict()
        self.temp_domains = dict()
        self.weights = dict()
        self.total_constraints = 0

        self.read_input_file(input, input1, input2)     #read input for information

        CSP.__init__(self, self.variables, self.domains, self.neighbours, self.rlfa_constraint)


    def get_tottal_assignments(self):
        return self.nassigns

    def set_total_constraints(self):
        self.total_constraints = 0

    def get_total_constraints(self):
        return self.total_constraints

    def increase_total_constraints(self):
        self.total_constraints += 1

    def AC3(csp, queue=None, removals=None, arc_heuristic=dom_j_up):
        """[Figure 6.3]"""
        if queue is None:
            queue = {(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]}
        csp.support_pruning()
        queue = arc_heuristic(csp, queue)
        checks = 0
        while queue:
            (Xi, Xj) = queue.pop()
            revised, checks = RLFA.revise(csp, Xi, Xj, removals, checks)
            if revised:
                if not csp.curr_domains[Xi]:
                    return False, checks  # CSP is inconsistent
                for Xk in csp.neighbors[Xi]:
                    if Xk != Xj:
                        queue.add((Xk, Xi))
        return True, checks  # CSP is satisfiable

    def revise(csp, Xi, Xj, removals, checks=0):
        """Return true if we remove a value."""
        revised = False
        for x in csp.curr_domains[Xi][:]:
            # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
            # if all(not csp.constraints(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            conflict = True
            for y in csp.curr_domains[Xj]:
                if csp.constraints(Xi, x, Xj, y):
                    conflict = False
                checks += 1
                if not conflict:
                    break
            if conflict:
                csp.prune(Xi, x, removals)
                revised = True

            if csp.curr_domains[Xi] == {}:
                self.weights[(int(Xi), int(Xj))] += 1
                self.weights[(int(Xj), int(Xi))] += 1

        return revised, checks

    def dom_j_up(csp, queue):
        return SortedSet(queue, key=lambda t: neg(len(csp.curr_domains[t[1]])))

    def mac(csp, var, value, assignment, removals, constraint_propagation = AC3):
        """Maintain arc consistency."""
        return constraint_propagation(csp, {(X, var) for X in csp.neighbors[var]}, removals)

    def forward_checking(self, csp, var, value, assignment, removals):
        """Prune neighbor values inconsistent with var=value."""
        csp.support_pruning()
        for B in csp.neighbors[var]:
            if B not in assignment:
                for b in csp.curr_domains[B][:]:
                    if not csp.constraints(var, value, B, b):
                        csp.prune(B, b, removals)
                        self.weights[(int(B), int(var))] += 1
                        self.weights[(int(var), int(B))] += 1
                if not csp.curr_domains[B]:
                    return False
        return True

    def sum(self, Xi, assignments):
        sum = 0
        for Xj in self.neighbours[int(Xi)]:
            sum += self.weights[(int(Xi), int(Xj))]
        return sum

    def heuristic(self, assignments, csp):
        min = 10000000000
        variable = None
        for var in csp.variables:
            if var in assignments:
                continue
            sum = self.sum(var, assignments)
            if csp.curr_domains is not None:
                dom = len(csp.curr_domains)
            else:
                dom = 1
            sum = dom/sum
            if(sum < min):
                min = sum
                variable = var
        return variable

    def read_input_file(self, input, input1, input2):
        print(input, input1, input2)
        line_counter = 1
        file = open(input, "r")

        for line in file:
            if(line_counter == 1):
                self.size = int(line)
            if(line_counter != 1):
                info = line.strip().split(' ')
                self.variables.append(int(info[0]))
                self.temp_domains[int(info[0])] = int(info[1])
                self.domains[int(info[0])] = []
                self.neighbours[int(info[0])] = []

            line_counter += 1

        line_counter = 1
        file = open(input2, "r")

        for line in file:
            if(line_counter != 1):
                info = line.strip().split(' ')

                for variable in self.variables:
                    if(self.temp_domains[variable] == int(info[0])):
                        for value in info[2:]:
                            self.domains[variable].append(int(value))

            line_counter += 1

        line_counter = 1
        file = open(input1, "r")

        for line in file:
            if(line_counter != 1):

                info = line.strip().split(' ')

                self.op_constraints[(int(info[0]), int(info[1]))] = info[2]
                self.op_constraints[(int(info[1]), int(info[0]))] = info[2]

                self.k_constraints[(int(info[0]), int(info[1]))] = int(info[3])
                self.k_constraints[(int(info[1]), int(info[0]))] = int(info[3])

                self.neighbours[int(info[0])].append(int(info[1]))
                self.weights[int(info[0]), int(info[1])] = 1
                self.neighbours[int(info[1])].append(int(info[0]))
                self.weights[int(info[1]), int(info[0])] = 1

            line_counter += 1

    def display(self, assignment):
        for var in self.variables:
            print(assignment[var], end=" ")
        print("")


    def rlfa_constraint(self, A, a, B, b):
        flag = False
        if self.op_constraints[(int(A), int(B))] == '=':
            flag = self.equal(A, a, B, b)
        elif self.op_constraints[(int(A), int(B))] == '>':
            flag = self.greater(A, a, B, b)

        self.increase_total_constraints()

        return flag

    def equal(self, A, a, B, b):
        k = self.k_constraints[(int(A), int(B))]
        return abs(a - b) == k

    def greater(self, A, a, B, b):
        k = self.k_constraints[(int(A), int(B))]
        return abs(a - b) > k



def solve_rlfa(input, input1, input2):
    prev_assignments = 0
    rlfa = RLFA(input, input1, input2)
    for index in range(1, 5):
        start = datetime.now()
        if(index == 1):
            print("- FC algorithm:")
            result = backtracking_search(rlfa, select_unassigned_variable = rlfa.heuristic, order_domain_values = lcv, inference = rlfa.forward_checking )
            # result = backtracking_search(rlfa, select_unassigned_variable = mrv, order_domain_values = lcv, inference = forward_checking)
        if(index == 2):
            print("- MAC algorithm:")
            result = backtracking_search(rlfa, select_unassigned_variable = rlfa.heuristic, order_domain_values = lcv, inference = RLFA.mac)
            # result = backtracking_search(rlfa, select_unassigned_variable = mrv, order_domain_values = lcv, inference = mac)
        if(index == 3):
            print("- FC+CBJ algorithm:")
            # result = backjumping_search(rlfa, select_unassigned_variable = mrv, order_domain_values = lcv, inference = mac )
            result = None
        if(index == 4):
            print("- MINCONFLICTS algorithm:")
            result = min_conflicts(rlfa, 5000)
        if(result != None):
            print("SET")
            rlfa.display(result)
        else:
            print("UNSET")
        print("Time: " + str(datetime.now()-start) + " seconds.")
        print("Assigns:" + str(rlfa.get_tottal_assignments() - prev_assignments))
        print("Constraints: " + str(rlfa.get_total_constraints()))
        rlfa.set_total_constraints()
        prev_assignments = rlfa.get_tottal_assignments()

# def backjumping_search(csp, select_unassigned_variable=first_unassigned_variable,
#                         order_domain_values=unordered_domain_values, inference=no_inference):
#
#     def backjump(assignment):
#
#         if len(assignment) == len(csp.variables):
#             return assignment
#
#         var = select_unassigned_variable(assignment, csp)
#         for value in order_domain_values(var, assignment, csp):
#             if 0 == csp.nconflicts(var, value, assignment):
#                 csp.assign(var, value, assignment)
#                 removals = csp.suppose(var, value)
#                 if inference(csp, var, value, assignment, removals):
#                     jump = backjump(assignment)
#                     if(jump != assignment and jump is not None):
#                         return jump
#                     # result = backtrack(assignment)
#                     # if result is not None:
#                     #     return result
#                 csp.restore(removals)
#         csp.unassign(var, assignment)
#         return None
#
#     result = backjump({})
#     assert result is None or csp.goal_test(result)
#     return result


if __name__ == '__main__':

    # for answer in range(4, 13):
    #     if(answer == 5):
    #         continue
    #     solve_rlfa(inputs[answer - 1], inputs[answer - 1 + 12], inputs[answer - 1 + 24])


    # choose puzzle to solve
    answer = input("Give a number from 1 to 12 to choose insample.\nGive 0 to finish.\n")
    answer = int(answer)

    while(answer != 0):

        if( answer >= 1 and answer <= 12):
            print("######################")
            print("Solution for \'rlfa"+ str(answer) + "\'")
            print("######################")
            solve_rlfa(inputs[answer-1], inputs[answer - 1 + 12], inputs[answer - 1 + 24])

        answer = input("Give a number from 1 to 12 to choose rlfa.\nGive 0 to finish.\n")
        answer = int(answer)





















