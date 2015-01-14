#!/usr/bin/python 

#For regular expression---------
import re	
import sys

#For GUI --------------

import Tkinter	
import tkFileDialog
from Tkinter import *
import tkFont
import Image
from PIL import Image,ImageTk
from tkFileDialog import askopenfilenames
import tkMessageBox
import ttk


ip_class={}				#	dictionary for storing Vlan and corresponding location
white_list=[]			#	White list for ignoring specific users


#	Writing white listed users in a file ---------------
def addw():

	f=open('wlist.txt','a')
	str=wuser.get()
	ip_win.withdraw()
	
	if str!='' and str not in white_list:
		f.write(str+'\n')
		white_list.append(str)
		f.close()
		

#	GUI to add white listed users ---------------

def add_wlist():
	global ip_win
	ip_win=Tk()
	ip_win.title("Add Whitelisted Users")
	frame=Frame(ip_win,relief=RAISED,height=150,width=550,borderwidth=1,bg='light blue')
	frame.pack(fill=BOTH,expand=1)
	
	ip_text=Label(frame,text='Enter user :',padx=10,pady=10)
	ip_text.pack(side=LEFT)
	
	global wuser
	wuser=Entry(frame,bd=5)
	wuser.pack(side=LEFT)
	
	submitB= Button(frame,text ='Submit', command = addw,fg='white',bg='black',padx=10)
	submitB.pack(side=LEFT)
	
	#	Initializing white_list from file------
def init_wlist():
	f=open('wlist.txt','rU')
	for line in f:
		white_list.append(line.strip())
	#print white_list

#	Initializing ip dictionary from file
def init_dict():
	f=open('dic.txt','rU')
	global ip_class
	#global ip_class_rev
	#ip_class_rev={}
	for line in f:
		ip_class[line.split(':')[0]]=(line.split(':')[1]).strip()
		#ip_class_rev[(line.split(':')[1]).strip()]=line.split(':')[0]
	f.close()

#	Reading selected files as string to buffer
	
def readFiles():
	global buffer
	buffer=""	
	for file in filename:
		f=open(file,'rU')
		buffer=buffer+f.read()
		f.close()
	
#	To simply display content of open logs	
def display():

	global info
	tuple = re.findall(r'(\d\d\-\d\d\-\d\d\d\d)\s(\d\d:\d\d:\d\d)\s-\s(\w+)\s\((\d+.\d+.\d+.\d+)\)', buffer)
	tuple=list(set(tuple))
	
	tuple=sorted(tuple,key=sort_by_time)
	info.delete(0,info.size())
	
	for x in tuple:
		info.insert(END,x[0]+"    "+x[1]+"    "+x[2] + "    "+x[3])

		
		
# 	returns  tuples as time user ip	sorted by time-----------
def sorted_tuple():
	
	tuple = re.findall(r'(\d\d\-\d\d\-\d\d\d\d)\s(\d\d:\d\d:\d\d)\s-\s(\w+)\s\((\d+.\d+.\d+.\d+)\)', buffer)  
	tuple=list(set(tuple))
	tuple=sorted(tuple,key=sort_by_time)
	return tuple
		
		
# adds input ips to ip dictionary		
def submit():

	global statusL
	ip=ip_box.get()
	loc= class_box.get()

	if ip=='' or loc=='':
		statusL.config(text='STATUS: Field can\'t be left blank',fg='red')
	elif ip not in ip_class:
		ip_class[ip]=loc
		statusL.config(fg='dark green')
		statusL.config(text='STATUS: Value Succesfully added',fg='dark green')
		f=open('dic.txt','a')
		f.write(ip+':'+loc+'\n')
		f.close()
	else:
		statusL.config(text='STATUS: Location Already Exist',fg='red')


	
