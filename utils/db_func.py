from DB.tables import User


def get_pri_errors(session, pri):
    if pri.lower() == 'info':
        objs = session.query(User).filter_by(info=True).all()
    if pri.lower() == 'warning':
        objs = session.query(User).filter_by(warning=True).all()
    if pri.lower() == 'error':
        objs = session.query(User).filter_by(error=True).all()
    if pri.lower() == 'critical':
        objs = session.query(User).filter_by(critical=True).all()
    return objs


def get_chat_ids(usr_list):
    return [user.bale_id for user in usr_list]