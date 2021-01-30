from sqlite3 import *
from tkinter import *
from tkinter import messagebox
from mainProg import mainFunc

class Db:
	def __init__(sf):
		sf.c = connect("clist.db")
		sf.cur = sf.c.cursor()

		try:
			sf.cur.execute("create table clist (alph varchar(1) PRIMARY KEY ,paath varchar(200))")
			for i in range(ord('a'),ord('z')+1):
				sf.cur.execute("insert into clist(alph, paath) values(%r,%r)"%(chr(i),"print('none')"))
		except:
			pass

			

		sf.mainpage()	


	def mainpage(sf):
		#window
		sf.scr = Tk()  
		sf.scr.geometry('1003x768')  
		sf.scr.title('Gesture Recognition Program')
		sf.scr['bg']='white'


		sf.back=PhotoImage(file="ges1.png")
		Label(sf.scr, image=sf.back).place(x=0, y=0, relwidth=1, relheight=1)



		Label(sf.scr, text='GESTURE RECOGNITION PROGRAM',bg="black",fg='white',font=("arial",30),padx=10, pady=3).place(relx=0.18,rely=0.11)
		Label(sf.scr, text='based on python',bg="black",fg='white',font=("arial",34),padx=10, pady=3).place(relx=0.5,rely=0.21)


		Button(sf.scr, text="View Command List",font=("helvetica",18),bg='royal blue', padx=50, pady=8, command=sf.show).place(relx=0.5,rely=0.55,anchor="center")

		Button(sf.scr, text=" START ",font=("helvetica",18),bg='royal blue', padx=50, pady=8, command=sf.runner).place(relx=0.5,rely=0.65,anchor="center")

		Button(sf.scr, text="Add Command",font=("helvetica",18),bg='royal blue', padx=50, pady=8, command=sf.add).place(relx=0.5,rely=0.75,anchor="center")


		#camera access
		#sf.varC stores url or port number for camera access
		sf.varC = StringVar(sf.scr,value='0')
		Label(sf.scr, text= 'Camera port/URL:',font=("arial",10)).place(relx=0.7,rely=0.65)
		sf.ent = Entry(sf.scr,textvariable= sf.varC).place(relx=0.82, rely=0.65)
		
		#quit button
		Button(sf.scr, text="QUIT",font=("helvetica",14),fg='purple',bg='white', padx=8, command=sf.closecmd).place(relx=0.92,rely=0.01)


		sf.scr.mainloop()	

	def closecmd(sf):
		sf.scr.destroy()

	def getURL(sf):
		return sf.varC


	def add(sf):
		try:
			sf.scr.destroy()
		except:
			sf.showscr.destroy()	

		sf.addscr = Tk(className="EDIT Command")
		sf.addscr.geometry('1003x768')  
		sf.addscr.title('Edit Window')

		sf.aback=PhotoImage(file="ges2.png")
		sf.abackground_label = Label(sf.addscr, image=sf.aback)
		sf.abackground_label.place(x=0, y=0, relwidth=1, relheight=1)

		Label(sf.addscr, text='YOUR COMMANDS',bg="light blue",fg='black',font=("arial",35),padx=15, pady=4).place(relx=0.37,rely=0.22)
		
		Label(sf.addscr,text="Command Type:",bg="light blue",fg='black',font=("arial",18)).place(relx=0.37,rely=0.45)
		sf.radio = IntVar()
		Radiobutton(sf.addscr,text='hotkey',fg='black',font=("arial",16),variable=sf.radio,value=1).place(relx=0.56,rely=0.45)
		Radiobutton(sf.addscr,text='path',fg='black',font=("arial",16),variable=sf.radio,value=2).place(relx=0.67,rely=0.45)


		sf.en11 = StringVar(sf.addscr)
		sf.en22 = StringVar(sf.addscr)
		Label(sf.addscr,text="Alphabet:",bg="light blue",fg='black',font=("arial",16)).place(relx=0.37,rely=0.55)
		sf.en1 = Entry(sf.addscr,textvariable=sf.en11).place(relx=0.56,rely=0.55)
		Label(sf.addscr,text="Input command:",bg="light blue",fg='black',font=("arial",16)).place(relx=0.37,rely=0.65)
		sf.en2 = Entry(sf.addscr,textvariable=sf.en22).place(relx=0.56,rely=0.65)

		Button(sf.addscr,text="ADD",bg='white',fg='blue',font=("arial",25),command=sf.commiter).place(relx=0.5,rely=0.75)

		Button(sf.addscr, text="BACK",font=("helvetica",14),fg='purple',bg='white', padx=8, command=sf.backcmd).place(relx=0.92,rely=0.01)
	

	def commiter(sf):

		if len(sf.en11.get())>1 or len(sf.en11.get())==0:
			messagebox.showinfo("warning","NOT AN ALPHABET")
			return
		if len(sf.en22.get())==0:
			messagebox.showinfo("warning","NO COMMAND")
			return


		if(sf.radio.get()==1):
			sf.st = "pyautogui.press('" + str(sf.en22.get()) + "')"
		elif sf.radio.get()==2:
			sf.st = "os.popen('" + str(sf.en22.get()) + "')"	
		else:
			messagebox.showinfo("warning","TYPE NOT SELECTED")
			return	

		sf.cur.execute("update clist set paath = %r where alph = %r"%(sf.st,sf.en11.get()))
		sf.c.commit()
		sf.addscr.destroy()
		sf.mainpage()


	def show(sf):
		sf.scr.destroy()

		sf.showscr = Tk(className= "Command List")  
		sf.showscr.geometry('1003x768')  
		sf.showscr.title('cmd list')
		sf.showscr['bg']='white'


		sf.sback = PhotoImage(file="ges.png")
		sf.sbackground_label = Label(sf.showscr, image=sf.sback)
		sf.sbackground_label.place(x=0,y=0,relheight=1,relwidth=1)

		sf.f2 = Frame(sf.showscr, width=1350, height=650 ,bd=8,relief="raise")
		sf.f2.pack(side=BOTTOM)

		sf.cmshow=Text(sf.f2,width=90,height=30,bg="white",bd=8,font=('arial',11,'bold'))
		sf.cmshow.grid(row=0,column=3)

		Button(sf.f2,text="BACK",font=("helvetica",18),bg='royal blue',command=sf.remenu).grid(row=0,column=2)

		Button(sf.f2,text="EDIT CMD",font=("helvetica",18),bg='royal blue',command=sf.add).grid(row=1,column=2)

		sf.cur.execute("select * from clist")
		sf.res = sf.cur.fetchall()
		for i in sf.res:
			sf.cmshow.insert(END,'\t' + i[0]+ '\t\t' + str(i[1]) + '\n')

	def backcmd(sf):
		sf.addscr.destroy()
		sf.mainpage()

	def remenu(sf):
		sf.showscr.destroy()
		sf.mainpage()		

	def runner(sf):
		sf.scr.destroy()
		mainFunc(str(sf.varC.get()))

s = Db()			