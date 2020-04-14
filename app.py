import logging

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

from mymod import (all_slot, cancel_booking ,current_bookings, check_current, check_main, current_date_func, curent_date_main, check_list, banneduser, availbooking, check_user, gsr_booking, gsr_main, gsr_function, gsr_slot, check_slot)


#other library 
from credentials import bot_token, APP_URL 
from datetime import datetime # to check date later on 
from flask import Response, Flask, request
import os 

app = Flask(__name__)
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

DATE, FACULTY, GETAVAILBOOKING= range(3)
BOOKINGDATE, BOOKINGFACULTY, BOOKINGGSR, BOOKINGSLOT, BOOKING, BOOKINGCONFIRMED= range(6)
CANCELASK, CONFIRMCANCEL, CANCELLED = range(3)
USERDETAIL = range(1)

#dictionary to store data temporary
temp = {'date': 'placeholder', 'faculty' : 'placeholder1', 'chat_id' : 'placeholder2', 'function': 'checkavail'} # for get bookings
booking= {'date': 'placeholder', 'faculty' : 'placeholder1', 'chat_id' : 'placeholder2', 'function' : 'booking'} #for getting gsr from the particular date user chooses  


querybookingref = {'chatid' : 'placeholder1'}
cancellation = {'chatid' : 'placeholder1', 'bookingref': 'placeholder2'}
details = {'chat_id' : 'placeholder1', 'function': 'checkuser'}

banned = {'chat_id' : 'placeholder1', 'function' : 'checkexist'}

a = {} 

#reminder here : to clean the value of the key when user cancel the transaction halfway / press other menu button - error handling  
#end

#to display the main menu 
def start(update, context): #/detial tbc
    update.message.reply_text(
        '''Welcome to SMU - ASK.GSR booking, your one stop GSR booking platform\n
        This is the Main menu:\n
        
        To check your details: /userdetails \n 
        To check available GSR: /availgsr \n
        To book a GSR: /createbooking \n
        To cancel GSR booking: /cancelbooking \n
        To cancel chat / If you face any technical difficulties: /cancel \n
        To start the chat again: /start\n
    
        In case of any difficulties:\n
        Please contact askgsrhelp@gmail.com\n
        ''')
    return ConversationHandler.END


