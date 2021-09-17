import pickle

barcode_tp_pkl = "barcode_toolpath.pkl"

barcode = '0003'
toolpath_lr = [6, 7]

barcode_toolpath = {barcode: toolpath_lr}

with open(barcode_tp_pkl, "ab") as pkl_file:
    pickle.dump(barcode_toolpath, pkl_file)

with open(barcode_tp_pkl, "rb") as pkl_file:
    bc_file = (pickle.load(pkl_file))