#displays those users that submitted files from outside of exam location
def findCCases(): #find cheating cases
	st=start_time.get()
	et=end_time.get()
	dt=date.get()
	vlan_name=venue.get()
	for key in ip_class.keys():
		if(ip_class[key]== vlan_name):
			vlan=key
			break;
	#vlan=ip_class_rev[vlan_name]
	folder_name=folder.get()
	#print "reached"
	tuple = re.findall(r'(\d\d\-\d\d\-\d\d\d\d)\s(\d\d:\d\d:\d\d)\s-\s(\w+)\s\((\d+.\d+.\d+.\d+)\).+Successfully transferred ' + '\"\/'+folder_name+'\"', buffer)
	#print tuple
	tuple=list(set(tuple))
	tuple=sorted(tuple,key=sort_by_date)
	tuple=list(tuple)
	
	todisplay=set([])    #   
	filew=open("tuplex.txt","w")
	for k in tuple:
		filew.write(str(k[2])+"\n")
	for x in tuple:
		if(dt==x[0]  and  st<=x[1] and et>=x[1] and x[2] not in white_list):
			loc='Unknown with ip '+x[3]
			if(x[3].split(".")[2]!=vlan):
				if x[3].split(".")[2] in ip_class:
					loc=ip_class[x[3].split(".")[2]]
				todisplay.add("User:   "+x[2]+"      Location: "+loc)

	ip_win.withdraw()
	info.delete(0,info.size())
	for user in todisplay:
		info.insert(END,user)

		
# to display users from same ips (only if users per ip >1)
def submit_timeIP():	
	dt=date.get()
	st=start_time.get()
	et=end_time.get()
	#window.withdraw()
	global info
	info.delete(0,info.size())
	IPs={}
	tuple =sorted_tuple()
	for x in tuple:
		if dt==x[0] and st<=x[1] and et>=x[1] : #00:00:00 23:59:59
			#print x[1] + x[2]
			user=x[2] # username
			ip=x[3] #ip
			#info.insert(END,x[0]+"    "+x[1]+"    "+x[2])
			if user not in white_list:
				if ip not in IPs :
					IPs[ip]=[user]
				else:
					if user not in IPs[ip]:
						IPs[ip].append(user)
	# dictionary of ips and users generated within the given time		
	##print string
	time_win.withdraw()
	for key in IPs:
		#info.insert(END,
		STR=key +":   "
		if len(IPs[key])>1:
			for user in IPs[key]:
				STR=STR+"   "+user
			info.insert(END,STR)
		
#display time user ip within input time slot
		
def submit_time():
	st=start_time.get()
	et=end_time.get()
	dt=date.get()
	ip_win.withdraw()
	global info
	info.delete(0,info.size())
	tuple =sorted_tuple()
	for x in tuple:
		if dt==x[0] and st<=x[1] and et>=x[1] and x[2] not in white_list :
			info.insert(END,x[0]+"    "+x[1]+"    "+x[2]+"       "+x[3]+" ")
	
	
	
# selects multiple files and saves to filename
def ChooseFile():
	global filename
	filename = askopenfilenames() # show an "Open" dialog box and return the path to the selected file
	filename= filename.split()
	path=re.search(r'(\S+)(/fzs\S+.log)',filename[0])
	global text	
	text.config(text='STATUS: Folder selected >'+path.group(1)+'                                Number of files selected  : '+ str(len(filename)))
	text.config(fg='dark green')
	readFiles()

# display GUI to add vlan id and its location
def addClass():
	global ip_win
	ip_win=Tk()
	ip_win.title("Add VLAN LOCATION")
	frame=Frame(ip_win,relief=RAISED,height=150,width=550,borderwidth=1,bg='light blue')
	frame.pack(fill=BOTH,expand=1)
	
	ip_text=Label(frame,text='Enter IP\'s VLAN :',padx=10,pady=10)
	ip_text.pack(side=LEFT)
	
	global ip_box
	ip_box=Entry(frame,bd=5)
	ip_box.pack(side=LEFT)
	
	class_text=Label(frame,text='Enter Class/Location : ',padx=10,pady=10)
	class_text.pack(side=LEFT)
	
	global class_box
	class_box=Entry(frame,bd=5)
	class_box.pack(side=LEFT)
	
	global statusL
	statusL=Label(ip_win,text='STATUS: Nothing Submitted',fg='red',relief=RAISED,padx=10)
	statusL.pack(side=LEFT)
	
	submitB= Button(frame,text ='Submit', command = submit,fg='white',bg='black',padx=10)
	submitB.pack(side=LEFT)

