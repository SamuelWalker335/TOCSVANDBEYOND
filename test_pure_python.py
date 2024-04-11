#A python program to convert tables from pdf files to csv format

from tkinter import *
from tkinter import filedialog
import pdfplumber
import pandas as pd
import subprocess

filename = "test "
# Function for opening the 
# open file explorer window
def browseFiles():
	global filename 
	filename = filedialog.askopenfilename(initialdir = "/",
										title = "Select a File",
										filetypes = (("pdf files",
														"*.pdf*"),
													("all files",
														"*.*")))
	
	# Change label contents
	if(filename != ""):
		label_file_explorer.configure(text=filename)
	else:
		label_file_explorer.configure(text="Select a file")


def remove_until_slash(input_string):
    # Find the last occurrence of '/'
    slash_index = input_string.rfind('/')
    # Return the substring before the last '/'
    return input_string[:slash_index + 1] if slash_index != -1 else input_string

#open table using pdf plumber
def convertToCSV():
	#get the location of og file, append the input text line and add the .csv
	outputName = remove_until_slash(filename) + inputtxt.get(1.0, "end-1c") + ".csv"
	filePath = filename 
	pdf = pdfplumber.open(filePath)
	
	

	#create a list of alll the different table sizes
	tableSizes = []
	#loop through all the pages
	for i in range(len(pdf.pages)):
		page = pdf.pages[i]
		tables = page.extract_tables()
		#loop through all the tables
		for j in range(len(tables)):
			#if the table size is not in the list, append to list
			if(len(tables[j][0]) not in tableSizes):
				tableSizes.append(len(tables[j][0]))

	#create a dataframe for each table column size
	dfs = []
	for i in range(len(tableSizes)):
		newColumns = [None] * tableSizes[i]
		dfNew = pd.DataFrame(columns = newColumns)
		dfs.append(dfNew)	
		

	#loop through pages
	for i in range(len(pdf.pages)):
		page = pdf.pages[i]
		tables = page.extract_tables()
		#loop through tables
		for j in range(len(tables)):
			#if the first dataframe has the right number of columns for current table
			if( len(tables[j][0]) == len(dfs[0].columns)):
				#store the table as a data frame
				each_page_data = pd.DataFrame(tables[j][0:], columns=dfs[0].columns) 
				#and append it to the first dataframe in the list
				dfs[0] = pd.concat([dfs[0], each_page_data], ignore_index=True)
			#else: as long as the table columns are greater than 0
			elif(len(tables[j][0]) > 0):
				#loop through all the data frames
				for o in range(len(dfs)):
					#check if the current dataframe has the right number of columns
					if(len(dfs[o].columns) == len(tables[j][0])):
						#create a dataframe from the new table
						each_page_data = pd.DataFrame(tables[j][0:], columns=dfs[o].columns)
						#and append it to the correct dataframe
						dfs[o] = pd.concat([dfs[o], each_page_data], ignore_index=True)
						#no need to continue searching the dataframes
						break 
	
	#run through the multiple data frames and write to csv
	with open(outputName,'w') as f:
		for df in dfs:
			df.to_csv(f, index = False, lineterminator = '\n')

	#change text to file converted and open the windows explorer on the converted file
	label_file_explorer.configure(text = "File Converted!")
	f = subprocess.Popen(r'explorer /select, ' "\"" + outputName.replace('/', '\\') + "\"")
	




																								
# Create the root window
window = Tk()

# Set window title
window.title('Pdf Converter')



#Set window background color
window.config(	background = "ivory3",
				padx= 10, pady = 10
			  )

# Create a File Explorer label
label_file_explorer = Label(window, 
							text = "Select a File",
							width = 50, height = 4,
							font= ("consola", 10),
							bg = "ivory2", fg = "black")

#opens the file explorer to select a file
button_explore = Button(window,
						text = "Browse Files",
						width= 10, height= 3,
						font= ("consola", 10),
						bg= "spring green", fg = "black",
						command = browseFiles)

#label for text box
label_output_name = Label(window,
						text= "Output Name: ",
						width= 10, height= 1,
						font= ("consola", 10),
						bg = "ivory2",fg= "black")

#text input box for the file output name
inputtxt = Text(window,
				width = 45, height = 1, 
            	font= ("consola", 10),
				) 
	

#button that calls convert to csv
button_convert = Button(window, 
						text = "Export",
						width= 10, height= 3,
						font= ("consola", 10),
						bg= "spring green", fg = "black",
						command = convertToCSV) 


# Grid method is chosen for placing
# the widgets at respective positions 
# in a table like structure by
# specifying rows and columns
label_file_explorer.grid(row = 0, column= 0, columnspan= 1)

button_explore.grid(row = 0, column= 1, columnspan= 1, sticky= W, padx=10)

label_output_name.grid(row = 2, column= 0, columnspan= 1, sticky= W,pady=10)

inputtxt.grid(row = 2, column= 0, columnspan= 1, sticky= E)

button_convert.grid(row = 4, column= 0, columnspan= 2)

# Let the window wait for any events
window.mainloop()


