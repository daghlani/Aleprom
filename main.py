#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import threading
import os.path
from DB.tables import User, Session
import config
from sqlalchemy import exc
from messages.messages import BotMSG, ErrLogs, priority_map
from telegram import (ReplyKeyboardMarkup, Bot)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from webhook.hook import app

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger()

UPDATEUSER, SEVERITY, END = range(3)


def read_file():
    try:
        if not os.path.isfile('ids.txt'):
            with open('ids.txt', 'w') as f:
                f.close()
        with open('ids.txt') as f:
            ids = f.readlines()
    except Exception as err:
        logger.error(err)
        return []
    return ids


def update_file(new_id):
    ids = read_file()
    try:
        if len(ids) == 1:
            if new_id not in ids[0].split(','):
                ids.append(new_id)
        else:
            ids.append(new_id)
        f = open('ids.txt', 'w')
        f.write(','.join(ids))
        f.close()
    except Exception as err:
        logger.error(err)

def validate(bot, update):
    logger.info("validate called")
    user = update.message.from_user
    txt = 'نام: {} \n' \
          'نام کاربری: {} \n' \
          'شماره آیدی: [{}]({}) \n'
    try:
        user_obj = User(bale_id=user.id, name=user.first_name, username=user.username)
        session = Session()
        session.add(user_obj)
        session.commit()
        bot.send_message(chat_id=config.admin_id, text=txt.format(user.first_name, user.username, user.id, user.id))
        bot.send_message(chat_id=config.admin_id, text='{}'.format(user.id))
        update.message.reply_text("{}".format(BotMSG.get_id))
    except exc.IntegrityError:
        logging.info(ErrLogs.record_exist)
        update.message.reply_text("{}".format(ErrLogs.record_exist))

    return ConversationHandler.END


def it_is_valid(bot, update):
    logger.info("it_is_valid called")
    user = update.message.from_user
    if str(user.id) == config.admin_id:
        update.message.reply_text(
            'what is id?'
        )
        return SEVERITY


def severity(bot, update, user_data):
    reply_keyboard = [['INFO', 'WARNING', 'ERROR', 'CRITICAL']]
    logger.info("severity called")
    req_id = update.message.text
    user_data['req_id'] = req_id
    update.message.reply_text('please set the minimum severity of user to receive alerts.',
                              reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard))
    return UPDATEUSER


def update_user(bot, update, user_data):
    logger.info("update_user called")
    severity_ = update.message.text
    req_id = user_data['req_id']
    session = Session()
    user_obj = session.query(User).filter_by(bale_id=req_id).first()
    if severity_ in ['INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        priority = 0
        if severity_ == 'INFO':
            priority = 1
        elif severity_ == 'WARNING':
            priority = 2
        elif severity_ == 'ERROR':
            priority = 3
        elif severity_ == 'CRITICAL':
            priority = 4
        user_obj.st_change(priority)
        user_obj.is_valid = True
        session.commit()
        bot.send_message(chat_id=user_obj.bale_id, text='you will be notified for [{}]'.format(priority_map[severity_]))
        update.message.reply_text('Thank you! it\'s Done. Selected priority is: [{}]'.format(priority_map[severity_]))
        return ConversationHandler.END
    else:
        update.message.reply_text('please chose one of supported options.')


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.')

    return ConversationHandler.END


def error(bot, update):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, update.message)


def main():
    x = threading.Thread(target=app.run)
    x.start()
    # Create the Updater and pass it your bots token.
    bot = Bot(token=config.token,base_url=config.base_url,base_file_url=config.base_file_url)
    updater = Updater(bot=bot)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[
            # CommandHandler('start', start),
            CommandHandler('alid__validate_users__1402', validate),
            CommandHandler('it_is_valid', it_is_valid)
        ],
        states={
            SEVERITY: [RegexHandler(pattern='\d', callback=severity, pass_user_data=True)],
            UPDATEUSER: [MessageHandler(Filters.text, callback=update_user, pass_user_data=True)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(poll_interval=2)
    updater.idle()


if __name__ == '__main__':
    main()
