import interface.print as iface_print
import interface.common as iface_common
import interface.user as iface_user
import auth
import auth.user as auth_user

def welcome() -> None:
    if auth.is_authed(): dashboard()
    iface_print.header()
    iface_print.info('Halo, silahkan pilih menu di bawah ini:')
    iface_print.general('[1] Login')
    iface_print.general('[2] Daftar')
    iface_print.general('[3] Keluar dari program')

    iface_print.separator()
    option = int(iface_common.input_general('Pilihan kamu'))
    while option not in [1, 2, 3]:
        iface_print.separator()
        iface_print.warning('Pilihan kamu tidak valid, silahkan coba lagi ya!')
        option = int(iface_common.input_general('Pilihan kamu'))

    match option:
        case 1:
            login()
        case 2:
            register()
        case 3:
            iface_print.header()
            iface_print.info('Program berhasil diakhiri, sampai jumpa lagi.')
            exit()

def login() -> None:
    if auth.is_authed(): dashboard()
    iface_print.header()
    iface_print.info('Silahkan login terlebih dahulu.')

    username = iface_common.input_general('Username')
    while not username.isalnum():
        iface_print.warning('Username hanya boleh pake a-z dan 0-9. Contoh: notonegoro12')
        username = iface_common.input_general('Username')

    while len(username) < 5:
        iface_print.warning('Username tidak boleh kurang dari 5 karakter.')
        username = iface_common.input_general('Username')

    password = iface_common.input_general('Password')
    while len(password) < 8:
        iface_print.warning('Password tidak boleh kurang dari 8 karakter.')
        password = iface_common.input_general('Password')

    if auth.authenticate(username, password):
        dashboard(is_from_login=True)
    else:
        iface_print.separator()
        iface_print.failed(f'Username atau password yang kamu masukkan salah nih.')

def register() -> None:
    if auth.is_authed(): dashboard()
    iface_print.header()
    iface_print.info('Halo, silahkan lengkapi data-datamu dulu ya!')

    name = iface_common.input_general('Nama panggilan kamu')
    while len(name) < 1 or len(name) > 20:
        iface_print.warning('Nama panggilan tidak boleh kosong atau lebih dari 20 karakter ya.')
        name = iface_common.input_general('Nama panggilan kamu')

    username = iface_common.input_general(f'Halo {name.split(' ')[0]}! sekarang pilih username kamu, harus unik ya!')
    while not username.isalnum():
        iface_print.warning('Username hanya boleh pake a-z dan 0-9. Contoh: notonegoro12')
        username = iface_common.input_general('Pilih username kamu, harus unik ya!')

    while len(username.lower()) < 5:
        iface_print.warning('Username tidak boleh kurang dari 5 karakter.')
        username = iface_common.input_general('Pilih username kamu, harus unik ya!')

    while auth.is_username_exist(username.lower()):
        iface_print.warning('Yahh, usernamenya udah dipake, coba yang lain deh!')
        username = iface_common.input_general('Pilih username kamu, harus unik ya!')

    password = iface_common.input_general('Buat password yang aman')
    while len(password) < 8:
        iface_print.warning('Biar aman, password tidak boleh kurang dari 8 karakter.')
        password = iface_common.input_general('Password')

    auth.user.register(name, username.lower(), password)

    iface_print.header()
    iface_print.success(
        f'Selamat datang {name.split(" ")[0]}, kamu telah terdaftar dengan username \033[4m\033[34m{username.lower()}\033[0m silahkan login dahulu ya!')

    iface_common.input_general('Tekan enter untuk login.')
    login()

def dashboard(is_from_login: bool = False) -> None:
    if not auth.is_authed(): welcome()

    iface_print.header()
    iface_user.profile()

    if is_from_login:
        iface_print.success(f'Selamat datang kembali {auth_user.user['name'].split(' ')[0]}, senang sekali bertemu lagi denganmu.')
        iface_print.separator()

    iface_print.info('Silahkan pilih menu dibawah ini:')
    iface_print.general('[1] Hitung emisi karbon')
    iface_print.general('[2] Bandingkan total emisi karbonmu')
    iface_print.general('[3] Lihat statistik kamu')
    iface_print.general('[4] Logout')
    iface_print.separator()

    option = int(iface_common.input_general('Masukkan pilihanmu'))
    while option not in [1, 2, 3, 4]:
        iface_print.warning('Pilihan kamu tidak valid, silahkan coba lagi ya!')
        option = int(iface_common.input_general('Masukkan pilihanmu'))

    iface_print.separator()
    match option:
        case 1:
            iface_user.calculate()
        case 2:
            iface_user.compare()
        case 3:
            iface_user.statistics()
        case 4:
            iface_print.warning('Kamu akan logout!')
            if iface_common.input_general('Kamu perlu login lagi untuk mengakses, kamu yakin ingin logout? [y/N]') in ['Y', 'y']:
                iface_print.header()
                iface_print.success(f'Kamu berhasil logout, sampai berjumpa lain waktu {auth_user.user['name'].split(' ')[0]}!')
                auth_user.logout()
                iface_print.separator()
                iface_common.input_general('Tekan enter untuk melanjutkan.')
                welcome()
            else:
                dashboard()