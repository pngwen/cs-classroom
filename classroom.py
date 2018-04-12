from githubpy.github import GitHub
from pathlib import Path
from os import chdir,system,mkdir,path,getcwd

class Classroom:
  def __init__(self):
    '''
    Initialize the classroom, logging in to github and loading
    the roster.
    '''
    
    #initilize the 
    self.access_token = Path("access-token").read_text()
    self.gh = GitHub(access_token=self.access_token)
    self.owner = self.gh.user.get().login
    self.orgname = Path("org-name").read_text()

    #read the roster
    file = open("roster", "r")
    self.roster = [line.strip() for line in file]
    file.close()

    
  def project_list(self, name):
    '''
    Build a list of student project names.
    '''
    return ["%s-%s"%(name, student) for student in self.roster]

  
  def source_project_url(self, name):
    '''
    Build the source project url for an assignment
    '''
    return "git@github.com:%s/%s %s"%(self.orgname, name)
  
    
  def fetch_student_project(self, project, student, owner=None):
    '''
    Check for the existence of the project
    '''
    #preserve our original path
    original_dir = getcwd()

    #get the owner name
    if owner is None:
      owner = self.orgname

    #change into the sutdent-work directory and then pull the repo
    chdir('student-work')
    if not path.isdir(project):
      mkdir(project)
    chdir(project)
    if path.isdir("%s-%s"%(project, student)):
      chdir("%s-%s"%(project,student))
      system("git pull")
    else:
      system("git clone git@github.com:%s/%s-%s.git"%(owner, project, student))

    #return to the original directory
    chdir(original_dir)
