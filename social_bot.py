#smtp: simple Mail Transfer Protocol
import smtplib, random, datetime, calendar, imapclient, pyzmail

#Populate User-Specific Variables CHANGE AS REQUIRED - NOTE the password must be an app password. See Google documentation for more info: https://support.google.com/accounts/answer/185833?hl=en

print('Please enter email address to be used:')
emailAddress = input()

print('Now enter the app password for this account. NOTE: the password must be an app password. See Google documentation for more info: https://support.google.com/accounts/answer/185833?hl=en')
password = input()

recipientList = ['Joe.Bloggs123@gmail.com']

#populate datetime and calendar variables
today = datetime.date.today()
day, month, year = today.day, today.month, today.year
cal = calendar.monthcalendar(year,month)
monthName = calendar.month_name[month]

#Define Functions

#Define function to determine suffix to day of the month
def findDaySuffix(strDay):
    lastNumber = strDay[len(strDay)-1:len(strDay)]
    
    if lastNumber == "1":
        suffix = "st"
    elif lastNumber == "2":
        suffix = "nd"
    elif lastNumber == "3":
        suffix = "rd"
    else:
        suffix = "th"

    return suffix
    
#Define function to create email and send email. The section creating the message will loop until the user indicates they are happy with the message.
def createEmail():
    #create message componants lists with day of week index as value
    opener = ['Hi Guys,','Hello All,','Howdy!']
    activity = {'Sailsbury Arms for 2-4-1 pizza on Monday ':0, 'Tenpin Bowling on Tuesday ': 1,'The Wrestlers Arms on Wednesday ': 2,'Calverlies Brewery on Thursday ': 3, 'Thirsty Chesterton Road on Friday ': 4}

    while(1 < 2):
        #random choice from lists
        chosenOpener = random.choice(list(opener))
        chosenActivity = random.choice(list(activity.keys()))

        #find date for activity - (last occurance of relevent day of the month)
        dayIndex = activity[chosenActivity]
        day = cal[-2][dayIndex] #returns the date of the last occurence of day index. There may not be an occurance of a specific day in the last week of the month but definetly will be in the penultimate.

        strDay = str(day)
        eventSuffix = findDaySuffix(strDay)

        #Replies will be totalled 2 weeks prior to make booking
        strReplyDay = str(day - 10)
        replySuffix = findDaySuffix(strReplyDay)

        #concatenate message componants and check with user
        message = chosenOpener + "\n\nThis month's social will be at " + chosenActivity + strDay + eventSuffix + " " + monthName + ". If you would like to join, please reply to this email by " + strReplyDay + replySuffix + " " + monthName + ". If you don't want to attend, please do not reply at all.\n\n\n[NOTE: This process is automated so late replies won't be considered]. \n\nBeep Boop,\nHorizon Social Bot"
        print("Message genereated: " + message + "\n")
        print("Would you like to proceed with the message genereated?(Y/N) - N to generate new message\n")
        if input() == "Y":
            break

    #Initiate connection and send email.

    #create connection object
    conn = smtplib.SMTP('smtp.gmail.com', 587)

    #start connections with .ehlo() method
    conn.ehlo()
    conn.starttls()
    conn.login(emailAddress, password)

    #Send each to each address in list and end connection

    for recipient in recipientList:
        conn.sendmail(emailAddress, recipient, 'Subject: ' + monthName + ' social!\n\n ' + message)

    conn.quit()

def canvasResponces():

    headCount = 0
    
    #initate connection
    conn = imapclient.IMAPClient('imap.gmail.com', ssl = True)
    conn.login(emailAddress, password)
    
    #search inbox for and count replies to emails generated and sent in current month
    conn.select_folder('INBOX', readonly = True)
    UIDs = conn.search([b'SINCE', datetime.date.today().replace(day=1)])
    for UID in UIDs:
        rawMessage = conn.fetch([UID], ['BODY[]', 'FLAGS'])
        message = pyzmail.PyzMessage.factory(rawMessage[UID][b'BODY[]'])
        print(message.get_subject() + ': ' + monthName + ' social!')
        if message.get_subject() == monthName + ' social!':
            headCount += 1

    #Print out tally and terminate connection
    print(str(headCount) + " people have responded to this months email.")
    conn.logout()
    
#Print out user instructions describing available functions and call selection
print('Hello and welcome to Gmail Social Bot! Would you like to send a new email or tally repsonses? (Create/Tally)?')

while(1 < 2):
    repsonce = input()
    if repsonce == 'Create':
        createEmail()
        break
    elif repsonce == 'Tally':
        canvasResponces()
        break
    else:
        print("I'm sorry I don't recognise that entry! Please enter either 'Create' or 'Tally'")
        