# display GUI to report cheating cases
def casestime(): ## creates a window for monitoring
	global ip_win
	ip_win=Tk()
	ip_win.title("Monitor")
	frame=Frame(ip_win,relief=RAISED,height=150,width=550,borderwidth=1,bg='light blue')
	frame.pack(fill=BOTH,expand=1)
	
	dt_text=Label(frame,text='Date:',padx=10,pady=10)
	dt_text.pack(side=LEFT)
	global date 
	date=Entry(frame,bd=5)
	date.pack(side=LEFT)
	
	##print "datem"
	st_text=Label(frame,text='Start Time:',padx=10,pady=10)
	st_text.pack(side=LEFT)
	global start_time
	start_time=Entry(frame,bd=5)
	start_time.pack(side=LEFT)
	
	et_text=Label(frame,text='End Time : ',padx=10,pady=10)
	et_text.pack(side=LEFT)
	global end_time
	end_time=Entry(frame,bd=5)
	end_time.pack(side=LEFT)
	
	##print "Choose venue"
	venue_bt=Label(frame,text='Venue : ',padx=10,pady=10)
	venue_bt.pack(side=LEFT)
	global venue
	venue=ttk.Combobox (frame, textvariable="123", state='readonly')
	venue.pack(side=LEFT)
	venue['values']=ip_class.values()
	#print ip_class.values()
	
	
	global folder
	fr_text=Label(frame,text='Folder : ',padx=10,pady=10)
	fr_text.pack(side=LEFT)
	folder=Entry(frame,bd=5)
	folder.pack(side=LEFT)

	submitB= Button(frame,text ='Submit', command = findCCases,fg='white',bg='black',padx=10)
	submitB.pack(side=LEFT)

	
	
## display GUI to input time slot for multiple ips

def chooseTimeIP():

	global time_win
	time_win=Tk()
	time_win.title("time slot")
	frame=Frame(time_win,relief=RAISED,height=150,width=550,borderwidth=1,bg='light blue')
	frame.pack(fill=BOTH,expand=1)
	
	dt_text=Label(frame,text='Date:',padx=10,pady=10)
	dt_text.pack(side=LEFT)
	
	global date
	date=Entry(frame,bd=5)
	date.pack(side=LEFT)
	
	
	st_text=Label(frame,text='Start Time:',padx=10,pady=10)
	st_text.pack(side=LEFT)
	
	global start_time
	start_time=Entry(frame,bd=5)
	start_time.pack(side=LEFT)
	
	et_text=Label(frame,text='End Time : ',padx=10,pady=10)
	et_text.pack(side=LEFT)
	
	global end_time
	end_time=Entry(frame,bd=5)
	end_time.pack(side=LEFT)

	submitB= Button(frame,text ='Submit', command = submit_timeIP,fg='white',bg='black',padx=10)
	submitB.pack(side=LEFT)



## display GUI to input time slot for user activity

def chooseTime():
	global ip_win
	ip_win=Tk()
	ip_win.title("Time Slot")
	frame=Frame(ip_win,relief=RAISED,height=150,width=550,borderwidth=1,bg='light blue')
	frame.pack(fill=BOTH,expand=1)
	
	dt_text=Label(frame,text='Date:',padx=10,pady=10)
	dt_text.pack(side=LEFT)
	
	global date
	date=Entry(frame,bd=5)
	date.pack(side=LEFT)
	
	st_text=Label(frame,text='Start Time:',padx=10,pady=10)
	st_text.pack(side=LEFT)
	
	global start_time
	start_time=Entry(frame,bd=5)
	start_time.pack(side=LEFT)
	
	et_text=Label(frame,text='End Time : ',padx=10,pady=10)
	et_text.pack(side=LEFT)
	
	global end_time
	end_time=Entry(frame,bd=5)
	end_time.pack(side=LEFT)
	"""
	global statusL
	statusL=Label(ip_win,text='STATUS: Nothing Submitted',fg='red',relief=RAISED,padx=10)
	statusL.pack(side=LEFT)
	"""
	submitB= Button(frame,text ='Submit', command = submit_time,fg='white',bg='black',padx=10)
	submitB.pack(side=LEFT)
	
