import logging
from datetime import datetime

from dateutil.tz import tzutc

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler


from db import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

db = init_firebase('todobotfirebase-firebase-adminsdk-npghl-cdadbeff71.json')
task = Task()

NAME, DESCRIPTION, DATE, TIME = map(chr, range(4))
UPDATE_GET, UPDATE_DESCRIPTION, UPDATE_DATE, UPDATE_TIME = map(chr, range(4, 8))
DELETE_GET = map(chr, range(8, 9))
DONE_GET = map(chr, range(9, 10))


def start(update, context):
    add_user(update.message.from_user.id, db)
    update.message.reply_text('Бот запущен!\nДобавте ему свои задачи, и он напомнит вам, если вы не сделали их вовремя \
								\nиспользуйте /help для просмотра доступных команд')


def help(update, context):
    update.message.reply_text("Список команд бота:\n/addTask - добавить новую задачу \
								\n/editTask - изменить описание и время выполнения существующей задачи \
								\n/delTask - удалить задачу \
								\n/doneTask - пометить задачу как выполненную \
								\n/getAll - получить список всех задач")


def unknown(update, context):
    update.message.reply_text('Неизвестная команда\nИспользуйте /help для просмотра доступных команд')


def add_task(update, context):
    update.message.reply_text("Введите название задачи\nДля отмены добавления используйте команду /cancel")
    return NAME


def name(update, context):
    task.user = update.message.from_user.id
    task.name = update.message.text
    update.message.reply_text("Введите описание задачи")
    return DESCRIPTION


def description(update, context):
    task.description = update.message.text
    update.message.reply_text('Введите дату, до которой задача должна быть выполнена в формате дд.мм.гггг')
    return DATE


def date(update, context):
    date = update.message.text
    try:
        valid_date = datetime.strptime(date, '%d.%m.%Y')
        if valid_date.date() >= datetime.today().date():
            task.date = valid_date
            update.message.reply_text('Введите время, до которого задача должна быть выполнена в формате чч.мм')
            return TIME
        else:
            update.message.reply_text('Этот день уже прошел!!!\nВведите дату не раньше чем сегодня')
            return DATE
    except ValueError:
        update.message.reply_text('Некорректный формат даты!!!\nВведите дату в формате дд.мм.гггг')
        return DATE


def time(update, context):
    time = update.message.text
    try:
        date_str = task.date.strftime('%d.%m.%Y') + '/' + time
        valid_time = datetime.strptime(date_str, '%d.%m.%Y/%H.%M')
        if valid_time >= datetime.today():
            tzut = tzutc()
            task.date = valid_time.replace(tzinfo=tzut)
            add_task_firebase(task, db)
            update.message.reply_text('Задача успешно добавлена')
            return ConversationHandler.END
        else:
            update.message.reply_text(
                'Время, до которого задача должна быть выполнена, должно быть не меньше чем текущее!\nПовторите ввод '
                'времени')
            return TIME
    except ValueError:
        update.message.reply_text('Некорректный формат времени!!!\nВведите время в формате чч.мм')
        return TIME


def cancel(update, context):
    update.message.reply_text('Вы отменили добавление задачи')
    return ConversationHandler.END


def get_all(update, context):
    tasks = get_all_firebase(update.message.from_user.id, db)
    if tasks:
        update.message.reply_text('Список задач:')
        for task in tasks:
            update.message.reply_text(task.to_str())
    else:
        update.message.reply_text('У вас нет задач')


def update_task(update, context):
    update.message.reply_text(
        'Введите название задачи, которую хотите изменить\nиспользуйте /cancel чтобы отменить изменение')
    return UPDATE_GET


def update_get(update, context):
    name = update.message.text
    task_copy = get_firebase(update.message.from_user.id, name, db)
    if task_copy:
        task.copy(task_copy)
        update.message.reply_text(task.to_str())
        update.message.reply_text('Введите новое описание задачи\nВведите /skip чтобы не изменять описание')
        return UPDATE_DESCRIPTION
    else:
        update.message.reply_text('Нет такой задачи. Попробуйте ввести название снова')
        return UPDATE_GET


def update_description(update, context):
    task.description = update.message.text
    update.message.reply_text(
        'Введите новую дату, до которой задача должна быть выполнена\nВведите /skip чтобы не изменять дату')
    return UPDATE_DATE


def skip_description(update, context):
    update.message.reply_text(
        'Введите новую дату, до которой задача должна быть выполнена\nВведите /skip чтобы не изменять дату')
    return UPDATE_DATE


def update_date(update, context):
    date = update.message.text
    try:
        valid_date = datetime.strptime(date, '%d.%m.%Y')
        if valid_date.date() >= datetime.today().date():
            task.date = valid_date
            update.message.reply_text(
                'Введите время, до которого задача должна быть выполнена в формате чч.мм\nВведите /skip чтобы не '
                'изменять время')
            return UPDATE_TIME
        else:
            update.message.reply_text('Этот день уже прошел!!!\nВведите дату не раньше чем сегодня')
            return UPDATE_DATE
    except ValueError:
        update.message.reply_text('Некорректный формат даты!!!\nВведите дату в формате дд.мм.гггг')
        return UPDATE_DATE


def skip_date(update, context):
    update.message.reply_text(
        'Введите время, до которого задача должна быть выполнена в формате чч.мм\nВведите /skip чтобы не изменять время')
    return UPDATE_TIME


