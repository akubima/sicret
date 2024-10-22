import interface.print as iface_print
import interface.error as iface_error
import interface.auth as iface_auth
import database as db

try:
    iface_print.header()
    db.validate_table(must_all_checked=False)
    iface_auth.welcome()
except Exception as e:
    iface_error.handle_exception(e)