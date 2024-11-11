import auth
import auth.user as auth_user
import interface.print as iface_print
import interface.common as iface_common
import database as db
import interface.auth as iface_auth
import time
import random

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
        while option not in range(len(vehicles) + 1) or option < 1:
            iface_print.warning('Pilihan kamu tidak valid, silahkan coba lagi ya!')
            option = int(iface_common.input_general('Masukkan pilihan kamu'))
        selected_vehicle = vehicles[option - 1]

        iface_print.separator()
        iface_print.success(f'Kamu memilih kendaraan {selected_vehicle['name']}.')
        iface_print.info('Masukkan jarak dalam meter, gunakan titik untuk pecahan, contoh: 1500.50 untuk 1.5 km.')
        iface_print.separator()
        distance = float(iface_common.input_general(f'Seberapa jauh kamu mengendarainya? (meter)'))
        while distance < 1:
            iface_print.warning('Jarak tidak boleh kurang dari atau sama dengan 0 (nol) meter.')
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
            f'Maka kamu telah menghasilkan emisi karbon sebanyak {selected_vehicle['emissions_gr_km']:.2f} gram x {distance_km} km = \033[34m{emissions:.2f} gram ≈ {emissions_kg} kg.\033[0m')
        iface_print.info(
            f'Total emisi karbon kamu sekarang adalah sebanyak \033[34m{(auth_user.user['total_carbon_gr'] / 1000):.2f} kg (+{emissions_kg} kg) \033[0m')

        iface_print.separator()
        if iface_common.input_general('Mau menghitung lagi [y/N]') not in ['y', 'Y']: break

    iface_auth.welcome()

def compare() -> None:
    quotes = [
        (
            'Climate change is a terrible problem, and it absolutely needs to be solved. It deserves to be a huge priority.', 'Bill Gates, Founder of Microsoft'
        ),
        (
            'Climate change is a huge challenge, but it can be brought in line if governments, businesses and individuals work together.',
            'Sir Richard Branson, Founder of Virgin Group'
        ),
        (
            'We are running the most dangerous experiment in history right now, which is to see how much carbon dioxide \n the atmosphere can handle before there is an environmental catastrophe.',
            'Elon Musk, CEO of Tesla & SpaceX'
        ),
        (
            'Adults keep saying we owe it to the young people, to give them hope, but I don’t want your hope. \nI don’t want you to be hopeful. I want you to panic. I want you to feel the fear I feel every day. I want you to act. \nI want you to act as you would in a crisis. I want you to act as if the house is on fire, because it is.',
            'Greta Thunberg, 17 year-old Swedish Activist'
        ),
        (
            'The time for seeking global solutions is running out. We can find suitable solutions only if we act together and in agreement.',
            'Pope Francis, 266th Catholic Pope'
        ),
    ]

    while True:
        iface_print.header()
        profile()
        iface_print.info('Bandingkan emisi karbon kamu dengan daya serap suatu jenis pohon!')

        iface_print.separator()
        iface_print.info('Pertama pilih jenis pohon di bawah ini.')
        trees = db.get_trees()
        for num, t in enumerate(trees, start=1):
            iface_print.general(f'[{num}] {t['name']} (\033[3m{t['scientific_name']}\033[0m) --- {t['carbon_absorption_gr_hr']:.2f} gram/jam')

        iface_print.separator()
        option = int(iface_common.input_general('Masukkan pilihan kamu'))
        while option not in range(len(trees) + 1) or option < 1:
            iface_print.warning('Pilihan kamu tidak valid, silahkan coba lagi ya!')
            option = int(iface_common.input_general('Masukkan pilihan kamu'))
        selected_tree = trees[option - 1]

        iface_print.header()
        profile()
        iface_print.success(f'Kamu memilih pohon {selected_tree['name']} \033[3m({selected_tree['scientific_name']})\033[0m yang memiliki potensi daya serap karbon sebanyak {selected_tree['carbon_absorption_gr_hr']:.2f} gram/jam.')

        amount_of_trees_needed = round(auth_user.user['total_carbon_gr'] / (selected_tree['carbon_absorption_gr_hr'] * 24), 2)

        time.sleep(2)
        iface_print.separator()
        iface_print.info(f'Total emisi karbon kamu adalah sebanyak \033[34m{auth_user.user['total_carbon_gr']:.2f} gram ≈ {auth_user.user['total_carbon_gr']/1000:.2f} kg\033[0m.')

        time.sleep(2)
        iface_print.info(f'Maka diperlukan sebanyak \033[34m{amount_of_trees_needed}\033[0m batang pohon {selected_tree['name']} \033[3m({selected_tree['scientific_name']})\033[0m untuk menyerap total emisi karbonmu dalam 24 jam.')

        time.sleep(2)
        iface_print.separator()
        iface_print.info('\033[104mYuk kurangi emisi karbon!\033[0m \033[3m\033[34m-1 gram\033[0m\033[3m karbon dikali 8 miliar orang itu impactful!\033[0m')

        time.sleep(2)
        iface_print.separator()
        iface_print.general('A wise person once said:')

        selected_quotes = random.choice(quotes)
        time.sleep(2)
        print()
        iface_print.animated_print(f'\033[3m"{selected_quotes[0]}"\033[0m\n\033[34m---{selected_quotes[1]}\033[0m', .05)
        print()

        iface_print.separator()
        if iface_common.input_general('Mau membandingkan lagi [y/N]') not in ['y', 'Y']: break

    iface_auth.welcome()

def statistics() -> None:
    iface_print.header()
    profile()
    iface_print.info('Statistik kamu')

    number_round_the_world = round((auth_user.user['total_distance_m'] / 1000) / 40007.863, 10)
    times_james_webb_weight = round((auth_user.user['total_carbon_gr'] / 1000) / 6161, 10)

    time.sleep(1)
    iface_print.separator()
    iface_print.general(f'Nama kamu \033[34m{auth_user.user['name']}\033[0m.')

    time.sleep(1.25)
    iface_print.general(f'Total jarak yang kamu tempuh adalah sejauh \033[34m{auth_user.user['total_distance_m']} meter ≈ {auth_user.user['total_distance_m']/1000:.2f} km\033[0m.')

    time.sleep(2)
    iface_print.general(f'Jarak tersebut sama dengan \033[34m{number_round_the_world}\033[0m kali mengelilingi bumi di sekitar ekuator.')

    time.sleep(2)
    iface_print.separator()
    iface_print.general(
        f'Total emisi karbon yang kamu ciptakan adalah sebanyak \033[34m{auth_user.user['total_carbon_gr']} gram ≈ {auth_user.user['total_carbon_gr'] / 1000:.2f} kg\033[0m.')

    time.sleep(2)
    iface_print.general(
        f'Berat tersebut sama dengan \033[34m{times_james_webb_weight}\033[0m kali berat Teleskop James Webb.')

    iface_print.separator()
    iface_common.input_general('Tekan enter untuk kembali ke menu utama')
    iface_auth.dashboard()
