import sqlite3
import tkinter
from tkinter import *
from tkinter import ttk, messagebox

def mk():
    cur.execute("CREATE TABLE IF NOT EXISTS inventory (urun TEXT,marka TEXT, adet INT, kod INTEGER primary key autoincrement, timestamp DATE DEFAULT (datetime('now','localtime')))")

def add3():
    urun = entry6.get()
    marka = entry7.get()
    adet = entry5.get()
    kod = entry8.get()
    if kod == "":
        trxt = "Lütfen kod alanını doldurunuz!"
    if urun != "":
        trxt="Veri Değişti!"
        cur.execute("UPDATE inventory SET urun = ? WHERE kod = ?;", (urun, kod))
        con.commit()
        entry5.delete(0, END)
        entry6.delete(0, END)
        entry7.delete(0, END)
        entry8.delete(0, END)
    if marka != "":
        trxt="Veri Değişti!"
        cur.execute("UPDATE inventory SET marka = ? WHERE kod = ?;", (marka, kod))
        con.commit()
        entry5.delete(0, END)
        entry6.delete(0, END)
        entry7.delete(0, END)
        entry8.delete(0, END)
    if adet != "":
        trxt="Veri Değişti!"
        cur.execute("UPDATE inventory SET adet = ? WHERE kod = ?;", (adet, kod))
        con.commit()
        entry5.delete(0, END)
        entry6.delete(0, END)
        entry7.delete(0, END)
        entry8.delete(0, END)
    list()
    db_verileri2()
    deleter_set()
    entry8_set()
    l4.config(text=trxt)
    root.after(2000, lambda: l4.config(text=''))

def add2():
    kod = deleter.get()
    cur.execute("""SELECT * FROM inventory WHERE
    kod = ?""", (kod,))
    data = cur.fetchone()
    if data:
        fext = "Veri kaldırıldı!"
        query = "DELETE from inventory where kod = ?"
        cur.execute(query, (kod,))
        con.commit()
        deleter.delete(0, END)
    elif kod == "":
        fext = "Lütfen tüm alanları doldurunuz!"

    else:
        fext = "Lütfen geçerli bir kod giriniz!"

    list()
    db_verileri2()
    deleter_set()
    entry8_set()
    l4.config(text=fext)
    root.after(2000, lambda: l4.config(text=''))

def add():
    urun = entry1.get()
    marka = entry2.get()
    adet = entry3.get()
    if urun == "":
        text = "Lütfen tüm alanları doldurunuz!"
    elif marka == "":
        text = "Lütfen tüm alanları doldurunuz!"
    elif adet == "":
        text = "Lütfen tüm alanları doldurunuz!"
    else:
        text="Veri Eklendi"
        cur.execute("INSERT INTO inventory(urun, marka, adet) VALUES (?, ?, ?)", (urun, marka, adet))
        con.commit()
        entry3.delete(0, END)
        entry2.delete(0, END)
        entry1.delete(0, END)
    list()
    db_verileri2()
    deleter_set()
    entry8_set()
    l4.config(text=text)
    root.after(2000, lambda: l4.config(text=''))

def db_verileri():
    with sqlite3.connect("database.db") as db:
        return db.execute("select * from inventory").fetchall()

def db_verileri2():
    with sqlite3.connect("database.db") as db:
        return db.execute("select kod from inventory").fetchall()

def list():
    treeview.delete(*treeview.get_children())
    veriler = db_verileri()
    for veri in veriler:
        treeview.insert("", index=END, values=(veri[0], veri[1], veri[2], veri[3], veri[4]))

def select():
    veriler = treeview.item(treeview.focus())
    for veri in veriler:
        entry8.insert("", index=END, values=(veri[3]))

def onumber(char):
    return char.isdigit()

root = Tk()
root.geometry("1500x500")
root.title("Database Demo")
root.resizable(width=False, height=False)

con = sqlite3.connect("database.db")
cur = con.cursor()

validation = root.register(onumber)

treeview_frame = ttk.Frame(root)
treeview_frame.grid(row=8, column=5)

