from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import sqlite3 as sq
import datetime



class ScrollFrame(tk.Frame):
    def __init__(self, parent, width=100, height=100):
        super().__init__(parent)  # create a frame (self)

        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff", width=width - 20,
                                height=height)  # place canvas on self
        self.viewPort = tk.Frame(self.canvas,
                                 background="#ffffff")  # place a frame on the canvas, this frame will hold the child widgets
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)  # place a scrollbar on self
        self.canvas.configure(yscrollcommand=self.vsb.set)  # attach scrollbar action to scroll of canvas

        self.vsb.pack(side="right", fill="y")  # pack scrollbar to right of self
        self.canvas.pack(side="left", fill="both", expand=True)  # pack canvas to left of self and expand to fil
        self.canvas_window = self.canvas.create_window((4, 4), window=self.viewPort, anchor="nw",
                                                       # add view port frame to canvas
                                                       tags="self.viewPort")

        self.viewPort.bind("<Configure>",
                           self.onFrameConfigure)  # bind an event whenever the size of the viewPort frame changes.
        self.canvas.bind("<Configure>",
                         self.onCanvasConfigure)  # bind an event whenever the size of the viewPort frame changes.

        self.onFrameConfigure(
            None)  # perform an initial stretch on render, otherwise the scroll region has a tiny border until the first resize

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox(
            "all"))  # whenever the size of the frame changes, alter the scroll region respectively.

    def onCanvasConfigure(self, event):
        '''Reset the canvas window to encompass inner frame when required'''
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window,
                               width=canvas_width)  # whenever the size of the canvas changes alter the window region respectively.


WINDOWS = []
TIME = 10
ATTEMPS = 0
hotel_list = []
HOTELS_BUTTONS = []
HOTELS_FILTER = ''
ADMINS_LIST = []
ADMINS_FILTER = ''
ADMINS_BUTTONS = []
ADMINS_BUTTONS_CB = []
ROOMS_BUTTONS = []
HOSTERS_BUTTONS = []
HOSTERS_BUTTONS_CB = []

def tc():
    global TIME
    TIME -= 1
    print(TIME, file=open("timertime", 'w'))
    return TIME


def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Ошибка")
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Ок", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def systemlock():
    def lc():
        global TIME
        global ATTEMPS
        if TIME > 0:
            locktimelabel.config(text=str(TIME))
            tc()
            locktimelabel.after(1000, lc)
        else:
            windestroy()
            ATTEMPS = 3
            TIME = 60
            print(ATTEMPS, file=open("attemps", 'w'))
            print(TIME, file=open("timertime", 'w'))
            login()

    global TIME

    windestroy()
    lockScreen = Tk()
    lockScreen.title("Система заблокирована")
    WINDOWS.append(lockScreen)
    lockScreen.geometry("300x150")
    Label(lockScreen, text="Система заблокирована!").place(x=80, y=50)
    TIME = int(open("timertime", 'r').read())

    locktimelabel = Label(lockScreen, text=str(TIME), fg="red")
    locktimelabel.place(x=135, y=80)

    lc()

    lockScreen.mainloop()


def windestroy():
    for win in WINDOWS:
        try:
            win.destroy()
            WINDOWS.remove(win)
        except:
            continue


def login():
    def logincheck():
        global ATTEMPS
        try:
            Label(text="                                                                      ", fg="red").place(x=70,
                                                                                                                 y=20)
            print(ATTEMPS)
            lgn = login_form.get()
            pswd = password_form.get()
            ##############################################
            #lgn1, pswd1 = '', ''
            ##############################################
            # print(lgn,pswd)
            conn = sq.connect('data.db')
            cursor = conn.cursor()
            resp = "SELECT * FROM accounts WHERE login LIKE '" + lgn + "' AND password LIKE '" + pswd + "' ;"
            # print(resp)
            cursor.execute(resp)
            results = cursor.fetchall()
            conn.close()
            print(results)
            if len(results) == 0:
                ATTEMPS -= 1
                now = datetime.datetime.now()
                print("Неудачная поптыка входа:" + str(now), file=open("Попытки входа.txt", 'a'))
                Label(text="Неверный логин или пароль", fg="red").place(x=70, y=20)
                print(ATTEMPS, file=open("attemps", "w"))
                ATTEMPS = int(open("attemps", 'r').read())
                if ATTEMPS <= 0:
                    systemlock()
            elif results[0][5] == 1:
                banWindow = Tk()
                WINDOWS.append(banWindow)
                banWindow.geometry("300x150")
                w = banWindow.winfo_screenwidth()  # ширина экрана
                h = banWindow.winfo_screenheight()  # высота экрана
                w = w // 2  # середина экрана
                h = h // 2
                w = w - 300  # смещение от середины
                h = h - 150
                banWindow.geometry('400x400+{}+{}'.format(w, h))
                banWindow.title("Ошибка")
                banWindow.maxsize(300, 150)
                banWindow.minsize(300, 150)
                Label(banWindow, text="Ваш аккаунт заблокирован!\nПричина: " + str(results[0][6]),
                      fg="red", width=40, height=10).place(x=0, y=0)
                Button(banWindow, text="Выход", command=lambda: banWindow.destroy()).place(x=125, y=100)
            else:
                try:
                    banWindow.destroy()
                except:
                    print()
                windestroy()
                program(results[0])

        except:
            pass

    login_, password = '', ''
    loginScreen = Tk()
    WINDOWS.append(loginScreen)
    loginScreen.geometry("300x150")
    w = loginScreen.winfo_screenwidth()  # ширина экрана
    h = loginScreen.winfo_screenheight()  # высота экрана
    w = w // 2  # середина экрана
    h = h // 2
    w = w - 300 # смещение от середины
    h = h - 150
    loginScreen.geometry('400x400+{}+{}'.format(w, h))
    loginScreen.minsize(300, 150)
    loginScreen.maxsize(300, 150)
    loginScreen.title("Вход")
    login_form = Entry(loginScreen, textvariable=login_, width=20)
    password_form = Entry(loginScreen, textvariable=password, width=20, show="*")
    Label(loginScreen, text="Логин").place(x=65, y=40)
    Label(loginScreen, text="Пароль").place(x=58, y=60)
    login_form.place(x=65 + 45, y=40)
    password_form.place(x=65 + 45, y=60)
    enter_button = Button(loginScreen, text="Войти", command=logincheck)
    exit_button = Button(loginScreen, text="Отмена", command=windestroy)
    enter_button.place(x=120, y=100)
    exit_button.place(x=170, y=100)
    loginScreen.mainloop()


