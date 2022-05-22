class BotMSG:
    start_msg = 'لطفا در صورتی که تمایل به ثبت نام دارید،\n ' \
                'قبل از ثبت نام از ثبت شدن *کد آیدی* خود از طریق مدیر اطمینان حاصل کنید.\n ' \
                'در صورتی که اطمینان دارید گزینه *تایید* و در غیر این صورت از گزینه *انصراف* استفاده نمایید.'

    get_id = "It's done. you will be notified if the admin accepts your request."


class ErrLogs:
    record_exist = 'duplicated bale id'


priority_map = dict(
    INFO='INFO, WARNING, ERROR, CRITICAL',
    WARNING='WARNING, ERROR, CRITICAL',
    ERROR='ERROR, CRITICAL',
    CRITICAL='CRITICAL'
)