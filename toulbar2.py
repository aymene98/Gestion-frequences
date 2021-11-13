from pytoulbar2 import *
import argparse
import time

parser = argparse.ArgumentParser(description='Get file name to generate .CFN file.')
parser.add_argument('-p','--path', help='Path to the CFN file to parse', required=True)
parser.add_argument('-ps',"--print_sol", type=bool, default=False,help="Print the problem's solution if found.")
args = vars(parser.parse_args())

file_path = args['path']
print_sol = args['print_sol']

myCFN = pytoulbar2.CFN(1000)
myCFN.Read(file_path)

t0 = time.time() 
sol = myCFN.Solve()
#print(myCFN.Scopes)
if sol != None:
    name = file_path.split('/')[-1].split('.')[0]
    t1 = time.time()
    total = t1-t0
    print("Solution for file ", name, " is of cost :", sol[1], ' time taken :', total)
    if print_sol : print("Solution :", sol[0]) 
else:
    name = file_path.split('/')[-1].split('.')[0]
    print("No solution found for file :", name)