def program_manager(result):
    global hotel_list

    def add_hotel():
        global hotel_list

        def create():

            global hotel_list
            floors, rooms, country, city, street, house = '', '', '', '', '', ''

            floors = floors_form.get()
            rooms = rooms_form.get()
            country = country_form.get()
            city = city_form.get()
            street = street_form.get()
            house = house_form.get()
            if floors == '' or rooms == '' or country == '' or city == '' or street == '' or house == '':
                popupmsg("Все поля должны быть заполнены")
                pass
            conn = sq.connect('data.db')
            cursor = conn.cursor()
            cmd = "SELECT MAX(id) from hotels"
            cursor.execute(cmd)
            res = cursor.fetchall()
            print(res)
            if res[0][0] != None:
                id_ = res[0][0] + 1
            else:
                id_ = 1
            print(id_)
            conn.close()

            # address = country + ', ' + city + ', ул. ' + street + ', д. ' + house

            conn = sq.connect('data.db')
            cursor = conn.cursor()
            cmd = "INSERT INTO hotels VALUES (" + str(id_) + ',' + floors + ',' + rooms + ',"' + country + '","' \
                  + city + '","' + street + '","' + house + '")'
            print(cmd)
            cursor.execute(cmd)
            cmd = 'CREATE TABLE"' + str(id_) + '"("id"	INTEGER,"rooms"	\
            INTEGER,"area"	INTEGER, "isFree" INTEGER) '
            cursor.execute(cmd)
            conn.commit()
            conn.close()
            update_hotels_list()

        add_hotel_window = Tk()
        WINDOWS.append(add_hotel_window)
        add_hotel_window.title("Добавить гостиницу")
        add_hotel_window.geometry("300x200")
        w = add_hotel_window.winfo_pointerx()
        h = add_hotel_window.winfo_pointery()
        w = w - 200  # смещение от середины
        h = h - 200
        add_hotel_window.geometry('300x220+{}+{}'.format(w, h))
        add_hotel_window.maxsize(300, 200)
        add_hotel_window.minsize(300, 200)

        country_form = Entry(add_hotel_window, width=35)
        Label(add_hotel_window, text="Страна: ").grid(row=1, column=30)
        country_form.grid(row=1, column=50)

        city_form = Entry(add_hotel_window, width=35)
        Label(add_hotel_window, text="Город: ").grid(row=4, column=30)
        city_form.grid(row=4, column=50)

        street_form = Entry(add_hotel_window, width=35)
        Label(add_hotel_window, text="Улица: ").grid(row=7, column=30)
        street_form.grid(row=7, column=50)

        house_form = Entry(add_hotel_window, width=35)
        Label(add_hotel_window, text="Дом: ").grid(row=11, column=30)
        house_form.grid(row=11, column=50)

        floors_form = Entry(add_hotel_window, width=35)
        Label(add_hotel_window, text="Этажи: ").grid(row=14, column=30)
        floors_form.grid(row=14, column=50)

        rooms_form = Entry(add_hotel_window, width=35)
        Label(add_hotel_window, text="Комнаты: ").grid(row=17, column=30)
        rooms_form.grid(row=17, column=50)

        Button(add_hotel_window, text="Сохранить", command=create, width=30).grid(row=29, column=50)
        Button(add_hotel_window, text="Отмена", command=lambda: add_hotel_window.destroy(), width=30).grid(row=30, column=50)

        add_hotel_window.mainloop()

    def edit_hotel(hotel):
        def edit(id_):
            floors, rooms, country, city, street, house = '', '', '', '', '', ''

            floors = floors_form.get()
            rooms = rooms_form.get()
            country = country_form.get()
            city = city_form.get()
            street = street_form.get()
            house = house_form.get()
            if floors == '' or rooms == '' or country == '' or city == '' or street == '' or house == '':
                popupmsg("Все поля должны быть заполнены")
            # address = country + ', ' + city + ', ул. ' + street + ', д. ' + house

            conn = sq.connect('data.db')
            cursor = conn.cursor()
            cmd = "UPDATE hotels SET floors = '" + str(floors) + "' ,rooms = '" + str(rooms) + \
                  "' ,country = '" + str(country) + "' ,city = '" + str(city) + "' ,street = '" + str(street) + \
                  "' ,house = '" + str(house) + "' WHERE id = " + str(id_)
            print(cmd)
            cursor.execute(cmd)

            conn.commit()
            conn.close()
            update_hotels_list()

        def del_single_hotel(id_):
            res = delete_hotel(hotel[0])
            if not res:
                popupmsg("Невозможно удалить гостиницу т.к в ней присутствуют номера")
                pass
            else:
                add_hotel_window.destroy()

        print(hotel)
        add_hotel_window = Tk()
        WINDOWS.append(add_hotel_window)
        add_hotel_window.title("Редактирование гостиницы")
        add_hotel_window.geometry("300x220")
        w = add_hotel_window.winfo_pointerx()
        h = add_hotel_window.winfo_pointery()
        w = w - 200  # смещение от середины
        h = h - 200
        add_hotel_window.geometry('300x220+{}+{}'.format(w, h))
        add_hotel_window.maxsize(300, 220)
        add_hotel_window.minsize(300, 220)

        v1 = StringVar(add_hotel_window, value=str(hotel[3]))
        country_form = Entry(add_hotel_window, width=35, textvariable=v1)
        Label(add_hotel_window, text="Страна: ").grid(row=1, column=30)
        country_form.grid(row=1, column=50)

        v2 = StringVar(add_hotel_window, value=str(hotel[4]))
        city_form = Entry(add_hotel_window, width=35, textvariable=v2)
        Label(add_hotel_window, text="Город: ").grid(row=4, column=30)
        city_form.grid(row=4, column=50)

        v3 = StringVar(add_hotel_window, value=str(hotel[5]))
        street_form = Entry(add_hotel_window, width=35, textvariable=v3)
        Label(add_hotel_window, text="Улица: ").grid(row=7, column=30)
        street_form.grid(row=7, column=50)

        v4 = StringVar(add_hotel_window, value=str(hotel[6]))
        house_form = Entry(add_hotel_window, width=35, textvariable=v4)
        Label(add_hotel_window, text="Дом: ").grid(row=11, column=30)
        house_form.grid(row=11, column=50)

        v5 = StringVar(add_hotel_window, value=str(hotel[1]))
        floors_form = Entry(add_hotel_window, width=35, textvariable=v5)
        Label(add_hotel_window, text="Этажи: ").grid(row=14, column=30)
        floors_form.grid(row=14, column=50)

        v6 = StringVar(add_hotel_window, value=str(hotel[2]))
        rooms_form = Entry(add_hotel_window, width=35, textvariable=v6)
        Label(add_hotel_window, text="Комнаты: ").grid(row=17, column=30)
        rooms_form.grid(row=17, column=50)

        Button(add_hotel_window, text="Сохранить", command=lambda x=hotel[0]: edit(x), width=30).grid(row=29, column=50)
        Button(add_hotel_window, text="Удалить", command=lambda x=hotel[0]: del_single_hotel(x), width=30).grid(row=30, column=50)
        Button(add_hotel_window, text="Отмена", command=lambda: add_hotel_window.destroy(), width=30).grid(row=31, column=50)

        add_hotel_window.mainloop()

    def update_hotels_list():
        global HOTELS_FILTER
        print(HOTELS_FILTER)

        conn = sq.connect('data.db')
        cursor = conn.cursor()
        cmd = "SELECT * from hotels"
        cursor.execute(cmd)
        hotels_list = cursor.fetchall()
        conn.close()

        for h in HOTELS_BUTTONS:
            try:
                h.destroy()
            except:
                continue

        for i in range(len(hotels_list)):
            address = str(hotels_list[i][3]) + ", " + str(hotels_list[i][4]) + ", Ул. " + str(hotels_list[i][5]) + \
                      ", д. " + str(hotels_list[i][6])
            txt = 'Гостиница номер ' + str(hotels_list[i][0]) + "\nЭтажей: " + str(hotels_list[i][1]) + \
                  "\nКомнат: " + str(hotels_list[i][2]) + "\nАдрес: " + address
            if HOTELS_FILTER.lower() in address.lower():
                b = Button(hotels_sfr.viewPort, text=txt, width=60, command=lambda x=hotels_list[i]: edit_hotel(x))
                HOTELS_BUTTONS.append(b)
                b.grid(column=1, row=i)
        return hotels_list

    def delete_hotel(id_):

        conn = sq.connect('data.db')
        cursor = conn.cursor()
        cmd = "SELECT * FROM '" + str(id_) + "'"
        cursor.execute(cmd)
        res = cursor.fetchall()
        if len(res) == 0:

            cmd = "DROP TABLE '" + str(id_) + "'"
            cursor.execute(cmd)
            cmd = "DELETE FROM hotels WHERE id = '" + str(id_) + "'"
            cursor.execute(cmd)
            conn.commit()
            conn.close()
            update_hotels_list()
            return True
        else:
            return False

    def uf(v):
        global HOTELS_FILTER
        HOTELS_FILTER = v
        update_hotels_list()

    def add_admin():
        def create():

            global ADMINS_LIST


            lgn = login_form.get()
            pswd = password_form.get()
            lastname = lastname_form.get()
            name = name_form.get()
            middlename = middlename_form.get()
            phone = phone_form.get()
            id_ = 0
            try:
                htl = int(hotel_menu.get().split()[2])
            except IndexError:
                popupmsg("Все поля должны быть заполнены")
                pass
            if lgn == '' or pswd == '' or lastname == '' or middlename == '' or phone == '' or htl == '' or name == '':
                popupmsg("Все поля должны быть заполнены")
                pass

            conn = sq.connect('data.db')
            cursor = conn.cursor()
            cmd = "SELECT MAX(id) from accounts"
            cursor.execute(cmd)
            res = cursor.fetchall()
            print(res)
            if res[0][0] != None:
                id_ = res[0][0] + 1
            else:
                id_ = 1
            print(id_)

            cmd = 'INSERT INTO accounts VALUES ({id}, "{login}", "{password}", "admin", \
             "{hotel}", 0, "", "{name}", "{middlename}", "{lastname}", \
              "{phonenumber}")'.format(
                id=id_,
                login=lgn,
                password=pswd,
                hotel=htl,
                name=name,
                middlename=middlename,
                lastname=lastname,
                phonenumber=phone
            )
            print(cmd)
            cursor.execute(cmd)
            conn.commit()
            update_admins_list()
            conn.close()

        add_admin_window = Tk()
        WINDOWS.append(add_admin_window)
        add_admin_window.title("Добавить администратора")
        add_admin_window.geometry("300x220")
        add_admin_window.maxsize(300, 220)
        add_admin_window.minsize(300, 220)
        w = add_admin_window.winfo_pointerx()
        h = add_admin_window.winfo_pointery()
        w = w - 200  # смещение от середины
        h = h - 200
        add_admin_window.geometry('300x250+{}+{}'.format(w, h))
        login_form = Entry(add_admin_window, width=35)
        Label(add_admin_window, text="Логин: ").grid(row=1, column=30)
        login_form.grid(row=1, column=50)

        password_form = Entry(add_admin_window, width=35)
        Label(add_admin_window, text="Пароль: ").grid(row=4, column=30)
        password_form.grid(row=4, column=50)

        lastname_form = Entry(add_admin_window, width=35)
        Label(add_admin_window, text="Фамилия: ").grid(row=7, column=30)
        lastname_form.grid(row=7, column=50)

        name_form = Entry(add_admin_window, width=35)
        Label(add_admin_window, text="Имя: ").grid(row=11, column=30)
        name_form.grid(row=11, column=50)

        middlename_form = Entry(add_admin_window, width=35)
        Label(add_admin_window, text="Отчество: ").grid(row=14, column=30)
        middlename_form.grid(row=14, column=50)

        phone_form = Entry(add_admin_window, width=35)
        Label(add_admin_window, text="Телефон: ").grid(row=17, column=30)
        phone_form.grid(row=17, column=50)

        conn = sq.connect('data.db')
        cursor = conn.cursor()
        cmd = "SELECT id FROM hotels"
        cursor.execute(cmd)
        tempd = cursor.fetchall()
        conn.close()
        print(tempd)
        lst = []
        for i in tempd:
            txt = "Гостиница номер " + str(i[0])
            lst.append(txt)
        Label(add_admin_window, text="Гостиница: ").grid(row=19, column=30)
        hotel_menu = ttk.Combobox(add_admin_window, stat="readonly",
                                  values=lst, width=32)

        hotel_menu.grid(row=19, column=50)
        Button(add_admin_window, text="Сохранить", command=create, width=30).grid(row=29, column=50)
        Button(add_admin_window, text="Отмена", command=lambda: add_admin_window.destroy(), width=30).grid(row=30, column=50)

        add_admin_window.mainloop()

    def delete_admin(id_):
            conn = sq.connect('data.db')
            cursor = conn.cursor()
            cmd = "DELETE FROM accounts WHERE id = " + str(id_)
            cursor.execute(cmd)
            conn.commit()
            conn.close()


    def ban(id_, reason='-'):
        print(reason)
        conn = sq.connect('data.db')
        cursor = conn.cursor()
        cmd = 'UPDATE accounts SET isBanned = 1, banReason = "{rsn}"  WHERE id = {id} '.format(rsn=reason, id=id_)
        cursor.execute(cmd)
        conn.commit()
        update_admins_list()
        conn.close()

    def unban(id_):

        conn = sq.connect('data.db')
        cursor = conn.cursor()
        cmd = "UPDATE accounts SET isBanned = 0, banReason = ''  WHERE id = " + str(id_)
        cursor.execute(cmd)
        conn.commit()
        update_admins_list()
        conn.close()

    def edit_admin(admin):
        global ADMINS_BUTTONS_CB

        def del_single_admin(id_):
            global ADMINS_BUTTONS_CB
            delete_admin(id_)



            update_admins_list()
            print(len(ADMINS_BUTTONS_CB))
            add_admin_window.destroy()


        def ban_single_admin(id_):
            def bn(id_, reason):
                ban(id_, reason=reason)
                banWindow.destroy()
                add_admin_window.destroy()

            banWindow = Tk()
            banWindow.resizable(False, False)
            w = add_admin_window.winfo_pointerx()
            h = add_admin_window.winfo_pointery()
            w = w - 300  # смещение от середины
            h = h - 100
            banWindow.geometry('300x80+{}+{}'.format(w, h))
            banWindow.title("Причина Блокировки")
            e = Entry(banWindow, width=49)

            Button(banWindow, text="Заблокировать", command=lambda x=id_: bn(x, e.get()), width=30).grid(row=2, column=0)
            Button(banWindow, text="Отмена", width=30).grid(row=3, column=0)
            e.grid(row=1, column=0)

        def create(id_):

            global ADMINS_LIST


            lgn = login_form.get()
            pswd = password_form.get()
            lastname = lastname_form.get()
            name = name_form.get()
            middlename = middlename_form.get()
            phone = phone_form.get()

            try:
                htl = int(hotel_menu.get().split()[2])
            except IndexError:
                popupmsg("Все поля должны быть заполнены")
                pass
            if lgn == '' or pswd == '' or lastname == '' or middlename == '' or phone == '' or htl == '' or name == '':
                popupmsg("Все поля должны быть заполнены")
                pass

            conn = sq.connect('data.db')
            cursor = conn.cursor()

            cmd = 'UPDATE accounts SET  login = "{login}", password = "{password}", role = "admin", \
             hotel = "{hotel}", name = "{name}", middlename = "{middlename}", lastname = "{lastname}", \
              phonenumber = "{phonenumber}" WHERE id = {id}'.format(
                id=id_,
                login=lgn,
                password=pswd,
                hotel=htl,
                name=name,
                middlename=middlename,
                lastname=lastname,
                phonenumber=phone
            )
            print(cmd)
            cursor.execute(cmd)
            conn.commit()
            update_admins_list()
            conn.close()

        def ubn(id_):
            unban(id_)
            add_admin_window.destroy()

        def export_single_admin(admin):

            from xlsxwriter.workbook import Workbook
            dirr = fd.asksaveasfilename(defaultextension='*.xlsx', filetypes=( ("Таблица Excel", "*.xlsx"), ))
            workbook = Workbook(str(dirr))
            worksheet = workbook.add_worksheet()
            worksheet.set_column('A:A', 20)
            worksheet.set_column('B:B', 20)
            worksheet.set_column('C:C', 20)
            worksheet.set_column('D:D', 20)
            worksheet.set_column('E:E', 20)
            worksheet.set_column('F:F', 20)
            worksheet.set_column('F:F', 20)

            data_format1 = workbook.add_format({'bg_color': 'red'})

            adm = [admin[9], admin[7], admin[8], admin[10], admin[4], admin[1], admin[2]]
            worksheet.write('A1', "Фамилия")
            worksheet.write('B1', "Имя")
            worksheet.write('C1', "Отчество")
            worksheet.write('D1', "Телефон")
            worksheet.write('E1', "Гостиница")
            worksheet.write('F1', "Логин")
            worksheet.write('G1', "Пароль")
            for j in range(len(adm)):
                worksheet.write(1, j, adm[j])
                if admin[6] == 1:
                    worksheet.set_row(1, cell_format=data_format1)
            workbook.close()
            pass

        add_admin_window = Tk()
        WINDOWS.append(add_admin_window)
        add_admin_window.title("Добавить администратора")
        add_admin_window.geometry("300x280")
        add_admin_window.maxsize(300, 280)
        add_admin_window.minsize(300, 280)

        w = add_admin_window.winfo_pointerx()
        h = add_admin_window.winfo_pointery()
        w = w - 200  # смещение от середины
        h = h - 200
        add_admin_window.geometry('300x250+{}+{}'.format(w, h))
        v1 = StringVar(add_admin_window, value=admin[1])
        login_form = Entry(add_admin_window, width=35, textvariable=v1)
        Label(add_admin_window, text="Логин: ").grid(row=1, column=30)
        login_form.grid(row=1, column=50)

        v2 = StringVar(add_admin_window, value=admin[2])
        password_form = Entry(add_admin_window, width=35, textvariable=v2)
        Label(add_admin_window, text="Пароль: ").grid(row=4, column=30)
        password_form.grid(row=4, column=50)

        v3 = StringVar(add_admin_window, value=admin[9])
        lastname_form = Entry(add_admin_window, width=35, textvariable=v3)
        Label(add_admin_window, text="Фамилия: ").grid(row=7, column=30)
        lastname_form.grid(row=7, column=50)

        v4 = StringVar(add_admin_window, value=admin[7])
        name_form = Entry(add_admin_window, width=35, textvariable=v4)
        Label(add_admin_window, text="Имя: ").grid(row=11, column=30)
        name_form.grid(row=11, column=50)

        v5 = StringVar(add_admin_window, value=admin[8])
        middlename_form = Entry(add_admin_window, width=35, textvariable=v5)
        Label(add_admin_window, text="Отчество: ").grid(row=14, column=30)
        middlename_form.grid(row=14, column=50)

        v6 = StringVar(add_admin_window, value=admin[10])
        phone_form = Entry(add_admin_window, width=35, textvariable=v6)
        Label(add_admin_window, text="Телефон: ").grid(row=17, column=30)
        phone_form.grid(row=17, column=50)

        conn = sq.connect('data.db')
        cursor = conn.cursor()
        update_hotels_list()
        cmd = "SELECT id FROM hotels"
        cursor.execute(cmd)
        tempd = cursor.fetchall()
        conn.close()
        #print(tempd)
        lst = []
        for i in tempd:
            txt = "Гостиница номер " + str(i[0])
            lst.append(txt)
        v8 = StringVar(add_admin_window, value="Гостиница номер "+str(admin[4]))
        Label(add_admin_window, text="Гостиница: ").grid(row=19, column=30)
        hotel_menu = ttk.Combobox(add_admin_window, state="readonly",
                                  values=lst, textvariable=v8, width=32)

        hotel_menu.grid(row=19, column=50)
        Button(add_admin_window, text="Сохранить", command=lambda x=admin[0]: create(x), width=30).grid(row=29, column=50)
        Button(add_admin_window, text="Экспорт в excel", command=lambda x=admin: export_single_admin(x), width=30).grid(row=30, column=50)
        if admin[5] == 0:
            Button(add_admin_window, text="Заблокировать", command=lambda x=admin[0]: ban_single_admin(x), width=30).grid(row=31, column=50)
        else:
            Button(add_admin_window, text="Разблокировать", command=lambda x=admin[0]: ubn(x), width=30).grid(row=31, column=50)
        Button(add_admin_window, text="Удалить", command=lambda x=admin[0]: del_single_admin(x), width=30).grid(row=32, column=50)
        Button(add_admin_window, text="Отмена", command=lambda: add_admin_window.destroy(), width=30).grid(row=33, column=50)

        add_admin_window.mainloop()


    def update_admins_list():
        global ADMINS_FILTER
        global ADMINS_BUTTONS_CB
        global ADMINS_BUTTONS
        print(ADMINS_FILTER)

        select_state.set(0)
        sds_all.config(text="Выбрать всех")

        conn = sq.connect('data.db')
        cursor = conn.cursor()
        cmd = "SELECT * from accounts WHERE role = 'admin' "
        cursor.execute(cmd)
        admins_list = cursor.fetchall()
        conn.close()

        for h in ADMINS_BUTTONS:

            h[0].destroy()


        for h in ADMINS_BUTTONS_CB:

            h[1].destroy()

        ADMINS_BUTTONS = []
        ADMINS_BUTTONS_CB = []


        #for i in ADMINS_BUTTONS_CB:
        #    print(i.get())

        for i in range(len(admins_list)):
            fioh = str(admins_list[i][4]) + " " + str(admins_list[i][7]) + " " + str(admins_list[i][8]) + \
                      " " + str(admins_list[i][9])
            fio = str(admins_list[i][9]) + " " + str(admins_list[i][7]) + \
                        " " + str(admins_list[i][8])
            f = False
            if admins_list[i][5] == 1:
                fg = "red"
                txt = fio + "\nЗаблокирован" + "\nПричина: " + admins_list[i][6]
            else:
                fg = "black"
                txt = fio + "\nРаботает в гостинце номер " + str(admins_list[i][4]) + \
                      "\nТелефон: " + str(admins_list[i][10])

            if ADMINS_FILTER.lower() in fioh.lower():
                b = Button(admins_sfr.viewPort, command=lambda x=admins_list[i]: edit_admin(x), text=txt, width=55, fg=fg)
                a = IntVar()

                cb = Checkbutton(admins_sfr.viewPort, variable=a, onvalue=admins_list[i][0], offvalue=0, width=3, height=3)

                ADMINS_BUTTONS.append([b,admins_list[i][0]])
                ADMINS_BUTTONS_CB.append([a, cb, admins_list[i][0]])
                b.grid(column=1, row=i)
                cb.grid(column=2, row=i)
            #a = Label(admins_sfr.viewPort)

        return admins_list

    def select_all():

        for i in ADMINS_BUTTONS_CB:
            i[1].select()

    def deselect_all():

        for i in ADMINS_BUTTONS_CB:
            i[1].deselect()
            #print(i[0].get(), end=' ')

    def sds():
        if select_state.get() == 0:
            sds_all.config(text="Убрать всех")
            select_all()
            select_state.set(1)

        elif select_state.get() == 1:
            sds_all.config(text="Выбрать всех")
            deselect_all()
            select_state.set(0)

    def export_many_admins():

        from xlsxwriter.workbook import Workbook
        dirr = fd.asksaveasfilename(defaultextension='*.xlsx', filetypes=(("Таблица Excel", "*.xlsx"),))
        workbook = Workbook(str(dirr))
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('C:C', 20)
        worksheet.set_column('D:D', 20)
        worksheet.set_column('E:E', 20)
        worksheet.set_column('F:F', 20)
        worksheet.set_column('F:F', 20)
        data_format1 = workbook.add_format({'bg_color': 'red'})
        worksheet.write('A1', "Фамилия")
        worksheet.write('B1', "Имя")
        worksheet.write('C1', "Отчество")
        worksheet.write('D1', "Телефон")
        worksheet.write('E1', "Гостиница")
        worksheet.write('F1', "Логин")
        worksheet.write('G1', "Пароль")

        a = [-1, 0]
        for i in ADMINS_BUTTONS_CB:
            if i[0].get() != 0:
                a.append(i[0].get())
        a = tuple(a)

        print(str(a))

        conn = sq.connect("data.db")
        cursor = conn.cursor()
        cmd = "SELECT name, lastname, middlename, phonenumber, hotel, login, password, isBanned from accounts WHERE id IN " + str(a)
        print(cmd)
        data = cursor.execute(cmd).fetchall()
        print(data)

        for i in range(len(data)):
            for j in range(len(data[i])-1):
                worksheet.write(i+1, j, data[i][j])
                if data[i][7] == 1:
                    worksheet.set_row(i+1, cell_format=data_format1)
        workbook.close()

        pass

    def import_from_excel():
        global ADMINS_BUTTONS_CB
        global ADMINS_BUTTONS
        import pandas as pd
        from xlsxwriter.workbook import Workbook
        dirr = fd.askopenfilename(filetypes=(("Таблица Excel", "*.xlsx"),))
        conn = sq.connect("data.db")
        cursor = conn.cursor()
        cmd = "DELETE from accounts WHERE role = 'admin'"
        cursor.execute(cmd)
        conn.commit()
        conn.close()
        update_admins_list()

        conn = sq.connect("data.db")
        cursor = conn.cursor()
        cmd = "SELECT MAX(id) FROM accounts"
        cursor.execute(cmd)

        res = cursor.fetchall()
        print(res)
        if res[0][0] != None:
            id_ = res[0][0] + 1
        else:
            id_ = 1
        conn.close()

        #print(dirr)
        df = pd.read_excel(dirr, sheet_name="Sheet1")

        c = df.values.tolist()
        for i in range(len(c)):

            cmd = "INSERT INTO accounts VALUES ({id}, '{login}', '{password}', 'admin', {hotel}, 0, '', '{name}', \
             '{middlename}', '{lastname}', '{phonenumber}' )".format(id=id_+i+1,
                                                                     lastname=c[i][0],
                                                                     name=c[i][1],
                                                                     middlename=c[i][2],
                                                                     phonenumber=c[i][3],
                                                                     hotel=c[i][4],
                                                                     login=c[i][5],
                                                                     password=c[i][6],
                                                                     )
            conn = sq.connect("data.db")
            cursor = conn.cursor()
            cursor.execute(cmd)
            conn.commit()
            conn.close()
            update_admins_list()



    msg = Tk()
    msg.geometry("300x150")
    msg.resizable(False, False)
    w = msg.winfo_screenwidth()  # ширина экрана
    h = msg.winfo_screenheight()  # высота экрана
    w = w // 2  # середина экрана
    h = h // 2
    w = w - 300  # смещение от середины
    h = h - 150
    msg.geometry('300x150+{}+{}'.format(w, h))
    msg.title("успешный вход")
    Label(msg, text="Вы успешно вошли в систему с ролью:\nУправляющий сетью гостиниц").place(x=45, y=50)
    Button(msg, text="Ок", command=lambda: msg.destroy()).place(x=145, y=90)
    msg.mainloop()

    mainWindow = Tk()
    WINDOWS.append(mainWindow)
    mainWindow.title("Управляющий сетью гостиниц")
    mainWindow.geometry("1000x500")
    mainWindow.resizable(False, False)
    w = mainWindow.winfo_screenwidth()  # ширина экрана
    h = mainWindow.winfo_screenheight()  # высота экрана
    w = w // 2  # середина экрана
    h = h // 2
    w = w - 1000//2  # смещение от середины
    h = h - 500//2
    mainWindow.geometry('1000x500+{}+{}'.format(w, h))
    hotels_fr = Frame(mainWindow, width=450, height=400, relief=RIDGE)
    hotels_sfr = ScrollFrame(hotels_fr, width=450, height=400)
    admins_fr = Frame(mainWindow, relief=RIDGE)
    admins_sfr = ScrollFrame(hotels_fr, width=450, height=400)
    hotels_list = update_hotels_list()

    hotels_fr.pack(side="top", fill="both", expand=True)
    admins_fr.pack(side="top", fill="both", expand=False)
    fv = StringVar()
    fv.trace("w", lambda name, index, mode: uf(filter_string.get()))
    filter_string = Entry(mainWindow, textvariable=fv, width=53)
    Label(mainWindow, text="Поиск по адресу: ").place(x=540, y=60)
    filter_string.place(x=650, y=60)
    hotels_sfr.place(x=540, y=80)
    admins_sfr.place(x=50, y=80)
    select_state = IntVar(value=0)
    add_hotel_button = Button(mainWindow, text="Добавить гостиницу", width=60, command=add_hotel)
    add_admin_button = Button(mainWindow, text="Добавить администратора", width=60, command=add_admin)
    sds_all = Button(mainWindow, text="Выбрать всех", width=11, command=sds)
    export_button = Button(mainWindow, text="Экспорт в Excel", width=12, command=export_many_admins)
    import_button = Button(mainWindow, text="Импорт из Excel", width=12, command=import_from_excel)
    export_button.place(x=300, y=50)
    add_admin_button.place(x=50, y=15)
    add_hotel_button.place(x=540, y=30)
    import_button.place(x=205, y=50)
    sds_all.place(x=395, y=50)
    update_admins_list()

    mainWindow.mainloop()


