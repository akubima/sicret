import auth
import auth.user as auth_user
import interface.print as iface_print
import interface.common as iface_common
import database as db
import interface.auth as iface_auth


def profile() -> None:
    iface_print.general(f'Nama: \033[34m{auth_user.user['name']}\033[0m')
    iface_print.general(f"Total emisi: \033[34m{round((auth_user.user['total_carbon_gr'] / 1000), 2)} kg\033[0m")
    iface_print.general(f"Total jarak: \033[34m{round((auth_user.user['total_distance_m'] / 1000), 2)} km\033[0m")
    iface_print.separator()

def calculate() -> None:
    while True:
        iface_print.header()
        profile()
        iface_print.info('Hitung emisi karbonmu!')

        iface_print.separator()
        iface_print.info('Pertama pilih kendaraan yang kamu gunakan dari daftar di bawah ini.')
        vehicles = db.get_vehicles()
        for num, v in enumerate(vehicles, start=1):
            iface_print.general(f'[{num}] {v['name']}')

        iface_print.separator()
        option = int(iface_common.input_general('Masukkan pilihan kamu'))
        while option not in range(len(vehicles) + 1):
            iface_print.warning('Pilihan kamu tidak valid, silahkan coba lagi ya!')
            option = int(iface_common.input_general('Masukkan pilihan kamu'))
        selected_vehicle = vehicles[option - 1]

        iface_print.separator()
        iface_print.success(f'Kamu memilih kendaraan {selected_vehicle['name']}.')
        iface_print.info('Masukkan jarak dalam meter, gunakan titik untuk pecahan, contoh: 1500.50 untuk 1.5 km.')
        iface_print.separator()
        distance = float(iface_common.input_general(f'Seberapa jauh kamu mengendarainya? (meter)'))
        distance_km = round(distance / 1000, 2)
        emissions = selected_vehicle['emissions_gr_km'] * distance_km
        emissions_kg = round(emissions / 1000, 2)

        db.increment_user_carbon(emissions)
        db.increment_user_distance(distance)
        auth.refresh_auth()

        iface_print.header()
        profile()
        iface_print.info(
            f'Kamu mengendarai {selected_vehicle['name']} yang menghasilkan emisi karbon sebanyak {selected_vehicle['emissions_gr_km']} gram untuk setiap 1 km tiap penumpang sejauh {distance_km} km.')
        iface_print.info(
            f'Maka kamu telah menghasilkan emisi karbon sebanyak {selected_vehicle['emissions_gr_km']:.2f} gram x{distance_km} km = \033[34m{emissions:.2f} gram = {emissions_kg} kg.\033[0m')

        iface_print.separator()
        if iface_common.input_general('Mau menghitung lagi [y/N]') not in ['y', 'Y']: break

    iface_auth.welcome()