import numpy as np
import math
from FixedPoint import FXfamily, FXnum

## Core neuron model
def Core_neuron_model_(active_Core_list):
	print("********** ISA for Core neuron model START **********")
	neuron_model = []

	type_ = input("Manual | Auto\n")

	if type_ == "Manual":
		print("*****************\n* 0 : SRM model *\n* 1 : LIF model *\n*****************")
		for core in active_Core_list:
			model = int(input("Neuron model in core %d " %core))
			neuron_model.append([core,model])

	elif type_ == "Auto":
		print("*****************\n* 0 : SRM model *\n* 1 : LIF model *\n*****************")
		model = int(input("Neuron model in cores "))
		for core in active_Core_list:
			neuron_model.append([core,model])

	else:
		print("Wrong command")

	print("********** ISA for Core neuron model END **********\n")
	return neuron_model

## Core neuron threshold
def Core_neuron_threshold_(active_Core_list, thresh, normalize): # [Q10.6]
	print("********** ISA for Core neuron threshold START **********")
	neuron_threshold = []

	type_ = input("Manual | Auto\n")

	if type_ == "Manual":
		for core in active_Core_list:
			thresh = float(input("Threshold in core %d with normarlize parameter %.2f " %(core, normalize)))
			thresh_norm = np.ceil(thresh / normalize)
			neuron_threshold.append([core,FXnum(thresh_norm,FXfamily(6,11)).scaledval])
	elif type_ == "Auto":
		thresh_norm = np.ceil(thresh / normalize)
		for core in active_Core_list:
			neuron_threshold.append([core,FXnum(thresh_norm,FXfamily(6,11)).scaledval])
	else:
		print("Wrong command")

	print("********** ISA for Core neuron threshold END **********\n")
	return neuron_threshold

## Core neuron constant
def Core_neuron_constant_(active_Core_list, tm, ts, normalize): # [Q5.6]
	print("********** ISA for Core neuron constant START **********")
	neuron_constant = []

	type_ = input("Manual | Auto\n")

	if type_ == "Manual":
		for core in active_Core_list:
			tm_ = float(input("Membrane time constant in core %d " %core))
			ts_ = float(input("Synaptic time constant in core %d " %core))
			constant_norm = tm_/((tm_-ts_)*normalize)
			neuron_constant.append([core,FXnum(constant_norm,FXfamily(6,6)).scaledval])
	elif type_ == "Auto":
		constant_norm = tm/((tm-ts)*normalize)
		for core in active_Core_list:
			neuron_constant.append([core,FXnum(constant_norm,FXfamily(6,6)).scaledval])
	else:
		print("Wrong command")

	print("********** ISA for Core neuron constant END **********\n")
	return neuron_constant


def TEMP_VAL(t_elap_in, dt, tau):
	# TEMP_LUT [Q16]
	addr_t = t_elap_in
	if(addr_t==0):	temp_val = 65535
	else:			temp_val = FXnum(math.exp(-dt*addr_t/tau),FXfamily(16,1)).scaledval

	return temp_val

def SCAL_VAL(t_elap_in, tau, b, l):
	# SCAL_LUT [Q16]
	addr_s = t_elap_in
	if(addr_s==0):	scal_val = 65535
	else:			scal_val = FXnum(math.exp(-b*t_elap_in/(l*tau)),FXfamily(16,1)).scaledval

	return scal_val

def Core_TS_EFA_(active_Core_list, dt, tm, ts, l, b):
	print("********** ISA for Core neuron TS-EFA generation START **********")
	ts_efa_lut = []

	type_ = input("Manual | Auto\n")

	if type_ == "Manual":
		for core in active_Core_list:
			tm_ = float(input("Membrane time constant in core %d " %core))
			ts_ = float(input("Synaptic time constant in core %d " %core))

			for ram_sel in range(4):
				for lut_addr in range(l):
					if(ram_sel==0):
						w_d_in = SCAL_VAL(lut_addr,tm_,b,l)
					elif(ram_sel==1):
						w_d_in = TEMP_VAL(lut_addr,dt,tm_)
					elif(ram_sel==2):
						w_d_in = SCAL_VAL(lut_addr,ts_,b,l)
					elif(ram_sel==3):
						w_d_in = TEMP_VAL(lut_addr,dt,ts_)
					ts_efa_lut.append([core,ram_sel,lut_addr,w_d_in])
	elif type_ == "Auto":
		for core in active_Core_list:		
			for ram_sel in range(4):
				for lut_addr in range(l):
					if(ram_sel==0):
						w_d_in = SCAL_VAL(lut_addr,tm,b,l)
					elif(ram_sel==1):
						w_d_in = TEMP_VAL(lut_addr,dt,tm)
					elif(ram_sel==2):
						w_d_in = SCAL_VAL(lut_addr,ts,b,l)
					elif(ram_sel==3):
						w_d_in = TEMP_VAL(lut_addr,dt,ts)
					ts_efa_lut.append([core,ram_sel,lut_addr,w_d_in])
	else:
		print("Wrong command")

	print("********** ISA for Core neuron TS-EFA generation END **********\n")
	return ts_efa_lut