def program_admin(admin):

    msg = Tk()
    msg.geometry("300x150")
    msg.resizable(False, False)
    w = msg.winfo_screenwidth()  # ширина экрана
    h = msg.winfo_screenheight()  # высота экрана
    w = w // 2  # середина экрана
    h = h // 2
    w = w - 300  # смещение от середины
    h = h - 150

    conn = sq.connect("data.db")
    cursor = conn.cursor()
    cmd = "SELECT * FROM '" + str(admin[4]) + "'"
    print(cmd)
    try:
        cursor.execute(cmd)
    except:
        msg.geometry('320x150+{}+{}'.format(w, h))
        msg.title("Ошибка")
        Label(msg, text="Гостиница, связанная с вашим аккантом не существует\nОбратитесь к укравляющему").place(x=5, y=50)
        Button(msg, text="Ок", command=lambda: msg.destroy()).place(x=145, y=90)
        conn.close()
        msg.mainloop()
    else:
        msg.geometry('300x150+{}+{}'.format(w, h))
        msg.title("успешный вход")
        Label(msg, text="Вы успешно вошли в систему с ролью:\nАдминистратор гостиницы").place(x=45, y=50)
        Button(msg, text="Ок", command=lambda: msg.destroy()).place(x=145, y=90)
        conn.close()
        msg.mainloop()


        def add_room():

            def create():
                area = area_form.get()
                rooms = rooms_form.get()
                number = number_form.get()
                if area == '' or rooms == '' or number == '':
                    popupmsg("Все поля должны быть заполнены")
                    pass
                conn = sq.connect('data.db')
                cursor = conn.cursor()
                cmd = "SELECT id FROM '" + admin[4] + "'"
                cursor.execute(cmd)
                res = cursor.fetchall()
                print(res)
                for i in res:
                    if int(number) == i[0]:
                        popupmsg("Данный номер уже существует")
                        return
                cmd = "SELECT rooms FROM hotels WHERE id = {id}".format(id=int(admin[4]))
                cursor.execute(cmd)
                max_rooms = int(cursor.fetchall()[0][0])
                if int(number) > max_rooms:
                    popupmsg("Номер комнаты превышает максимальный для этой гостиницы")
                    return

                cmd = "INSERT INTO '{hotel}' VALUES ({number}, {rooms}, {area}, 0)".format(hotel=admin[4],
                                                                                        number=number,
                                                                                        rooms=rooms,
                                                                                        area=area)
                cursor.execute(cmd)
                conn.commit()
                update_rooms_list()
                conn.close()


            add_room_window = Tk()
            WINDOWS.append(add_room_window)
            add_room_window.title("Добавить гостиницу")
            add_room_window.geometry("300x200")
            w = add_room_window.winfo_pointerx()
            h = add_room_window.winfo_pointery()
            w = w - 200  # смещение от середины
            h = h - 200
            add_room_window.geometry('300x120+{}+{}'.format(w, h))
            add_room_window.maxsize(300, 120)
            add_room_window.minsize(300, 120)

            number_form = Entry(add_room_window, width=35)
            Label(add_room_window, text="Номер: ").grid(row=1, column=30)
            number_form.grid(row=1, column=50)

            rooms_form = Entry(add_room_window, width=35)
            Label(add_room_window, text="Комнат: ").grid(row=4, column=30)
            rooms_form.grid(row=4, column=50)

            area_form = Entry(add_room_window, width=35)
            Label(add_room_window, text="Площадь: ").grid(row=7, column=30)
            area_form.grid(row=7, column=50)



            Button(add_room_window, text="Сохранить", command=create, width=30).grid(row=29, column=50)
            Button(add_room_window, text="Отмена", command=lambda: add_room_window.destroy(), width=30).grid(row=30,
                                                                                                               column=50)

            add_room_window.mainloop()

        def edit_room(rm):

            def delete_room(number):

                conn = sq.connect('data.db')
                cursor = conn.cursor()
                cmd = "SELECT isFree FROM '{hotel}' WHERE id = {number}".format(hotel=admin[4], number=number)
                cursor.execute(cmd)
                isFree = cursor.fetchall()[0][0]
                if isFree == 0:
                    cmd = "DELETE FROM '{hotel}' WHERE id = {number}".format(hotel=admin[4], number=number)
                    cursor.execute(cmd)
                else:
                    popupmsg("Нельзя удалть номер т.к в нём проживает постоялец")
                conn.commit()
                conn.close()
                update_rooms_list()
                add_room_window.destroy()

            def create(number):
                area = area_form.get()
                rooms = rooms_form.get()

                if area == '' or rooms == '':
                    popupmsg("Все поля должны быть заполнены")
                    pass


                cmd = "UPDATE '{hotel}' SET rooms={rooms}, area={area} WHERE id={number}".format(hotel=admin[4],
                                                                                        number=number,
                                                                                        rooms=rooms,
                                                                                        area=area)
                conn = sq.connect('data.db')
                cursor = conn.cursor()
                cursor.execute(cmd)
                conn.commit()
                conn.close()
                update_rooms_list()



            add_room_window = Tk()
            WINDOWS.append(add_room_window)
            add_room_window.title("Редактировать комнату")
            add_room_window.geometry("300x200")
            w = add_room_window.winfo_pointerx()
            h = add_room_window.winfo_pointery()
            w = w - 200  # смещение от середины
            h = h - 200
            add_room_window.geometry('300x120+{}+{}'.format(w, h))
            add_room_window.maxsize(300, 120)
            add_room_window.minsize(300, 120)

            v1 = StringVar(add_room_window, value=str(rm[1]))
            rooms_form = Entry(add_room_window, width=35, text=v1)
            Label(add_room_window, text="Комнат: ").grid(row=4, column=30)
            rooms_form.grid(row=4, column=50)

            v2 = StringVar(add_room_window, value=str(rm[2]))
            area_form = Entry(add_room_window, width=35, text=v2)
            Label(add_room_window, text="Площадь: ").grid(row=7, column=30)
            area_form.grid(row=7, column=50)

            Button(add_room_window, text="Сохранить", command=lambda x=rm[0]: create(x), width=30).grid(row=29, column=50)
            Button(add_room_window, text="Удалить", command=lambda x=rm[0]: delete_room(x), width=30).grid(row=30, column=50)
            Button(add_room_window, text="Отмена", command=lambda: add_room_window.destroy(), width=30).grid(row=31, column=50)

            add_room_window.mainloop()

        def update_rooms_list():
            global ROOMS_BUTTONS
            conn = sq.connect('data.db')
            cursor = conn.cursor()
            cmd = "SELECT * FROM '" + admin[4] + "'"
            cursor.execute(cmd)
            rooms_list = cursor.fetchall()
            conn.close()

            for h in ROOMS_BUTTONS:
                try:
                    h.destroy()



                except:
                    continue

            for i in range(len(rooms_list)):

                if rooms_list[i][3] == 0:
                    txt = "Комнана номер {number}\nКомнат: {rooms}\nПлощадь: {area}\nСвободен ".format(
                        number=rooms_list[i][0],
                        rooms=rooms_list[i][1],
                        area=rooms_list[i][2])
                    b = Button(rooms_sfr.viewPort, text=txt, width=60, fg="green",
                     command=lambda x=rooms_list[i]: edit_room(x))
                    # command=lambda x=hotels_list[i]: edit_hotel(x))
                    ROOMS_BUTTONS.append(b)
                    b.grid(column=1, row=i)
                else:
                    txt = "Комнана номер {number}\nКомнат: {rooms}\nПлощадь: {area}\nЗанят ".format(
                        number=rooms_list[i][0],
                        rooms=rooms_list[i][1],
                        area=rooms_list[i][2])
                    b = Button(rooms_sfr.viewPort, text=txt, width=60, fg="red",
                     command=lambda x=rooms_list[i]: edit_room(x))
                    ROOMS_BUTTONS.append(b)
                    b.grid(column=1, row=i)

        def update_hosters_list():

            global HOSTERS_BUTTONS
            global HOSTERS_BUTTONS_CB
            conn = sq.connect('data.db')
            cursor = conn.cursor()
            cmd = "SELECT * FROM hosters WHERE hotel = 0 OR hotel = " + str(admin[4])
            cursor.execute(cmd)
            hosters_list = cursor.fetchall()
            conn.close()

            for h in HOSTERS_BUTTONS:

                h[0].destroy()

            for h in HOSTERS_BUTTONS_CB:

                h[1].destroy()


            HOSTERS_BUTTONS_CB = []
            HOSTERS_BUTTONS = []
            for i in range(len(hosters_list)):

                if hosters_list[i][10] == 0:
                    txt = "{lastname} {name} {middlename}\nНе заселён".format(lastname=hosters_list[i][1],
                                                                              name=hosters_list[i][2],
                                                                              middlename=hosters_list[i][3])
                    fg = "red"

                else:
                    txt = "{lastname} {name} {middlename}\nПроживает в номере {number}".format(lastname=hosters_list[i][1],
                                                                              name=hosters_list[i][2],
                                                                              middlename=hosters_list[i][3],
                                                                              number=hosters_list[i][10])
                    fg = "black"
                b = Button(hosters_sfr.viewPort, text=txt, command=lambda x=hosters_list[i]: edit_hoster(x), width=55, fg=fg)
                HOSTERS_BUTTONS.append([b, hosters_list[i][0]])
                a = IntVar()
                cb = Checkbutton(hosters_sfr.viewPort, variable=a, onvalue=hosters_list[i][0], offvalue=0, width=3,
                                height=2 )
                cb.deselect()
                HOSTERS_BUTTONS_CB.append((a, cb, hosters_list[i][0]))
                b.grid(column=1, row=i)
                cb.grid(column=2, row=i)

        def edit_hoster(result):
            def create(id_):
                lastname = lastname_form.get()
                name = name_form.get()
                middlename = middlename_form.get()
                birth = birth_form.get()
                numberphone = numberphone_form.get()
                pasport = pasport_form.get()
                sex = sexvar.get()
                conn = sq.connect("data.db")
                cursor = conn.cursor()
                if lastname == '' or name == '' or middlename == '' or birth == '' or numberphone == '' or pasport == '':
                    popupmsg("Все поля должны быть заполнены")
                    pass
                cmd = "UPDATE hosters SET lastname = '{lastname}', name = '{name}',  middlename = '{middlename}'," \
                      " birthdate = '{birth}', sex = '{sex}', " \
                      "numberphone = '{numberphone}', pasport = '{pasport}'" \
                      "WHERE id = {id}".format(id=id_,
                                     lastname=lastname,
                                     name=name,
                                     middlename=middlename,
                                     birth=birth,
                                     sex=sex,
                                     numberphone=numberphone,
                                     pasport=pasport,
                                     )
                cursor.execute(cmd)
                conn.commit()
                update_hosters_list()
                conn.close()

            def checkin(id_):
                def ckn():
                    from fpdf import FPDF
                    room = int(v8.get().split()[2])
                    d = ddt.get()
                    if d == '':
                        popupmsg("Введите дату выселения")
                        pass
                    dirr = str(fd.asksaveasfilename(defaultextension='*.pdf', filetypes=(("Документ PDF", "*.pdf"),)))
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.add_font('FreeSans', '', 'FreeSans.ttf', uni=True)
                    pdf.set_font("FreeSans", size=20)

                    pdf.cell(180, 8, txt="Документ о зеселении", ln=1, align='C')
                    pdf.set_font("FreeSans", size=15)
                    pdf.cell(180, 8, txt="Сведения о постояльце", ln=5, align='C')
                    pdf.set_font("FreeSans", size=12)
                    pdf.cell(100, 8, txt="Имя: " + str(result[1]), ln=8)
                    pdf.cell(100, 8, txt="Фамилия: " + str(result[2]), ln=9)
                    pdf.cell(100, 8, txt="Отчество: " + str(result[3]), ln=10)
                    pdf.cell(100, 8, txt="Гостиница номер " + str(admin[4]), ln=11)
                    pdf.cell(100, 8, txt="Номер: " + str(room), ln=12)
                    pdf.cell(100, 8, txt="Дата выселения: " + d, ln=13)

                    pdf.set_font("FreeSans", size=15)
                    pdf.cell(180, 8, txt="Сведения об администраторе", ln=20, align='C')
                    pdf.set_font("FreeSans", size=12)
                    pdf.cell(100, 8, txt="Имя: " + str(admin[7]), ln=8)
                    pdf.cell(100, 8, txt="Фамилия: " + str(admin[9]), ln=9)
                    pdf.cell(100, 8, txt="Отчество: " + str(admin[8]), ln=10)


                    pdf.output(dirr)
                    hstcnt = result[8]+1
                    conn = sq.connect('data.db')
                    cursor = conn.cursor()
                    cmd = "UPDATE hosters SET hstcount = {hstcount}, hotel = {hotel}, number = {room} WHERE id = {id}".format(hstcount=hstcnt,
                                                                                                              hotel=admin[4],
                                                                                                              room=room,
                                                                                                              id=id_)
                    cursor.execute(cmd)
                    cmd = "UPDATE '{hotel}' SET isFree = 1 WHERE id = {room}".format(room=room, hotel=admin[4])
                    cursor.execute(cmd)
                    conn.commit()
                    conn.close()
                    update_hosters_list()
                    update_rooms_list()
                    checkin_window.destroy()
                    add_hoster_window.destroy()



                conn = sq.connect('data.db')
                cursor = conn.cursor()
                update_rooms_list()
                cmd = "SELECT id FROM '{}' WHERE isFree = 0".format(admin[4])
                cursor.execute(cmd)
                tempd = cursor.fetchall()
                conn.close()
                # print(tempd)
                lst = []
                for i in tempd:
                    txt = "Комната номер " + str(i[0])
                    lst.append(txt)

                if len(lst) == 0:

                    popupmsg("Все номера заняты")
                    return
                checkin_window = Tk()
                WINDOWS.append(add_hoster_window)
                checkin_window.title("Заселить постояльца")
                checkin_window.geometry("300x250")
                w = checkin_window.winfo_pointerx()
                h = checkin_window.winfo_pointery()
                w = w - 200  # смещение от середины
                h = h - 200
                checkin_window.geometry('300x120+{}+{}'.format(w, h))
                checkin_window.maxsize(300, 120)
                checkin_window.minsize(300, 120)


                v8 = StringVar(checkin_window, value=lst[0])


                Label(checkin_window, text="Номер: ").grid(row=19, column=30)
                room_menu = ttk.Combobox(checkin_window, state="readonly",
                                          values=lst, textvariable=v8, width=32)
                room_menu.grid(row=19, column=50)
                Label(checkin_window, text="Дата\nвыселения: ").grid(row=20, column=30)
                ddt = Entry(checkin_window, width=30)
                ddt.grid(row=20, column=50)
                Button(checkin_window, text="Заселить", command=ckn, width=30).grid(row=22, column=50)
                Button(checkin_window, text="Отмена", command=checkin_window.destroy, width=30).grid(row=25, column=50)

            def checkout(id_):

                def ckn():

                    conn = sq.connect('data.db')
                    cursor = conn.cursor()
                    room = result[10]
                    from fpdf import FPDF

                    d = ddt.get()
                    if d == '':
                        popupmsg("Введите дату выселения")
                        pass
                    dirr = str(fd.asksaveasfilename(defaultextension='*.pdf', filetypes=(("Документ PDF", "*.pdf"),)))
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.add_font('FreeSans', '', 'FreeSans.ttf', uni=True)
                    pdf.set_font("FreeSans", size=20)

                    pdf.cell(180, 8, txt="Документ о выселении", ln=1, align='C')
                    pdf.set_font("FreeSans", size=15)
                    pdf.cell(180, 8, txt="Сведения о постояльце", ln=5, align='C')
                    pdf.set_font("FreeSans", size=12)
                    pdf.cell(100, 8, txt="Имя: " + str(result[1]), ln=8)
                    pdf.cell(100, 8, txt="Фамилия: " + str(result[2]), ln=9)
                    pdf.cell(100, 8, txt="Отчество: " + str(result[3]), ln=10)
                    pdf.cell(100, 8, txt="Гостиница номер " + str(admin[4]), ln=11)
                    pdf.cell(100, 8, txt="Номер: " + str(room), ln=12)
                    pdf.cell(100, 8, txt="Дата выселения: " + d, ln=13)

                    pdf.set_font("FreeSans", size=15)
                    pdf.cell(180, 8, txt="Сведения об администраторе", ln=20, align='C')
                    pdf.set_font("FreeSans", size=12)
                    pdf.cell(100, 8, txt="Имя: " + str(admin[7]), ln=8)
                    pdf.cell(100, 8, txt="Фамилия: " + str(admin[9]), ln=9)
                    pdf.cell(100, 8, txt="Отчество: " + str(admin[8]), ln=10)
                    pdf.output(dirr)
                    cmd = "UPDATE hosters SET  hotel = 0, number = 0 WHERE id = {id}".format(id=id_)
                    cursor.execute(cmd)
                    cmd = "UPDATE '{hotel}' SET isFree = 0 WHERE id = {room}".format(room=room, hotel=admin[4])
                    cursor.execute(cmd)
                    conn.commit()
                    conn.close()
                    update_hosters_list()
                    update_rooms_list()
                    checkout_window.destroy()
                    add_hoster_window.destroy()

                checkout_window = Tk()
                WINDOWS.append(add_hoster_window)
                checkout_window.title("Выселить постояльца")
                checkout_window.geometry("300x250")
                w = checkout_window.winfo_pointerx()
                h = checkout_window.winfo_pointery()
                w = w - 200  # смещение от середины
                h = h - 200
                checkout_window.geometry('300x100+{}+{}'.format(w, h))
                checkout_window.maxsize(300, 100)
                checkout_window.minsize(300, 100)

                Label(checkout_window, text="Дата\nвыселения: ").grid(row=20, column=30)
                ddt = Entry(checkout_window, width=30)
                ddt.grid(row=20, column=50)
                Button(checkout_window, text="Выселить", command=ckn, width=30).grid(row=22, column=50)
                Button(checkout_window, text="Отмена", command=checkout_window.destroy, width=30).grid(row=25, column=50)

            def delete(id_):
                global HOSTERS_BUTTONS_CB
                global HOSTERS_BUTTONS
                if int(result[10]) == 0:



                    conn = sq.connect("data.db")
                    cursor = conn.cursor()
                    cmd = "DELETE FROM hosters WHERE id = {}".format(id_)
                    cursor.execute(cmd)
                    conn.commit()
                    conn.close()

                    update_hosters_list()
                    add_hoster_window.destroy()
                else:
                    popupmsg("Невозможно удалить постояльца\nт.к он проживает в гостинце")
                    return

            def export_to_csv_single():
                import csv
                dirr = str(fd.asksaveasfilename(defaultextension='*.csv', filetypes=(("Документ CSV", "*.csv"),)))

                with open(dirr, 'w', encoding="utf-8") as f:
                    fnames = ["Фамилия", "Имя", "Отчество", "Дата рождения", "Пол", "Номер телефона", "Номер паспорта",
                              "Гостиница", "Номер", "Число заселений"]
                    writer = csv.DictWriter(f, fieldnames=fnames,
                             quoting=csv.QUOTE_MINIMAL, dialect='excel')

                    writer.writeheader()
                    writer.writerow({
                        'Фамилия': str(result[1]),
                        'Имя': str(result[2]),
                        'Отчество': str(result[3]),
                        'Дата рождения': str(result[4]),
                        'Пол': str(result[5]),
                        'Номер телефона': str(result[6]),
                        'Номер паспорта': str(result[7]),
                        'Гостиница': str(result[9]),
                        'Номер': str(result[10]),
                        'Число заселений': str(result[8]),

                    })

            add_hoster_window = Tk()
            WINDOWS.append(add_hoster_window)
            add_hoster_window.title("Редактировать постояльца")
            add_hoster_window.geometry("300x250")
            w = add_hoster_window.winfo_pointerx()
            h = add_hoster_window.winfo_pointery()
            w = w - 200  # смещение от середины
            h = h - 200
            add_hoster_window.geometry('300x360+{}+{}'.format(w, h))
            add_hoster_window.maxsize(300, 360)
            add_hoster_window.minsize(300, 360)

            v1 = StringVar(add_hoster_window, value=result[1])
            lastname_form = Entry(add_hoster_window, width=35, text=v1)
            Label(add_hoster_window, text="Фамилия: ").grid(row=1, column=30)
            lastname_form.grid(row=1, column=50)

            v2 = StringVar(add_hoster_window, value=result[2])
            name_form = Entry(add_hoster_window, width=35, text=v2)
            Label(add_hoster_window, text="Имя: ").grid(row=4, column=30)
            name_form.grid(row=4, column=50)

            v3 = StringVar(add_hoster_window, value=result[3])
            middlename_form = Entry(add_hoster_window, width=35, text=v3)
            Label(add_hoster_window, text="Отчество: ").grid(row=7, column=30)
            middlename_form.grid(row=7, column=50)

            v4 = StringVar(add_hoster_window, value=result[4])
            birth_form = Entry(add_hoster_window, width=35, text=v4)
            Label(add_hoster_window, text="Дата\nрождения: ").grid(row=10, column=30)
            birth_form.grid(row=10, column=50)

            v5 = StringVar(add_hoster_window, value=result[6])
            numberphone_form = Entry(add_hoster_window, width=35, text=v5)
            Label(add_hoster_window, text="Номер\nтелефона: ").grid(row=14, column=30)
            numberphone_form.grid(row=14, column=50)

            v6 = StringVar(add_hoster_window, value=result[7])
            pasport_form = Entry(add_hoster_window, width=35, text=v6)
            Label(add_hoster_window, text="Номер\nпаспорта: ").grid(row=17, column=30)
            pasport_form.grid(row=17, column=50)

            v7 = StringVar(add_hoster_window, value=result[5])
            sexvar = StringVar(add_hoster_window, value="")
            male = Radiobutton(add_hoster_window, text="Мужчина", variable=sexvar, value="Мужчина")
            female = Radiobutton(add_hoster_window, text="Женщина", variable=sexvar, value="Женщина")
            Label(add_hoster_window, text="Пол: ").grid(row=20, column=30)
            male.grid(row=20, column=50)
            female.grid(row=21, column=50)
            if v7.get() in "Мужчина":
                male.select()
                print(11)
            else:
                female.select()
            print(v1.get(), v2.get(), v3.get(), v4.get(), v5.get(), v6.get(), v7.get())
            Button(add_hoster_window, text="Сохранить", command=lambda x=result[0]: create(x), width=30).grid(row=29, column=50)
            if result[10] == 0:
                Button(add_hoster_window, text="Заселить", width=30, command=lambda x=result[0]: checkin(x)).grid(row=30, column=50)
            else:
                Button(add_hoster_window, text="Выселить", command=lambda x=result[0]: checkout(x), width=30).grid(row=30, column=50)
            Button(add_hoster_window, text="Экспорт в CSV", width=30, command=export_to_csv_single).grid(row=31, column=50)
            Button(add_hoster_window, text="Удалить", command=lambda x=result[0]: delete(x), width=30).grid(row=32, column=50)
            Button(add_hoster_window, text="Отмена", command=lambda: add_hoster_window.destroy(), width=30).grid(row=33,
                                                                                                                 column=50)
            add_hoster_window.mainloop()

        def add_hoster():

            def create():
                lastname = lastname_form.get()
                name = name_form.get()
                middlename = middlename_form.get()
                birth = birth_form.get()
                numberphone = numberphone_form.get()
                pasport = pasport_form.get()
                sex = sexvar.get()
                if lastname == '' or name == '' or middlename == '' or birth == '' or numberphone == '' or pasport == '':
                    popupmsg("Все поля должны быть заполнены")
                    pass
                conn = sq.connect('data.db')
                cursor = conn.cursor()
                cmd = "SELECT MAX(id) FROM hosters"
                cursor.execute(cmd)
                res = cursor.fetchall()
                print(res)
                if res[0][0] == None:
                    id_ = 1
                else:
                    id_ = int(res[0][0]) + 1
                cmd = "INSERT INTO hosters VALUES ({id}, '{lastname}', '{name}',  '{middlename}', '{birth}', '{sex}', '{numberphone}', '{pasport}'," \
                      "0, 0, 0)".format(id=id_,
                                     lastname=lastname,
                                     name=name,
                                     middlename=middlename,
                                     birth=birth,
                                     sex=sex,
                                     numberphone=numberphone,
                                     pasport=pasport)
                cursor.execute(cmd)
                conn.commit()
                update_hosters_list()
                conn.close()

            add_hoster_window = Tk()
            WINDOWS.append(add_hoster_window)
            add_hoster_window.title("Добавить постояльца")
            add_hoster_window.geometry("300x250")
            w = add_hoster_window.winfo_pointerx()
            h = add_hoster_window.winfo_pointery()
            w = w - 200  # смещение от середины
            h = h - 200
            add_hoster_window.geometry('300x290+{}+{}'.format(w, h))
            add_hoster_window.maxsize(300, 290)
            add_hoster_window.minsize(300, 290)

            lastname_form = Entry(add_hoster_window, width=35)
            Label(add_hoster_window, text="Фамилия: ").grid(row=1, column=30)
            lastname_form.grid(row=1, column=50)

            name_form = Entry(add_hoster_window, width=35)
            Label(add_hoster_window, text="Имя: ").grid(row=4, column=30)
            name_form.grid(row=4, column=50)

            middlename_form = Entry(add_hoster_window, width=35)
            Label(add_hoster_window, text="Отчество: ").grid(row=7, column=30)
            middlename_form.grid(row=7, column=50)

            birth_form = Entry(add_hoster_window, width=35)
            Label(add_hoster_window, text="Дата\nрождения: ").grid(row=10, column=30)
            birth_form.grid(row=10, column=50)

            numberphone_form = Entry(add_hoster_window, width=35)
            Label(add_hoster_window, text="Номер\nтелефона: ").grid(row=14, column=30)
            numberphone_form.grid(row=14, column=50)

            pasport_form = Entry(add_hoster_window, width=35)
            Label(add_hoster_window, text="Номер\nпаспорта: ").grid(row=17, column=30)
            pasport_form.grid(row=17, column=50)

            sexvar = StringVar(add_hoster_window, value="")
            male = Radiobutton(add_hoster_window, text="Мужчина", variable=sexvar, value="Мужчина")
            female = Radiobutton(add_hoster_window, text="Женщина", variable=sexvar, value="Женщина")
            Label(add_hoster_window, text="Пол: ").grid(row=20, column=30)
            male.grid(row=20, column=50)
            female.grid(row=21, column=50)
            male.select()

            Button(add_hoster_window, text="Сохранить", command=create, width=30).grid(row=29, column=50)
            Button(add_hoster_window, text="Отмена", command=lambda: add_hoster_window.destroy(), width=30).grid(row=30, column=50)
            add_hoster_window.mainloop()

        def select_all():
            for i in HOSTERS_BUTTONS_CB:
                i[1].select()

        def deselect_all():
            for i in HOSTERS_BUTTONS_CB:
                i[1].deselect()

        def sds():
            state = select_state.get()
            if state == 0:
                select_state.set(1)
                sds_all.config(text="Убрать всех")
                select_all()
            else:
                select_state.set(0)
                sds_all.config(text="Выбрать всех")
                deselect_all()

        def export_to_csv_many():

            a = [-1, 0]
            for i in HOSTERS_BUTTONS_CB:
                if i[0].get() != 0:
                    a.append(i[0].get())
            a = tuple(a)
            print(str(a))

            import csv
            dirr = str(fd.asksaveasfilename(defaultextension='*.csv', filetypes=(("Документ CSV", "*.csv"),)))

            conn = sq.connect("data.db")
            cursor = conn.cursor()
            cmd = "SELECT * FROM hosters WHERE id IN " + str(a)
            cursor.execute(cmd)
            res = cursor.fetchall()
            print(res)
            with open(dirr, 'w', encoding="utf-8") as f:
                fnames = ["Фамилия", "Имя", "Отчество", "Дата рождения", "Пол", "Номер телефона", "Номер паспорта",
                          "Гостиница", "Номер", "Число заселений"]
                writer = csv.DictWriter(f, fieldnames=fnames,
                                        quoting=csv.QUOTE_MINIMAL, dialect='excel')

                writer.writeheader()
                for result in res:
                    print(result)
                    writer.writerow({
                        'Фамилия': str(result[1]),
                        'Имя': str(result[2]),
                        'Отчество': str(result[3]),
                        'Дата рождения': str(result[4]),
                        'Пол': str(result[5]),
                        'Номер телефона': str(result[6]),
                        'Номер паспорта': str(result[7]),
                        'Гостиница': str(result[9]),
                        'Номер': str(result[10]),
                        'Число заселений': str(result[8]),

                    })



        mainWindow = Tk()
        WINDOWS.append(mainWindow)
        mainWindow.title("Администратор гостиницы")
        mainWindow.geometry("1000x500")
        mainWindow.resizable(False, False)
        w = mainWindow.winfo_screenwidth()  # ширина экрана
        h = mainWindow.winfo_screenheight()  # высота экрана
        w = w // 2  # середина экрана
        h = h // 2
        w = w - 1000 // 2  # смещение от середины
        h = h - 500 // 2
        mainWindow.geometry('1000x500+{}+{}'.format(w, h))

        rooms_fr = Frame(mainWindow, width=450, height=400, relief=RIDGE)
        rooms_sfr = ScrollFrame(rooms_fr, width=450, height=400)

        hosters_fr = Frame(mainWindow, width=450, height=400, relief=RIDGE)
        hosters_sfr = ScrollFrame(rooms_fr, width=450, height=400)

        add_room_button = Button(mainWindow, text="Добавить комнату", width=60, command=add_room)
        add_hoster_button = Button(mainWindow, text="Добавить постояльца", width=61, command=add_hoster)
        add_room_button.place(x=500, y=50)
        add_hoster_button.place(x=50, y=20)
        rooms_fr.pack(side="top", fill="both", expand=True)
        rooms_sfr.place(x=500, y=80)
        select_state = IntVar(value=0)
        sds_all = Button(mainWindow, text="Выбрать всех", width=11, command=sds)
        export_to_csv_button = Button(mainWindow, text="Экспорт в csv", width=11, command=export_to_csv_many)
        export_to_csv_button.place(x=300, y=50)
        sds_all.place(x=400, y=50)
        hosters_sfr.place(x=50, y=80)
        update_rooms_list()
        update_hosters_list()
        mainWindow.mainloop()


def program(result):
    if result[3] == 'manager':
        program_manager(result)
    if result[3] == 'admin':
        program_admin(result)


ATTEMPS = int(open("attemps", 'r').read())
if ATTEMPS <= 0:
    systemlock()
else:
    login()
