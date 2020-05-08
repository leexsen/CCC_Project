import sys, array 

# create an index whose all elements are type of unsigned long
index = array.array('L') 
total_rows = 0;
offset = 0

input_filename = sys.argv[1]
output_filename = input_filename + '.index'

with open(input_filename, 'rb') as file:
    for line in file:
        index.append(offset) 
        offset += len(line) 
        total_rows += 1

index.append(total_rows)

with open(output_filename, 'wb') as file:
    index.tofile(file)
