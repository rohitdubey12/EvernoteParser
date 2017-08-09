#!/usr/bin/python
import subprocess,shlex,time
from datetime import datetime, timedelta


tag="TODO"
notebook="Meeting_Notes"
notebook_todo="My_Plate"
note_todo="TODO"
content_marker="----------------- CONTENT -----------------"
start_date=(datetime.today() - timedelta(days=30)).strftime("%d.%m.%Y")
end_date=time.strftime("%d.%m.%Y")
#end_date=(datetime.today() - timedelta(days=1)).strftime("%d.%m.%Y")
#cmd_find="geeknote find --search '"+tag+"' --notebooks '"+notebook+"' --content-search --date '"+start_date+"-"+end_date+"' --exact-entry"
cmd_find="geeknote find --search '"+tag+"' --notebooks '"+notebook+"' --content-search --date '"+end_date+"' --exact-entry"
cmd_show="geeknote show"
cmd_grep="grep 'Linux'"
cmd_find_todo="geeknote find --search '"+note_todo+"' --notebooks '"+notebook_todo+"'"
find_str="Total found: "
TODO="Linux"
TODO_LIST="-----------------------------Action items for "+ end_date+":\n"
LOG_TAG="=====[INFO@:"+str(datetime.today())+"]"


print LOG_TAG+"\n\n\n\n----------------------------INIT-----------------------------"
print LOG_TAG+"Checking for notes with action items...."
raw_res=subprocess.check_output(shlex.split(cmd_find))


#TODO if raw_res contains "Notes have not been found"

if find_str in raw_res:
	number= int(raw_res[raw_res.find(find_str)+13:].splitlines()[0])
	
print LOG_TAG+"Found "+str(number)+" notes."

print LOG_TAG+"extracting action items..."

for x in range(1,number+1):
	raw_notes=subprocess.check_output(shlex.split(cmd_show + ' '+ str(x)))
	
	
notes_lines = raw_notes.splitlines()

for line in notes_lines:
		if tag in line:
			TODO_LIST+=line+"\n"
			
TODO_LIST+="\n"

print LOG_TAG+"Fetching TODO LIST..."
subprocess.check_output(shlex.split(cmd_find_todo))
content=subprocess.check_output(shlex.split(cmd_show+' 1'))

original_content=content[content.find(content_marker)+len(content_marker):]

new_content=(original_content+TODO_LIST).replace("\n\n","\n").replace("'","^").replace("[","{").replace("]","}")

print LOG_TAG+"Adding action items to the TODO list"
cmd_edit="geeknote edit '"+note_todo+"' --content '"+new_content+"'"
output=subprocess.check_output(shlex.split(cmd_edit))
print LOG_TAG+"Done! See you tomorrow\n\n"