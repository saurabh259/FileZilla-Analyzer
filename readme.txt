
The package provides two instances of the Log Analyzer

	1) Named as log_analyzer-1
	
		<> "filezilla_analyzer.py" which can be 
		run on any system having python installed.
		<> other files necesary for the program to work
		<> to execute the analyzer through this instance all files 
		must be in the same folder.

	2) Named as log_analyzer-2
	
		<>The version has executable file for Windows and supports both 
		32-bit and 64-bit version of windows.
		<>The version has two folders, build and dist. Both of which are 
		necessary for execution of the program.
		<>The program can be executed by running the file 
		filezilla_analyzer.exe in the folder dist


The following is the functionality of the log_analyzer

	1) Choose log files <button>: You have to choose log files to begin the analyzer.
	
 	2) Add Ip Class <button>: The user can give each vlan id a User Defined location. 
	
	3) Add white list user <button>: The user can add some users as whitelist. Such users will 
	not be displayed in log functions.
 	
	4) Display log <button> : Displays the content of all logs as Date Time User IP
	
	5) User Location <button> : Displays users from all the log files selected 
	that logged into the system along with their IP Location (given by their vlan id)	
	
	6) Choose Time <button> : Initiates a GUI that seeks you date and a time slot between 
	which all non whitelisted users information ( "User" "IP" )
	
	7) Show same IP users <button>: Initiates a GUI that seeks you date and a time slot and 
	displays all users who logged into the system from the same IP
	
	8) Report Cheating Cases <button>: Initiates a GUI that seeks you date, a time slot, 
	IP location, and folder name. On pressing submit button the Analyzer displays all users
	along with their IP locations that submitted a file in the specified folder.

Main methods/features implementations of the Application :

	1) initGUI() - Initializes GUI main window with all the buttons and labels. Components/Widgets
	used in GUI are Buttons, Labels , Scroll Bar , PhotoImage , Font .
	'TKinter' Library is used for GUI.

	2) Choosing and Reading multiple log files through GUI : askopenfilenames method of 'tkFileDialog'
	 is used. All the log files data is buffered/stored into a global variable called 'buffer' 

	3) Adding IP Class : A dictionary is maintained with key=VLan_id and value=location of Vlan, 
	 whose contents are saved into a file named 'dixt.txt' and initialized everytime the program starts

	4) Adding White List Users : All white listed users are stored in a file 'wlist.txt' and initialized
	/retrived when program starts.

	5) Manipulating Log Data : 're'( Regular Expression) library of python is used to extract the data in required
	format.



Authors : Saurabh Joshi (saurabh259) , Abhijeet Baranwaal (abhijeet-anshu) , Rishi Ghosh

	 

		