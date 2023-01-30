import pandas as pd

## Output manager Pointer LUT
def Output_manager_Pointer_(network, dataset, active_Neo_num):
	print("********** ISA for Output manager Pointer LUT generate START **********")
	LUT = []
	idx = 0
	model_name = "./Interface/" + network + "_" + dataset + "_Output_manager.xlsx"
	for Neos in range(active_Neo_num):
		target_Neo_pointer = pd.DataFrame(pd.read_excel(model_name, sheet_name=Neos))[['sub layer (group) id', 'Pointer start', 'Pointer end']].dropna(axis=0)
		for lut_address in range(len(target_Neo_pointer['sub layer (group) id'])):
			LUT.append([])
			LUT[idx].append(target_Neo_pointer['sub layer (group) id'][lut_address])
			LUT[idx].append(target_Neo_pointer['Pointer start'][lut_address])
			LUT[idx].append(target_Neo_pointer['Pointer end'][lut_address])
			idx += 1
	print("********** ISA for Output manager Pointer LUT generate END **********\n")
	return LUT


def Output_manager_Destination_(network, dataset, active_Neo_num):
	print("********** ISA for Output manager Destination LUT generate START **********")
	LUT = []
	idx = 0
	model_name = "./Interface/" + network + "_" + dataset + "_Output_manager.xlsx"
	for Neos in range(active_Neo_num):
		target_Neo_destination = pd.DataFrame(pd.read_excel(model_name, sheet_name=Neos))[['destination lut address', 'Chip output port', 'destination core']].dropna(axis=0)
		for lut_address in range(len(target_Neo_destination['destination lut address'])):
			LUT.append([])
			LUT[idx].append(target_Neo_destination['destination lut address'][lut_address])
			if(target_Neo_destination['Chip output port'][lut_address]=='North'):
				LUT[idx].append(0)
			elif(target_Neo_destination['Chip output port'][lut_address]=='East'):
				LUT[idx].append(1)
			elif(target_Neo_destination['Chip output port'][lut_address]=='West'):
				LUT[idx].append(2)
			else:
				LUT[idx].append(0)
			LUT[idx].append(target_Neo_destination['destination core'][lut_address])
			idx += 1
	print("********** ISA for Output manager Destination LUT generate END **********\n")
	return LUT

