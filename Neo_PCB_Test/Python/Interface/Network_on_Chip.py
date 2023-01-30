import pandas as pd

## Network on Chip Pointer LUT 
def NoC_Pointer_(network, dataset, active_NoC_num):
	print("********** ISA for NoC Pointer LUT generate START **********")
	LUT = []
	idx = 0
	model_name = "./Interface/" + network + "_" + dataset + "_NoC.xlsx"
	for NoCs in range(active_NoC_num):
		target_NoC_pointer = pd.DataFrame(pd.read_excel(model_name, sheet_name=NoCs))[['NoC id pointer','Pointer start','Pointer end']].dropna(axis=0)
		for lut_adress in range(len(target_NoC_pointer['NoC id pointer'])):
			LUT.append([])
			LUT[idx].append(target_NoC_pointer['NoC id pointer'][lut_adress])
			LUT[idx].append(lut_adress)
			LUT[idx].append(target_NoC_pointer['Pointer start'][lut_adress])
			LUT[idx].append(target_NoC_pointer['Pointer end'][lut_adress])
			idx += 1
	print("********** ISA for NoC Pointer LUT generate END **********\n")
	return LUT

## Network on Chip Destination LUT 
def NoC_Destination_(network, dataset, active_NoC_num):
	print("********** ISA for NoC Destination LUT generate START **********")
	LUT = []
	idx = 0
	model_name = "./Interface/" + network + "_" + dataset + "_NoC.xlsx"
	for NoCs in range(active_NoC_num):
		target_NoC_destination = pd.DataFrame(pd.read_excel(model_name, sheet_name=NoCs))[['NoC id destination','destination lut address','destination core']].dropna(axis=0)
		for lut_adress in range(len(target_NoC_destination['NoC id destination'])):
			LUT.append([])
			LUT[idx].append(target_NoC_destination['NoC id destination'][lut_adress])
			LUT[idx].append(target_NoC_destination['destination lut address'][lut_adress])
			LUT[idx].append(target_NoC_destination['destination core'][lut_adress])
			idx += 1
	print("********** ISA for NoC Destination LUT generate END **********\n")
	return LUT

