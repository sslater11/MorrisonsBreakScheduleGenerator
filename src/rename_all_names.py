#!/usr/bin/env python3

import random


# Rename everyone in the file to create a sample output.

input_file = open( "Employee Schedule Weekly.html", "r" )

output_file = open( "sample_input.html", "w" )

# Change names to these
#⟇⁖⁖⁖⁖⁖⁖⁖⟇⁖⁖⁖⁖⁖⁖⁖⟇⁖⁖⁖⁖⁖⁖⁖⟇⁖⁖⁖⁖⁖⁖⁖⟇⁖⁖⁖⁖⁖⁖⁖⟇⁖⁖⁖⁖⁖⁖⁖<div class="employeeName">John, Smith</div>
all_names = [
    "Smith, John",
    "Smith, Jason",
    "Smith, Jerry",
    "Smith, Jeremy",
    "Smith, Sam",
    "Smith, Shawn",
    "Smith, Sean",
    "Smith, Simon",

    "Smith, Jenny",
    "Smith, Jan",
    "Smith, Jean",
    "Smith, Jo",
    "Smith, Jess",
    "Smith, Sandy",
    "Smith, Samantha",
    "Smith, Sally",
    "Smith, Sandra"
]

for line in input_file:
    if ("<div class=\"employeeName\">" in line):
        arr = line.split(",")
        left_side = arr[0].split(">")[0]
        right_side = arr[1].split("<")[1]
        name_index = random.randint(0, len(all_names)-1)
        name = all_names[ name_index ]
        line = left_side + ">" + name + "<" + right_side
        output_file.write( line )
        print( line )
    else:
        output_file.write( line )





# Randomize shift lengths

