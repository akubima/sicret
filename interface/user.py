import auth.user as auth_user
import interface.print as iface_print
import interface.common as iface_common
import database as db

def profile() -> None:
    iface_print.general(f'Nama: \033[34m{auth_user.user['name']}\033[0m')
    iface_print.general(f"Total emisi: \033[34m{round((auth_user.user['total_carbon_gr'] / 1000), 2)} kg\033[0m")
    iface_print.separator()

def calculate() -> None:
    iface_print.header()
    profile()
    iface_print.info('Hitung emisi karbonmu!')
    iface_print.separator()
    iface_print.info('Pertama pilih kendaraan yang kamu gunakan dari daftar di bawah ini.')
    iface_print.separator()
    option = int(iface_common.input_general('Masukkan pilihan kamu'))
    print(db.get_vehicles())
    # Whil is not valid option loop till correct