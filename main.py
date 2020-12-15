import os
import logging
import gspread

from oauth2client.service_account import ServiceAccountCredentials
from telegram.ext import Updater, CommandHandler, MessageHandler,    Filters, InlineQueryHandler, Job, JobQueue,MessageHandler
from dotenv import load_dotenv
from datetime import datetime,time
from pytz import timezone
from dbhelper import DBHelper


# parsing data first!!, into a 2D array
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open("Copy of Innopolis prayer timetable1").sheet1

sheet_data = sheet.get_all_values()
Prayer_name = sheet_data[0]
Prayer_status = sheet_data[1]

#preparing for the database to store the  userids
db = DBHelper()


#set the port number to listen in for the webhook.
PORT = int(os.environ.get('PORT', 5000))

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
load_dotenv()

TOKEN = '1155106665:AAGFXra4l-XnHa2lIBwZlWLRFVu5EDpYd4c'
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
j = updater.job_queue
moscow = timezone('Europe/Moscow')

def callback_alarm(context):
    context.bot.send_message(chat_id=(context.job.context[0]),
                             text=f"{Prayer_status[int(context.job.context[1])]} of {Prayer_name[int(context.job.context[1]) -1] if len(Prayer_name[int(context.job.context[1])]) == 0 else Prayer_name[int(context.job.context[1])]}  is NOW!")


def callback_timer(context):
    for i in range(10):
        current_array = sheet_data[datetime.now().day + 1]
        current_time = time(int(current_array[i+2].split(':')[0]) , int(current_array[i+2].split(':')[1]))
        print(current_time)

        j.run_once(callback_alarm, current_time,tzinfo=moscow , context=[context.job.context[1],i+2])



def start(update, context):
    new_id = update.effective_chat.id
    db.add_id(new_id)
    print(db)
    context.bot.send_message(chat_id=new_id,
                             text="Welcome in Innopolis Prayer time Bot!")
    print(datetime.now())
    j.run_daily(callback_timer,datetime.now(),context=new_id)



def main():
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    print(updater.bot)
    # updater.start_polling()
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://prayer-time-bot.herokuapp.com/' + TOKEN)

    updater.idle()





if __name__ == '__main__':
    db.setup()
    main()