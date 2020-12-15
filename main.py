<<<<<<< HEAD
import os
import logging
import gspread
import telegram

from oauth2client.service_account import ServiceAccountCredentials
from telegram.ext import Updater, CommandHandler, MessageHandler,    Filters, InlineQueryHandler, Job, JobQueue,MessageHandler
from dotenv import load_dotenv
from datetime import datetime,time
from array import *

# parsing data first!!, into a 2D array
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Copy of Innopolis prayer timetable1").sheet1

sheet_data = sheet.get_all_values()
Prayer_name = sheet_data[0]
Prayer_status = sheet_data[1]



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue




def callback_alarm(context):
    context.bot.send_message(chat_id=(context.job.context[0]),
                             text=f"{Prayer_status[int(context.job.context[1])]} of {Prayer_name[int(context.job.context[1]) -1] if len(Prayer_name[int(context.job.context[1])]) == 0 else Prayer_name[int(context.job.context[1])]}  is NOW!")


def callback_timer(context):

    for i in range(10):
        x = i+2
        now = datetime.now()
        current_day = now.day
        current_array = sheet_data[current_day + 1]
        current_time = time(int(current_array[x].split(':')[0]) , int(current_array[x].split(':')[1]))
        j.run_once(callback_alarm, current_time , context=[context.job.context[1],x])



def start(update, context):
    row = ["chat_id = " , str(update.effective_chat.id)]
    sheet.insert_row(row,40)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Welcome in Innopolis Prayer time Bot!")
    for i in range(150):
        x = i+40
        if x > sheet.row_count:
            break
        j.run_daily(callback_timer,time(13,55),context=sheet.row_values(x))




start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

print(updater.bot)


updater.start_polling()
updater.idle()


=======
import os
import logging
import gspread

from oauth2client.service_account import ServiceAccountCredentials
from telegram.ext import Updater, CommandHandler, MessageHandler,    Filters, InlineQueryHandler, Job, JobQueue,MessageHandler
from dotenv import load_dotenv
from datetime import datetime,time
from pytz import timezone


# parsing data first!!, into a 2D array
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Copy of Innopolis prayer timetable1").sheet1

sheet_data = sheet.get_all_values()
Prayer_name = sheet_data[0]
Prayer_status = sheet_data[1]

#set the port number to listen in for the webhook.
PORT = int(os.environ.get('PORT', 5000))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue
moscow = timezone('Europe/Moscow')

def callback_alarm(context):
    context.bot.send_message(chat_id=(context.job.context[0]),
                             text=f"{Prayer_status[int(context.job.context[1])]} of {Prayer_name[int(context.job.context[1]) -1] if len(Prayer_name[int(context.job.context[1])]) == 0 else Prayer_name[int(context.job.context[1])]}  is NOW!")


def callback_timer(context):

    for i in range(10):
        x = i+2
        now = datetime.now()
        current_day = now.day
        current_array = sheet_data[current_day + 1]
        current_time = time(int(current_array[x].split(':')[0]) , int(current_array[x].split(':')[1]))
        j.run_once(callback_alarm, current_time,tzinfo=moscow , context=[context.job.context[1],x])



def start(update, context):
    row = ["chat_id = " , str(update.effective_chat.id)]
    sheet.insert_row(row,40)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Welcome in Innopolis Prayer time Bot!")
    for i in range(150):
        x = i+40
        if x > sheet.row_count:
            break
        j.run_daily(callback_timer,time(16,16),context=sheet.row_values(x))




start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

print(updater.bot)


#updater.start_polling()
updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
updater.bot.setWebhook('https://prayer-time-bot.herokuapp.com/' + TOKEN)

updater.idle()
<<<<<<< HEAD
>>>>>>> b13c850... Initial commit
=======


>>>>>>> 3e6b56e... connected google sheet by the bot