def availgsr(update, context):
    user = update.message.from_user
    banned['chat_id'] = user['id']
    print (banned)
    reply = banneduser(banned) #return reply  --> to check if user is banned 

    if reply == "Not from SMU":
        update.message.reply_text('You are not from SMU')
        start(update, context)
        return ConversationHandler.END
    elif reply == "Banned":
        update.message.reply_text('You are banned')
        start(update, context)
        return ConversationHandler.END
    else:
        reply_keyboard = [['Yes', 'No']]
        update.message.reply_text(
            'Do you want to check available GSR ?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return DATE


def key_date(update, context): #middle man to check if user click on yes , if yes give keyboard for date 
    user = update.message.from_user
    logger.info("Choice of %s: %s", user.first_name, update.message.text)
    if update.message.text == 'Yes':
        # ask_date(update, context)
        # user = update.message.from_user
        current_date = current_date_func()
        # reply_keyboard = [current_date]
        reply_keyboard = [current_date[:int(round(len(current_date)/2))] , current_date[int(round(len(current_date)/2)):]]
        update.message.reply_text(
            'Please choose the date that you want to see the bookings',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return FACULTY
    else:
        update.message.reply_text('See you around, bringing u back to main menu', reply_markup=ReplyKeyboardRemove())
        start(update,context)
        return ConversationHandler.END
    # return PHOTO

def key_fac(update, context): 
    user = update.message.from_user
    # print (user)
    text = update.message.text
    # print (text)
    # logger.info("Choice of %s: %s", user.first_name, update.message.text)

    if text == datetime.strptime(text, "%Y-%m-%d").strftime('%Y-%m-%d'):
        logger.info("Choice of %s: %s", user.first_name, update.message.text)
        temp['date'] = text
        print (temp)
        update.message.reply_text('You have chosen date: {}!'.format(text), reply_markup=ReplyKeyboardRemove())
        

        reply_keyboard = [['SIS']]
        update.message.reply_text(
            'Please key in the faculty ',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        # user = update.message.from_user
        text = update.message.text
        print (text)
        # logger.info("Choice of %s: %s", user.first_name, update.message.text)
        
        return GETAVAILBOOKING

    else:
        logger.info("Choice of %s: %s", user.first_name, update.message.text)
        reply = 'Please key in the DATE Properly'
        update.message.reply_text(reply, reply_markup=ReplyKeyboardRemove())
        return FACULTY 


def get_avail_booking(update, context): #diplay the avail gsr over here 
    user = update.message.from_user
    print (user)
    print (user['id'])
    text = update.message.text
    if text == 'SIS':
        temp['faculty'] = text
        temp['chat_id'] = user['id']
        print (temp)
        update.message.reply_text('You have keyed in faculty!', reply_markup=ReplyKeyboardRemove())
        update.message.reply_text('Here is the available GSR for booking, press /createbooking to create booking or \n /start to go back to main menu!', reply_markup=ReplyKeyboardRemove())

        reply = availbooking(temp)

        update.message.reply_text(reply , reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        return GETAVAILBOOKING


def createbooking(update, context):
    user = update.message.from_user
    banned['chat_id'] = user['id']
    print (banned)
    reply = banneduser(banned) #return reply  --> to check if user is banned 

    if reply == "Not from SMU":
        update.message.reply_text('You are not from SMU')
        start(update, context)
        return ConversationHandler.END
    elif reply == "Banned":
        update.message.reply_text('You are banned')
        start(update, context)
        return ConversationHandler.END
    else:
        reply_keyboard = [['Yes', 'No']]
        update.message.reply_text(
            'Do you want book GSR ?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return BOOKINGDATE



def booking_date(update, context):
    user = update.message.from_user
    logger.info("Choice of %s: %s", user.first_name, update.message.text)
    if update.message.text == 'Yes':

        current_date = current_date_func()
        # reply_keyboard = [current_date]
        reply_keyboard = [current_date[:int(round(len(current_date)/2))] , current_date[int(round(len(current_date)/2)):]]
        update.message.reply_text(
            'Please select the date that you want to book',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard =True ,one_time_keyboard=True))

        return BOOKINGFACULTY
    else:
        update.message.reply_text('See you around, bringing u back to main menu', reply_markup=ReplyKeyboardRemove())
        start(update,context)
        return ConversationHandler.END

def booking_faculty(update, context):

    user = update.message.from_user
    text = update.message.text

    # if text == datetime.strptime(text, "%Y/%m/%d").strftime('%Y/%m/%d'):
    logger.info("Choice of %s: %s", user.first_name, update.message.text)
    booking['date'] = text
    print (booking)
    update.message.reply_text('You have keyed in the date!', reply_markup=ReplyKeyboardRemove())

    reply_keyboard = [['SIS']]
    update.message.reply_text(
        'Now, please key in the faculty',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    text = update.message.text
    
    return BOOKINGGSR

    # else:
    #     logger.info("Choice of %s: %s", user.first_name, update.message.text)
    #     reply = 'Please key in the DATE Properly!'
    #     update.message.reply_text(reply, reply_markup=ReplyKeyboardRemove())
    #     return None 

def booking_gsr(update, context):
    user = update.message.from_user

    text = update.message.text
    # if text == 'SIS':
    booking['faculty'] = text
    booking['chat_id'] = user['id']
    print (booking)
    update.message.reply_text('You have chosen Faculty: {} !'.format(text), reply_markup=ReplyKeyboardRemove())
    
    everyslot = all_slot()
    
    slotgsr = gsr_slot(booking) # to show slot and gsr 

    availgsr = gsr_function(booking) #to be replace with the api show in keyboard format 
    reply_keyboard = [availgsr] #to be replace with the api show in keyboard format  
    #show the slot and GSR TGT in text format

    update.message.reply_text(everyslot, parse_mode="Markdown")

    update.message.reply_text(slotgsr) #text msg 

    update.message.reply_text(
        'Now, please choose the GSR',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard,resize_keyboard =True , one_time_keyboard=True))
    return BOOKINGSLOT


def booking_slot(update,context):
    text = update.message.text
    print (text)
    booking.update({'gsr_no': text})

    update.message.reply_text('You have chosen {} !'.format(text), reply_markup=ReplyKeyboardRemove())
    update.message.reply_text(
        'Now pls Key in the Slot that you want to book, in 3 slot only and make sure that the numbers are consecutive and in this format! e.g. 1,2,3,')
    return BOOKING 



def booking_confirmation(update, context):

    text = update.message.text
    print (text)

    if text == '/start':
        start(update, context)
        return ConversationHandler.END
    elif text == '/cancel':
        cancel(update, context)
        return ConversationHandler.END
    elif text == '/cancelbooking':
        cancelbooking(update, context)
        return ConversationHandler.END
    elif text == '/createbooking':
        createbooking(update, context)
        return ConversationHandler.END
    elif text == '/availgsr':
        availgsr(update, context)
        return ConversationHandler.END
    elif text == '/userdetails':
        userdetails(update, context)
        return ConversationHandler.END
    else: 
        reply = check_list(text) #check user input 
        print (booking)
    # booking = {'date': '2020-04-08', 'faculty': 'SIS', 'chat_id': 281997556, 'function': 'booking', 'gsr_no': 'GSR 2-5'}

        d = check_slot(booking) #
        e = booking.get('gsr_no') #get from user input (from dict)

        real = d[e] #e.g. [4, 5, 10, 11, 12]

        b = 0
        if reply == False: 
            update.message.reply_text('Please key in consecutive numbers and in this format! e.g. 1,2,3')
            return BOOKING
        else:
            l = [int(s) for s in reply.split(',')] 
                   
            for i in l:
                if i in real:
                    b += 0
                else:
                    b += 1
            if b > 0:
                update.message.reply_text('Please key in within the slot! ')
                return BOOKING 
            else:
                booking['slots'] = l
                print (booking)
                reply_keyboard = [['Yes', 'No']]
                slot = booking['slots']
                gsr = booking['gsr_no']
                date = booking['date']
                faculty = booking['faculty']
                update.message.reply_text(
                    'Confirm booking of {} at {} on {}, Time slot = {} ?'.format(gsr, faculty, date, slot), 
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return BOOKINGCONFIRMED


def booking_confirmed(update, context):
    text = update.message.text
    print (text)
    if text == 'Yes':
        a = booking['gsr_no']
        a = a[4::]
        booking['gsr_no'] = a
        gsr_booking(booking) 
        start(update, context)
        return ConversationHandler.END
    else:
        #slot not avalable ? 
        update.message.reply_text('''You have cancelled your booking, bringing you back to main menu''',
        reply_markup=ReplyKeyboardRemove())
        start(update, context)
        return ConversationHandler.END

#cancel gsr booking 
def cancelbooking(update, context):
    #check whether banned 
    user = update.message.from_user
    banned['chat_id'] = user['id']
    print (banned)
    reply = banneduser(banned) #return reply  --> to check if user is banned 

    if reply == "Not from SMU":
        update.message.reply_text('You are not from SMU')
        start(update, context)
        return ConversationHandler.END
    elif reply == "Banned":
        update.message.reply_text('You are banned')
        start(update, context)
        return ConversationHandler.END
    else:
        reply_keyboard = [['Yes', 'No']]
        update.message.reply_text(
            'Do you want to cancel booking?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return CANCELASK

def askcancel(update,context):
    text = update.message.text    
    if text == 'Yes': 
        user = update.message.from_user

        querybookingref['chatid'] = user['id'] #chat id 
        print (cancellation)
        bookingref = check_current(querybookingref)
        #api codes will be here to query the bookings of the user
        # if the user have no booking, will have an tell user he have no booking then send him back to menu
        if len(bookingref) != 0:
            reply_keyboard = [bookingref] #tb change 
            update.message.reply_text(
                'Please select the booking reference you like to cancel',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return CONFIRMCANCEL
        else:
            update.message.reply_text('You do not have any booking... bringing u back to main menu', reply_markup=ReplyKeyboardRemove())
            start(update, context)
            return ConversationHandler.END
    else:
        update.message.reply_text('See you around, bringing u back to main menu', reply_markup=ReplyKeyboardRemove())
        start(update, context)
        return ConversationHandler.END


def askcancelfinal(update,context):
    user = update.message.from_user
    text = update.message.text

    if text == '/start':
        start(update, context)
        return ConversationHandler.END
    elif text == '/cancel':
        cancel(update, context)
        return ConversationHandler.END
    elif text == '/cancelbooking':
        cancelbooking(update, context)
        return ConversationHandler.END
    elif text == '/createbooking':
        createbooking(update, context)
        return ConversationHandler.END
    elif text == '/availgsr':
        availgsr(update, context)
        return ConversationHandler.END
    elif text == '/userdetails':
        userdetails(update, context)
        return ConversationHandler.END
    else: 
        try: 
            cancellation['chatid'] = user['id']
            cancellation['bookingref'] = int(text) 
            print (cancellation)
            reply_keyboard = [['Yes', 'No']]

            update.message.reply_text(
                'Please confirm your booking cancellation?',
                reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
            return CANCELLED

        except: 
            update.message.reply_text('Please choose what is on the given keyboard only')
            return CONFIRMCANCEL 

def finalcancel(update, context): 
    #collect dict and post the dictionary to delete API 
    #booking {} deleted. format 
    text = update.message.text
    if text == 'Yes':
        #send api to cancel booking 
        cancel_booking(cancellation)

        update.message.reply_text('''You have successfully cancelled your booking, bringing you back to main menu''',
        reply_markup=ReplyKeyboardRemove())
        start(update, context)
        return ConversationHandler.END
    else: 
        update.message.reply_text('''You have cancelled your request, bringing you back to main menu''',
        reply_markup=ReplyKeyboardRemove())
        start(update, context)
        return ConversationHandler.END

def userdetails(update, context):
    user = update.message.from_user
    banned['chat_id'] = user['id']
    print (banned)
    reply = banneduser(banned) #return reply  --> to check if user is banned 

    if reply == "Not from SMU":
        update.message.reply_text('You are not from SMU')
        start(update, context)
        return ConversationHandler.END
    elif reply == "Banned":
        update.message.reply_text('You are banned')
        start(update, context)
        return ConversationHandler.END
    else:
        reply_keyboard = [['Yes', 'No']]
        update.message.reply_text(
            'Do you want to check your user detail?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return USERDETAIL 


def sendetails(update, context):
    text = update.message.text
    if text == 'Yes':
        user = update.message.from_user
        details['chat_id'] = user['id']
        print (details)

        reply = check_user(details)


        update.message.reply_text('''Here is your user details, press /start to go back to main menu''',
        reply_markup=ReplyKeyboardRemove())
        update.message.reply_text(reply)

        #send api get request here
        return ConversationHandler.END
    else:
        update.message.reply_text('See you around, bringing u back to main menu', reply_markup=ReplyKeyboardRemove())
        start(update, context)
        return ConversationHandler.END

#don touch below 
def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
#end 

#main - brain child 
def main():

    TOKEN = bot_token
    PORT = int(os.environ.get('PORT', '8443'))
    updater = Updater(TOKEN, use_context=True)

    updater.start_webhook(listen="0.0.0.0",
                        port=PORT,
                        url_path=TOKEN)

    updater.bot.set_webhook(APP_URL + TOKEN)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    #my library
    gsrmain = gsr_main(booking)
    current_date_main = curent_date_main() #for current data 
    # ref_booking = check_main(querybookingref) #check cancelled booking
     # to display avial gsr in keyboard  

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('availgsr', availgsr)],

        states={
            DATE: [MessageHandler(Filters.regex('^(Yes|No)$'), key_date)],  #middle man check choise

            FACULTY:[MessageHandler(Filters.regex(current_date_main), key_fac)],

            GETAVAILBOOKING : [MessageHandler(Filters.regex('^(SIS)$'), get_avail_booking)],

        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    #ask booking
    conv_handler_bookings = ConversationHandler(
        entry_points=[CommandHandler('createbooking', createbooking)],
        
        states={  
            BOOKINGDATE: [MessageHandler(Filters.regex('^(Yes|No)$'), booking_date)],
            BOOKINGFACULTY:[MessageHandler(Filters.regex(current_date_main), booking_faculty)],
            BOOKINGGSR: [MessageHandler(Filters.regex('^(SIS)$'), booking_gsr)],

            BOOKINGSLOT: [MessageHandler(Filters.regex(gsrmain), booking_slot)], #over ehre 

            BOOKING: [MessageHandler(Filters.text, booking_confirmation)],
            BOOKINGCONFIRMED: [MessageHandler(Filters.regex('^(Yes|No)$'), booking_confirmed)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    #cancel 
    conv_handler_cancel= ConversationHandler(
        entry_points=[CommandHandler('cancelbooking', cancelbooking)],
        
        states={  
            CANCELASK: [MessageHandler(Filters.regex('^(Yes|No)$'), askcancel)],
            CONFIRMCANCEL:[MessageHandler(Filters.text, askcancelfinal)], #placeholder
            CANCELLED: [MessageHandler(Filters.regex('^(Yes|No)$'), finalcancel)]
        },
# regex(ref_booking)
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    conv_handler_details= ConversationHandler(
        entry_points=[CommandHandler('userdetails', userdetails)],
        
        states={  
            USERDETAIL: [MessageHandler(Filters.regex('^(Yes|No)$'), sendetails)],
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    #asking bookings phase  
    dp.add_handler(CommandHandler('start', start)) #display the main menu  
    dp.add_handler(conv_handler) # for SEEING AVAILABLE GSR BOOKINGS  
    dp.add_handler(conv_handler_bookings) # for Booking of GSR
    dp.add_handler(conv_handler_cancel) #for cancellationg of bookings 
    dp.add_handler(conv_handler_details) #for checking of user details 

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