scrollbar = ttk.Scrollbar(treeview_frame, orient="vertical")
scrollbar.pack(side=RIGHT, fill=Y)
scrollbar1 = ttk.Scrollbar(treeview_frame, orient="horizontal")
scrollbar1.pack(side=BOTTOM, fill=X)
columns = ("1", "2", "3", "4", "5")
treeview = ttk.Treeview(treeview_frame, yscrollcommand=scrollbar.set, columns=columns, show="headings", height=23)
scrollbar.config(command=treeview.yview)
def selectItem(a):
    curItem = treeview.focus(column=4)
    print(treeview.item(curItem))
treeview.bind('<ButtonRelease-1>', selectItem)
treeview.pack()

treeview.column("4", width=100, anchor=CENTER)
treeview.column("1", width=100)
treeview.column("2", width=100)
treeview.column("3", width=100, anchor=CENTER)
treeview.column("5", width=200)
treeview.heading("1", text="Ürün Adı", anchor=W)
treeview.heading("2", text="Marka Adı", anchor=W)
treeview.heading("4", text="Ürün Kodu", anchor=W)
treeview.heading("5", text="Tarih/Saat", anchor=W)
treeview.heading("3", text="Adet", anchor=W)
###############################################################
l4 = Label(root)
l4.place(x=630, y=450)
l4["font"] = ("Futura", 20)

label4 = Label(text = "Kaldır", font= ("Futura", 20))
label4.place(x = 1250, y = 4)

label7 = Label(text = "Ürün kodu giriniz:")
label7.place(x = 1080, y = 80)
label7.config(padx=0)

n = StringVar()
deleter = ttk.Combobox(root, width = 27, textvariable = n)
deleter.place(x = 1200, y = 80, width=200, height=25)
def deleter_set():
    deleter['values'] = (db_verileri2())

button2 = Button(root, text = "Kaldır", command = add2, highlightthickness = 0, bd = 0, bg = "#828282", fg="white")
button2.place(x = 1280, y = 120)

label = Label(text = "Ekle", font= ("Futura", 20))
label.place(x = 800, y = 4)

label1 = Label(text = "Ürün adı giriniz:")
label1.place(x = 630, y = 40)
label1.config(padx=0)

label2 = Label(text = "Marka adı giriniz:")
label2.place(x = 630, y = 80)
label2.config(padx=0)

label3 = Label(text = "Ürün adeti giriniz:")
label3.place(x = 630, y = 120)
label3.config(padx=0)

entry1 = Entry(root, highlightthickness = 0, bd = 0)
entry1.place(x = 750, y = 40, width=200, height=25)

entry2 = Entry(root, highlightthickness = 0, bd = 0)
entry2.place(x = 750, y = 80, width=200, height=25)

entry3 = Entry(root, highlightthickness = 0, bd = 0, validate="key", validatecommand=(validation, '%S'))
entry3.place(x = 750, y = 120, width=200, height=25)

button1 = Button(root, text = "Ekle", command = add, highlightthickness = 0, bd = 0, bg = "#828282", fg="white")
button1.place(x = 840, y = 160)

########################################################################################################################

label = Label(text = "Değiştir", font= ("Futura", 20))
label.place(x = 800, y = 190)

label6 = Label(text = "Ürün adı giriniz:")
label6.place(x = 630, y = 230)
label6.config(padx=0)

label7 = Label(text = "Marka adı giriniz:")
label7.place(x = 630, y = 270)
label7.config(padx=0)

label8 = Label(text = "Ürün kodu giriniz:")
label8.place(x = 630, y = 310)
label8.config(padx=0)

label5 = Label(text = "Ürün adeti giriniz:")
label5.place(x = 630, y = 350)
label5.config(padx=0)

entry6 = Entry(root, highlightthickness = 0, bd = 0)
entry6.place(x = 750, y = 230, width=200, height=25)

entry7 = Entry(root, highlightthickness = 0, bd = 0)
entry7.place(x = 750, y = 270, width=200, height=25)

n1 = StringVar()
entry8 = ttk.Combobox(root, width = 27, textvariable = n1)
entry8.place(x = 750, y = 310, width=200, height=25)
def entry8_set():
    entry8['values'] = (db_verileri2())

entry5 = Entry(root, highlightthickness = 0, bd = 0, validate="key", validatecommand=(validation, '%S'))
entry5.place(x = 750, y = 350, width=200, height=25)

button1 = Button(root, text = "Değiştir", command = add3, highlightthickness = 0, bd = 0, bg = "#828282", fg="white")
button1.place(x = 840, y = 390)

mk()
list()
deleter_set()
entry8_set()
root.mainloop()