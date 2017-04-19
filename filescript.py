import csv
import shutil
from pathlib import Path

with open('training_data.csv', newline='') as csvfile:
	count=0;
	csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in csvreader:
		csvstrings=(row[0].split(","));
		my_file = Path("images/"+csvstrings[0]+".jpg");
		if my_file.is_file():
			if csvstrings[1]=="WALMART":
				count+=1;
				shutil.copy2("images/"+csvstrings[0]+".jpg", "images/isWalMart/"+csvstrings[0]+".jpg")
			else :
				shutil.copy2("images/"+csvstrings[0]+".jpg", "images/notWalMart/"+csvstrings[0]+".jpg")

	print (count);
