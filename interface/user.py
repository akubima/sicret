import auth.user as auth_user
import interface.print as iface_print

def profile() -> None:
    iface_print.general(f'Nama: \033[34m{auth_user.user['name']}\033[0m')
    iface_print.general(f"Total emisi: \033[34m{round((auth_user.user['total_carbon_gr'] / 1000), 2)} kg\033[0m")
    iface_print.separator()