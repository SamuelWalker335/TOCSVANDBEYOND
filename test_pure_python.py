# Python program to create 
# a file explorer in Tkinter

# import all components
# from the tkinter library
from tkinter import *

# import filedialog module
from tkinter import filedialog

import pdfplumber
import pandas as pd

filename = "test "
# Function for opening the 
# file explorer window
def browseFiles():
	global filename 
	filename = filedialog.askopenfilename(initialdir = "/",
										title = "Select a File",
										filetypes = (("pdf files",
														"*.pdf*"),
													("all files",
														"*.*")))
	
	# Change label contents
	label_file_explorer.configure(text="File Opened: " + filename)

def remove_until_slash(input_string):
    # Find the last occurrence of '/'
    slash_index = input_string.rfind('/')
    # Return the substring after the last '/'
    return input_string[:slash_index + 1] if slash_index != -1 else input_string

def convertToCSV():
	outputName = remove_until_slash(filename) + inputtxt.get(1.0, "end-1c") + ".csv"
	print(outputName)
	filePath = filename 
	pdf = pdfplumber.open(filePath)
	#find columns for table
	page0 = pdf.pages[0]
	table = page0.extract_table()
	df = pd.DataFrame(columns = table[0])
	#loop through pages and add the tables together into one dataframe
	for i in range(len(pdf.pages)):
		page = pdf.pages[i]
		tables = page.extract_tables()
		
		for j in range(len(tables)):
			if( len(tables[j][0]) == len(df.columns)):
				# storing as dataframe from every table from 0 index including header!!!
				each_page_data = pd.DataFrame(tables[j][0:], columns=df.columns) 
				# Adding each df to main df by using concat (Eg :sum of numbers in array)
				df = pd.concat([df, each_page_data], ignore_index=True)
	
	df.to_csv(outputName)
	
	




																								
# Create the root window
window = Tk()

# Set window title
window.title('Pdf Converter')



#Set window background color
window.config(background = "white")

# Create a File Explorer label
label_file_explorer = Label(window, 
							text = "convert pdf files to csv",
							width = 50, height = 4, 
							fg = "blue")

inputtxt = Text(window,
                height = 1, 
                width = 20) 
	
button_explore = Button(window, 
						text = "Browse Files",
						command = browseFiles) 

button_convert = Button(window, 
						text = "convert",
						command = convertToCSV) 


# Grid method is chosen for placing
# the widgets at respective positions 
# in a table like structure by
# specifying rows and columns
label_file_explorer.pack()

inputtxt.pack()

button_explore.pack()

button_convert.pack()

# Let the window wait for any events
window.mainloop()


