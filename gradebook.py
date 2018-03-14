import re

def add_section(gb, section, weight):
  '''
  Add a section to the gradebook.
  '''
  gb[section] = { 'assignments':{}, 'weight': weight }


def add_assignment(gb, section, assignment, grade, notes=[]):
  '''
  Add an assignment to the gradebook
  '''
  if section not in gb:
    raise KeyError("Gradebook section %s does not exist"%(section,))
  gb[section]['assignments'][assignment] = { 'notes':notes, 'grade': grade}

  
def load_gradebook(fname):
  '''
  Load gradebook from a file.
  '''
  
  gb = {}
  section=None
  assignment=None
  #run through and parse the lines in the file
  file = open(fname)
  for line in file:
    #check for a new section
    m = re.search("^== *(.*?) ([0-9]+).*==$", line)
    if m is not None:
      section = m.group(1)
      add_section(gb, section, int(m.group(2)))
      continue

    #check for an assignment
    m = re.search("(^[^ ].*?)([0-9]+)$", line)
    if m is not None:
      assignment=m.group(1).strip()
      add_assignment(gb, section, assignment, int(m.group(2)))

      continue

    #check for a note
    m = re.search("^ +(.*)$", line)
    if m is not None:
      gb[section]['assignments'][assignment]['notes'].append(m.group(1).strip())
      continue

  return gb


def write_gradebook(fname, gb):
  '''
  Write the gradebook to a file.
  '''
  file = open(fname, "w")
  
  #go through each section
  for section, section_data in gb.items():
    #write the section to file
    file.write("== %s %d ==\n"%(section, section_data['weight']))

    #write all the assignments to the file
    for assignment, assignment_data in section_data['assignments'].items():
      file.write("%s %d\n"%(assignment, assignment_data['grade']))
      
      #write all the notes to the file
      for note in assignment_data['notes']:
        file.write("  %s\n"%(note,))
        
  file.close()
      

def grade_editor(gb, section, assignment, replace=False):
  '''
  Interactively enter a grade into the gradebook
  '''
  #verify that the section exists
  if section not in gb:
    raise KeyError("Gradebook section %s does not exist"%(section,))
  
  #check to see if the grade already exists, return if we need to
  if assignment in gb[section]['assignments'] and not replace:
    print("Grade for %s - %s already exists."%(section, assignment))
    return

  #get the grading notes
  notes=[]
  print("Enter grading notes.  Put a . on a line bye itself to exit.")
  line = input("> ")
  while line != '.':
    notes.append(line)
    line = input("> ")

  #get the final grade
  grade=int(input("Grade for %s > "%(assignment,)))

  #insert the assignment into the gradebook
  add_assignment(gb, section, assignment, grade, notes)

