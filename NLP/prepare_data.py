import utils

logs = open('chat_logs.txt').readlines()

file = open("chat_logs_processed.txt","w") 

for line in logs:
    row = line.split(':')
    if(len(row)>3):
        if(('bot' not in row[2]) and ('twitchnotify' not in row[2])):
            message = utils.process(row)
            if(len(message.split(' '))>1):
                file.write(message)