def update_time(update, context):
    time = update.message.text
    try:
        date_str = task.date.strftime('%d.%m.%Y') + '/' + time
        valid_time = datetime.strptime(date_str, '%d.%m.%Y/%H.%M')
        if valid_time >= datetime.today():
            tzut = tzutc()
            task.date = valid_time.replace(tzinfo=tzut)
            task.is_send_message = False
            update_firebase(update.message.from_user.id, task, db)
            update.message.reply_text('Задача успешно изменена')
            return ConversationHandler.END
        else:
            update.message.reply_text(
                'Время, до которого задача должна быть выполнена, должно быть не меньше чем текущее!\nПовторите ввод '
                'времени')
            return UPDATE_TIME
    except ValueError:
        update.message.reply_text('Некорректный формат времени!!!\nВведите время в формате чч.мм')
        return UPDATE_TIME


def skip_time(update, context):
    task.is_send_message = False
    update_firebase(update.message.from_user.id, task, db)
    update.message.reply_text('Задача успешно изменена')
    return ConversationHandler.END


def cancel_update(update, context):
    update.message.reply_text('Вы отменили редактирование задачи')
    return ConversationHandler.END


def del_task(update, context):
    update.message.reply_text(
        'Введите название задачи, которую хотите удалить\nВведите /cancel чтобы не удалять задачу')
    return DELETE_GET


def delete_get(update, context):
    name = update.message.text
    task = get_firebase(update.message.from_user.id, name, db)
    if task:
        delete_firebase(update.message.from_user.id, name, db)
        update.message.reply_text('задача удалена')
        return ConversationHandler.END
    else:
        update.message.reply_text('Нет такой задачи. Попробуйте ввести название снова')
        return DELETE_GET


def cancel_delete(update, context):
    update.message.reply_text('Вы отменили удаление задачи')
    return ConversationHandler.END


def done_task(update, context):
    update.message.reply_text('Какую задачу пометить как выполненную?\nВведите /cancel чтобы не помечать задачу')
    return DONE_GET


def done_get(update, context):
    name = update.message.text
    task = get_firebase(update.message.from_user.id, name, db)
    if task:
        done_firebase(update.message.from_user.id, name, db)
        update.message.reply_text('Задача помечена как выполненная')
        return ConversationHandler.END
    else:
        update.message.reply_text('Нет такой задачи. Попробуйте ввести название снова')
        return DONE_GET


def cancel_done(update, context):
    update.message.reply_text('Вы отменили выполнение задачи')
    return ConversationHandler.END


def check_db(context):
    users = get_users(db)
    for doc in users:
        user = doc.to_dict()
        tasks = get_all_firebase(user['id'], db)
        for task_doc in tasks:
            task = Task.from_dict(task_doc.to_dict())
            date = datetime.now()
            date = date.replace(tzinfo=tzutc())
            if task.date <= date and not task.is_done and not task.is_send_message:
                context.bot.send_message(chat_id=user['id'], text='Вы не выполнили задачу!\n' + task.to_str())
                task.is_send_message = True
                add_task_firebase(task, db)


def main():
    updater = Updater(token='1361442277:AAGvchKc35aElkOd9NPFIBJGCO3s8XzpjQI', use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)

    help_handler = CommandHandler('help', help)

    get_all_handler = CommandHandler('getAll', get_all)

    add_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('addTask', add_task)],
        states={
            NAME: [MessageHandler(Filters.text & (~Filters.command), name)],

            DESCRIPTION: [MessageHandler(Filters.text & (~Filters.command), description)],

            DATE: [MessageHandler(Filters.text & (~Filters.command), date)],

            TIME: [MessageHandler(Filters.text & (~Filters.command), time)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    update_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('editTask', update_task)],
        states={
            UPDATE_GET: [MessageHandler(Filters.text & (~Filters.command), update_get)],

            UPDATE_DESCRIPTION: [MessageHandler(Filters.text & (~Filters.command), update_description),
                                 CommandHandler('skip', skip_description)],

            UPDATE_DATE: [MessageHandler(Filters.text & (~Filters.command), update_date),
                          CommandHandler('skip', skip_date)],

            UPDATE_TIME: [MessageHandler(Filters.text & (~Filters.command), update_time),
                          CommandHandler('skip', skip_time)]
        },

        fallbacks=[CommandHandler('cancel', cancel_update)]
    )

    delete_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('delTask', del_task)],
        states={
            DELETE_GET: [MessageHandler(Filters.text & (~Filters.command), delete_get)]
        },
        fallbacks=[CommandHandler('cancel', cancel_delete)]
    )

    done_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('doneTask', done_task)],
        states={
            DONE_GET: [MessageHandler(Filters.text & (~Filters.command), done_get)]
        },
        fallbacks=[CommandHandler('cancel', cancel_done)]
    )

    unknown_command_handler = MessageHandler(Filters.command, unknown)

    dispatcher.add_handler(get_all_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(add_conv_handler)
    dispatcher.add_handler(update_conv_handler)
    dispatcher.add_handler(delete_conv_handler)
    dispatcher.add_handler(done_conv_handler)
    dispatcher.add_handler(unknown_command_handler)

    j = updater.job_queue
    checking_job = j.run_repeating(check_db, interval=600, first=0)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
