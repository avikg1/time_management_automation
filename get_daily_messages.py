from imessage_reader import fetch_data
import sys
import subprocess
import os

DB_PATH = os.path.expanduser("~/Library/Messages/chat.db")
WRITE_SCRIPT_PATH = os.path.expanduser("~/Desktop/projects/time_management_sheet/new_entry.sh")
DELETE_SCRIPT_PATH = ""

def get_date(message):
        #Get date of message in form yyyy-mm-dd
        return message[2][:10]

def get_sender(message):
    #Get phone number of message sent
    return message[0]

def get_words(message):
    #Get an array of each word contained in the message
    return message[1].split()

def modify_date(date):
    #change from YYYY-MM-DD to MM-DD-YYYY
    yyyy = date[0:4]
    mm = date[5:7]
    dd = date[8:]
    return (mm + '-' + dd + '-' + yyyy)

def edit_time(time, is_pm):
    #make sure hours have two digits
    #and adjust to pm if obvious user meant to do that
    if (time[1] == ':'):
        time = '0' + time

    try:
        hour = int(time[:2])
    except:
        return time

    if (hour < 12 and is_pm):
        time = str(hour + 12) + time[2:]
    return time

def determine_time_spent(start, end):
    try:
        hh_1 = int(start[0:2])
        mm_1 = int(start[3:])

        hh_2 = int(end[0:2])
        mm_2 = int(end[3:])

        return str(60*(hh_2 - hh_1) + (mm_2 - mm_1))
    except ValueError:
        return "NA"

def script_plus_args(path, date, args, is_pm):
    #prepare list to pass to subprocess.run
    new_date = modify_date(date)

    #Modify time input to account for likely user error
    new_args = args
    new_args[1] = edit_time(new_args[1], is_pm)
    new_args[2] = edit_time(new_args[2], is_pm)
    
    #calculate and add time spent
    new_args.append(determine_time_spent(new_args[1], new_args[2]))
    
    return [path] + [new_date] + new_args
    
def main():
    fd = fetch_data.FetchData(DB_PATH)
    messages = fd.get_messages()

    #When you send yourself a message, 2 show up, so this avoids that
    skipNext = False

    #This will track if it's pm yet
    is_pm = False

    for message in messages:
        if (skipNext):
            skipNext = False
            continue
        skipNext = False

        if (get_date(message) == sys.argv[1] and get_sender(message) == '+16123835311'):
            skipNext = True
            in_stuff = get_words(message)
            if (len(in_stuff[0]) > 1 and in_stuff[0:2] == '//'):
                continue
            if (in_stuff[0] in ["noon", "Noon"]):
                is_pm = True
            elif (in_stuff[0] in ["delete", "Delete"]):
                continue
                in_stuff = in_stuff[1:]        
                subprocess.run(script_plus_args(DELETE_SCRIPT_PATH, get_date(message), in_stuff, is_pm), capture_output=True, text=True)
            else:
                subprocess.run(script_plus_args(WRITE_SCRIPT_PATH, get_date(message), in_stuff, is_pm), capture_output=True, text=True)

if (__name__ == '__main__'):
    main()