#main windown GUI----------------
def init_GUI():

	win = Tk()
	win.title('FileZilla Log Analyzer')
	frame =Frame(win,relief=RAISED,width=1300, height=576, bg="gray")
	frame.pack(fill=BOTH,expand=1)
	frame.pack_propagate(0)
	b1=Button(frame,text='     Display Log     ',command = display,fg='black',bg='white',width=18)
	b2=Button(frame,text='     User-Location ',command = uloc,fg='black',bg='white',width=18)
	b3=Button(frame,text='Choose Time Slot',command = chooseTime,fg='black',bg='white',width=18)
	b4=Button(frame,text='Show same IP users',command = chooseTimeIP,fg='black',bg='white',width=18)
	b5=Button(frame,text='Report Cheating Cases',command = casestime,fg='black',bg='white',width=18)
	b6=Button(frame,text='           Quit            ',command = lambda : sys.exit(1),fg='black',bg='white',width=18)
	b7=Button(frame,text='Add White List',command = add_wlist,fg='black',bg='white',width=18)
	b1.place(in_=frame,relx=0.01,rely=0.1)
	b2.place(in_=frame,relx=0.01,rely=0.2)
	b3.place(in_=frame,relx=0.01,rely=0.3)
	b4.place(in_=frame,relx=0.01,rely=0.4)
	b5.place(in_=frame,relx=0.01,rely=0.5)
	b7.place(in_=frame,relx=0.01,rely=0.6)
	b6.place(in_=frame,relx=0.01,rely=0.7)
		
	selectB= Button(win,text ='Choose Log Files', command = ChooseFile,fg='white',bg='black')
	selectB.pack(side= RIGHT,padx=2,pady=5)
	
	addipB= Button(win,text ='Add IP location',command = addClass,fg='white',bg='black',relief=RAISED)
	addipB.pack(side=RIGHT,padx=2,pady=5)
		
	sbar=Scrollbar(frame)
	sbar.pack(side=RIGHT,fill=Y)
	
	global text	
	text= Label(win,text='No log file selected',fg='red',relief=RAISED)		
	text.pack(side=LEFT)
	
	font= tkFont.Font(family="Helvetica",size=10,weight="bold")
	global info
	
	info=Listbox(frame,yscrollcommand=sbar.set,height=20,width=155,relief=RAISED,borderwidth=5,font=font)
	info.pack(side=RIGHT,fill=Y)
	sbar.config(command=info.yview)
	
	photo = PhotoImage(file="logo2.gif")
	label = Label(frame,image=photo)
	label.image = photo 
	label.place(in_=frame,relx=0.005,rely=0.8)


	
	init_dict()
	init_wlist()
	win.mainloop()

def sort_by_date(log):
	return log[0]+log[1]


	
def sort_by_time(log):
	return log[0]+log[1]


def uloc():

	user_ip= re.findall(r'(\w+)\s\((\d+.\d+.\d+.\d+)\)', buffer)
	user_ip=list(set(user_ip))
	user_ip=sorted(user_ip)
	global info
	info.delete(0,info.size())
	for x in user_ip:
		result=re.search(r'(\d+).(\d+).(\d+).(\d+).',x[1])
		val =result.group(3)
		if val in ip_class and x[0] not in white_list:
			info.insert(END,'User : '+ x[0] + '              Location : ' + ip_class[ val ])
		elif x[0] not in white_list:
			info.insert(END,'User : '+ x[0] + '               Location : Unknown with IP: '+x[1] )
			

		
	

def main():

	init_GUI()

if __name__ == '__main__':
  main()




