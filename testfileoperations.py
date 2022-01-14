from datetime import datetime
from github import Github


user = "RoboticsLogger"
with open("password.txt", "r") as f:
    password = f.readline()

now = datetime.now()
date = now.strftime("%Y-%m-%d")
day = now.weekday()
day_of_the_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
commit_message = "Updated " + date + " (" + day_of_the_week[day] + ")"

g = Github(password)
repo = g.get_user().get_repo('RoboticsLog') # repo name

all_files = []
contents = repo.get_contents("")
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        file = file_content
        all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

with open('RoboticsHourLog.csv', 'r') as file:
    content = file.read()

# Upload to github
git_prefix = ''
git_file = git_prefix + 'RoboticsHourLog.csv'
if git_file in all_files:
    contents = repo.get_contents(git_file)
    repo.update_file(contents.path, commit_message, content, contents.sha, branch="main")
    print(git_file + ' UPDATED')
else:
    repo.create_file(git_file, commit_message, content, branch="main")
    print(git_file + ' CREATED')