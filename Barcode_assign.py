#!/usr/bin/env python3
from evasdk import Eva
import pickle

print("\n\n---------- Barcode - Toolpath Association ----------\n")

host_ip = '172.16.16.2'
token = 'a12eb9247519db8f010fad19104b8d901fd2dc00'

eva = Eva(host_ip, token)

i=0

barcode_toolpath = {}
barcode = ""
toolpath = ""
b = False

while i<1:

	barcode = ""
	toolpath = ""
	b = False

	while barcode == "":
		barcode=input("\nScan Barcode... (q to quit):")
		if barcode in barcode_toolpath:
			overide = input("Barcode already registered. Overide? (y/n)")
			if overide == "n":
				barcode = ""


		if barcode == "q":
			b = True
			break
			
	if b == True:
		break

	while toolpath == "":
		toolpath=input("Input Tootpath ID (l for list):")
		if toolpath == "l":

			print(eva.toolpaths_list())

			toolpath=input("Input Tootpath ID:")

	barcode_toolpath[barcode]=toolpath


print(barcode_toolpath)
a_file = open("barcode_toolpath.pkl", "ab")  # EM: Changed
pickle.dump(barcode_toolpath, a_file)
a_file.close()










