import sys
import os

from problem import SumOfSubsetProblem

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

if len(sys.argv) != 3:
    print("Wrong number of arguments")
    sys.exit(-1)

subset_problems = SumOfSubsetProblem.from_json(input_file_path)

print("\n")

for idx, subset_problem in enumerate(subset_problems):
    print(f"Working on {subset_problem} \n")
    solution = subset_problem.bruteforce()
    subset_problem.export_correct_solutions_to_json(os.path.join(output_file_path, f"solution_{idx}.json"))

    if solution:
        print(f"Solution for this problem is {solution.subset}")
    
    print("\n")