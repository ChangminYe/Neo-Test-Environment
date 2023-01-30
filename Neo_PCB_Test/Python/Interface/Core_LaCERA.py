import pandas as pd

## Core LaCERA Group LUT
def Core_LaCERA_Group_(network, dataset, active_Core_list):
	print("********** ISA for Core LaCERA Group LUT generate START **********")
	LUT = []
	idx = 0
	model_name = "./Interface/" + network + "_" + dataset + "_Core_LaCERA.xlsx"
	for Cores in range(len(active_Core_list)):
		target_Core_group = pd.DataFrame(pd.read_excel(model_name, sheet_name=Cores))[['group id',
																					 'source layer id',
																					 'group width index',
																					 'group height index',
																					 'group channel index']].dropna(axis=0)
		for groups in range(len(target_Core_group)):
			LUT.append([])
			LUT[idx].append(active_Core_list[Cores]) # Core index
			LUT[idx].append(target_Core_group['group id'][groups]) # LUT address
			LUT[idx].append(target_Core_group['source layer id'][groups]) # Layer index
			LUT[idx].append(target_Core_group['group width index'][groups]) # Group W index
			LUT[idx].append(target_Core_group['group height index'][groups]) # Group H index
			LUT[idx].append(target_Core_group['group channel index'][groups]) # Group C index
			idx += 1
	print("********** ISA for Core LaCERA Group LUT generate END **********\n")
	return LUT

## Core LaCERA Layer LUT
def Core_LaCERA_Layer_(network, dataset, active_Core_list):
	print("********** ISA for Core LaCERA Layer LUT generate START **********")
	LUT = []
	idx = 0
	model_name = "./Interface/" + network + "_" + dataset + "_Core_LaCERA.xlsx"
	for Cores in range(len(active_Core_list)):
		target_Core_layer = pd.DataFrame(pd.read_excel(model_name, sheet_name=Cores))[['Layer id',
																					 'group offset',
																					 'neurons in the layer',
																					 'feature map width',
																					 'feature map height',
																					 'dimension',
																					 'connective offset',
																					 'connective count']].dropna(axis=0)
		for layers in range(len(target_Core_layer)):
			LUT.append([])
			LUT[idx].append(active_Core_list[Cores]) # Core index
			LUT[idx].append(target_Core_layer['Layer id'][layers]) # LUT address
			LUT[idx].append(target_Core_layer['group offset'][layers]) # Group offset
			LUT[idx].append(target_Core_layer['neurons in the layer'][layers]) # Number of neurons in sub-layer
			LUT[idx].append(target_Core_layer['feature map width'][layers]) # Layer W
			LUT[idx].append(target_Core_layer['feature map height'][layers]) # Layer H
			LUT[idx].append(target_Core_layer['dimension'][layers]) # Layer dim
			LUT[idx].append(target_Core_layer['connective offset'][layers]) # Connective pointer offeset
			LUT[idx].append(target_Core_layer['connective count'][layers]) # Connective pointer count
			idx += 1
	print("********** ISA for Core LaCERA Layer LUT generate END **********\n")
	return LUT

## Core LaCERA Connective LUT
def Core_LaCERA_Coneective_(network, dataset, active_Core_list):
	print("********** ISA for Core LaCERA Coneective LUT generate START **********")
	LUT = []
	idx = 0
	model_name = "./Interface/" + network + "_" + dataset + "_Core_LaCERA.xlsx"
	for Cores in range(len(active_Core_list)):
		target_Core_connective = pd.DataFrame(pd.read_excel(model_name, sheet_name=Cores))[['connective id',
																							 'slot offset',
																							 'post layer index',
																							 'pool',
																							 'skip',
																							 'channel dimension of kernel (m_c)',
																							 'kernel pad width',
																							 'kernel size width',
																							 'kernel stride width',
																							 'kernel stride width recip',
																							 'kernel pad height',
																							 'kernel size height',
																							 'kernel stride height',
																							 'kernel stride height recip',
																							 'channel offset of post-layer',
																							 'channel serach range of post-layer']].dropna(axis=0)
		for connectives in range(len(target_Core_connective)):
			LUT.append([])
			LUT[idx].append(active_Core_list[Cores]) # Core index
			LUT[idx].append(target_Core_connective['connective id'][connectives]) # Connective address
			LUT[idx].append(target_Core_connective['slot offset'][connectives]) # Slot offset
			LUT[idx].append(target_Core_connective['post layer index'][connectives]) # Post layer address
			LUT[idx].append(target_Core_connective['pool'][connectives]) # Pool
			LUT[idx].append(target_Core_connective['skip'][connectives]) # Skip
			LUT[idx].append(target_Core_connective['channel dimension of kernel (m_c)'][connectives]) # m_c
			LUT[idx].append(target_Core_connective['kernel pad width'][connectives]) # O_W
			LUT[idx].append(target_Core_connective['kernel size width'][connectives]) # K_W
			LUT[idx].append(target_Core_connective['kernel stride width'][connectives]) # 1/S_W
			LUT[idx].append(target_Core_connective['kernel stride width recip'][connectives]) # 1/S_W
			LUT[idx].append(target_Core_connective['kernel pad height'][connectives]) # O_H
			LUT[idx].append(target_Core_connective['kernel size height'][connectives]) # K_H
			LUT[idx].append(target_Core_connective['kernel stride height'][connectives]) # S_H
			LUT[idx].append(target_Core_connective['kernel stride height recip'][connectives]) # 1/S_H
			LUT[idx].append(target_Core_connective['channel offset of post-layer'][connectives]) # Channel offset of post-layer
			LUT[idx].append(target_Core_connective['channel serach range of post-layer'][connectives]) # Chaneel range
			idx += 1
	print("********** ISA for Core LaCERA Coneective LUT generate END **********\n")
	return LUT



