import interface.print as iface_print
import interface.error as iface_error
import interface.auth as iface_auth
import database as db

try:
    iface_print.header()
    db.validate_tables()
    iface_auth.welcome()
except KeyboardInterrupt:
    print()
    iface_print.separator()
    iface_print.warning('Sepertinya kamu telah menekan kombinasi tombol CTRL+C.')
    iface_print.warning('Program telah dihentikan dengan aman.')
except Exception as e:
    iface_error.handle_exception(e)