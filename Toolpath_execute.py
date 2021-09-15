from evasdk import Eva
import json
import pickle

print("\n\n---------- Barcode - Toolpath Execution ----------\n")

host_ip = '172.16.16.2'
token = 'a12eb9247519db8f010fad19104b8d901fd2dc00'

a_file = open("barcode_toolpath.pkl", "rb")
barcode_toolpath = pickle.load(a_file)
#print(barcode_toolpath)
a_file.close()

eva = Eva(host_ip, token)

i=0

while i<1 :

    barcode = input("\nScan Barcode... (q to quit):")

    if barcode == "q":
        break

    if barcode in barcode_toolpath:
        toolpath_id = barcode_toolpath.get(barcode)

        with eva.lock():
            eva.control_wait_for_ready()
            eva.toolpaths_use_saved(int(toolpath_id))  # EM: Changed
            eva.control_home()
            eva.control_run(loop=0, mode='automatic')  # EM: Changed
    else:
        print("Barcode Unregistered!")










