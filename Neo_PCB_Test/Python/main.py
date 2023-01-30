import sys
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
import argparse
import serial

from util_and_function import load_data
from util_and_function import make_model
from util_and_function import make_evaluation_model
from util_and_function import load_pretrained

from Interface import instruction_data_format as ISA
from Interface.Network_on_Chip import *
from Interface.Core_Neuron import *
from Interface.Core_LaCERA import *
from Interface.Core_Synapse import *
from Interface.Core_Output_manager import *

############################## Hardware ##############################
## UART
ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM4'
ser.timeout = 0.1

def uart_write(list):
	for i in list:
		for chunk in range(20):
			ser.write((int(i[8*chunk:8*(chunk+1)],2)).to_bytes(1,byteorder="little"))

def uart_write_test(list):
	for i in list:
		for chunk in range(20):
			data_chunk = i[8*chunk:8*(chunk+1)]


## GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
######################################################################

#################################################### Arguments ####################################################
parser = argparse.ArgumentParser(description="Neo.v1 test - Dataset : MNIST, DVS, NMNIST - Network : cNet, LeNet")

parser.add_argument("--Type", type=str, default="PC", help="PC : simulation, Neo : emulation") # Execution type
parser.add_argument("--Active_cores", type=list, default=[2,3,4,5,6,7,8], help="List of activated cores") # Active cores

parser.add_argument("--Dataset", type=str, default="NMNIST", help="MNIST, DVS, NMNIST") # Dataset
parser.add_argument("--Network", type=str, default="cNet", help="cNet, LeNet") # Network architecture
parser.add_argument("--Pretrained", type=bool, default=True, help="Load pretrained model") # Load pretrained model

args = parser.parse_args()

print(args)
###################################################################################################################

########################################################################### Hyper-parameter ###########################################################################
batch_size = 100
thresh_ = dict([['cNet_MNIST',0.1],['cNet_DVS',0.15],['cNet_NMNIST',0.1],['LeNet_MNIST',0.15],['LeNet_DVS',0.15],['LeNet_NMNIST',0.15]])
delta_t_ = dict([['cNet_MNIST',2**(-12)],['cNet_DVS',2**(-10)],['cNet_NMNIST',2**(-10)],['LeNet_MNIST',2**(-12)],['LeNet_DVS',2**(-10)],['LeNet_NMNIST',2**(-10)]]) # s
tau1_ = dict([['cNet_MNIST',40e-3],['cNet_DVS',50e-3],['cNet_NMNIST',50e-3],['LeNet_MNIST',50e-3],['LeNet_DVS',50e-3],['LeNet_NMNIST',50e-3]]) # s
tau2_ = dict([['cNet_MNIST',10e-3],['cNet_DVS',10e-3],['cNet_NMNIST',10e-3],['LeNet_MNIST',10e-3],['LeNet_DVS',10e-3],['LeNet_NMNIST',10e-3]]) # s
num_classes_ =  dict([['MNIST',10],['DVS',11],['NMNIST',10]])
T_ = dict([['cNet_MNIST',512],['cNet_DVS',1500],['cNet_NMNIST',300],['LeNet_MNIST',512],['LeNet_DVS',1500],['LeNet_NMNIST',300]])
max_firing_rate = 200 # Hz

Neo_Normolize = 0.05
TS_EFA_L = 2**8
TS_EFA_B = 2**4
#######################################################################################################################################################################

pad = nn.ZeroPad2d(2)

def main():
	thresh, delta_t, tau1, tau2, num_classes, T = thresh_[args.Network+'_'+args.Dataset], delta_t_[args.Network+'_'+args.Dataset], tau1_[args.Network+'_'+args.Dataset], tau2_[args.Network+'_'+args.Dataset], num_classes_[args.Dataset], T_[args.Network+'_'+args.Dataset]

	if args.Type == "PC":
		_, test_loader = load_data(args.Dataset, batch_size)

		const = tau1 / (tau1 - tau2)
		decay1 = np.exp(-delta_t / tau1) 
		decay2 = np.exp(-delta_t / tau2)

		model = make_model(args.Network+'_'+args.Dataset, T, delta_t, max_firing_rate, batch_size, device, decay1, decay2, const, thresh).to(device)
		print(model)

		if args.Pretrained:
			path = load_pretrained(args.Network+'_'+args.Dataset)
			print(path)
			checkpoint = torch.load(path)
			model.load_state_dict(checkpoint['net'])

		model.eval()
		total, correct = 0, 0

		if (args.Dataset == 'MNIST') or (args.Dataset == 'NMNIST'):
			with torch.no_grad():
				for batch_idx, (inputs, targets) in enumerate(test_loader):
					if args.Network+'_'+args.Dataset == 'LeNet_MNIST':
						inputs = pad(inputs).to(device)
					else:
						inputs = inputs.to(device)
					outputs = model(inputs)
					_, predicted = outputs.cpu().max(1)

					total += float(targets.size(0))
					correct += float(predicted.eq(targets).sum().item())

					if batch_idx % 10 == 0:
						acc = 100. * float(correct) / float(total)
						print(batch_idx, len(test_loader), 'Simulation Accuracy : %.5f' %acc)

				print('Test Accuracy : %.5f' %(100. * float(correct) / float(total)))

		elif args.Dataset == 'DVS':
			with torch.no_grad():
				for batch_idx, (inputs, targets) in enumerate(test_loader):
					inputs = inputs.to(device)
					outputs = model(inputs)
					_, predicted = outputs.cpu().max(1)

					labels_ = torch.reshape(torch.chunk(targets, T, dim=1)[0],(batch_size,11))
					_, labels_idx = labels_.max(1)

					total += float(labels_.size(0))
					correct += float(predicted.eq(labels_idx).sum().item())

					if batch_idx % 10 == 0:
						acc = 100. * float(correct) / float(total)
						print(batch_idx, len(test_loader), 'Simulation Accuracy : %.5f' %acc)

				print('Test Accuracy : %.5f' %(100. * float(correct) / float(total)))

		else:
			print('Wrong command Dataset')

	elif args.Type == "Neo":
		print("###################### %s_%s LUT for Network on Chip START ######################" %(args.Network, args.Dataset))
		NoC_pointer_LUT = NoC_Pointer_(args.Network, args.Dataset, 3)
		NoC_destination_LUT = NoC_Destination_(args.Network, args.Dataset, 3)
		print("###################### %s_%s LUT for Network on Chip END ######################\n" %(args.Network, args.Dataset))

		print("###################### %s_%s LUT for Core Neuron Block START ######################" %(args.Network, args.Dataset))
		Core_neuron_model = Core_neuron_model_(args.Active_cores)
		Core_neuron_threshold = Core_neuron_threshold_(args.Active_cores, thresh, Neo_Normolize)
		Core_neuron_constant = Core_neuron_constant_(args.Active_cores, tau1, tau2, Neo_Normolize)
		Core_TS_EFA_LUT = Core_TS_EFA_(args.Active_cores, delta_t, tau1, tau2, TS_EFA_L, TS_EFA_B)
		print("###################### %s_%s LUT for Core Neuron Block END ######################\n" %(args.Network, args.Dataset))

		print("###################### %s_%s LUT for Core LaCERA Block START ######################" %(args.Network, args.Dataset))
		Core_LaCERA_Group_LUT = Core_LaCERA_Group_(args.Network, args.Dataset, args.Active_cores)
		Core_LaCERA_Layer_LUT = Core_LaCERA_Layer_(args.Network, args.Dataset, args.Active_cores)
		Core_LaCERA_Coneective_LUT = Core_LaCERA_Coneective_(args.Network, args.Dataset, args.Active_cores)
		print("###################### %s_%s LUT for Core LaCERA Block END ######################\n" %(args.Network, args.Dataset))

		if args.Pretrained:
			print("###################### %s_%s LUT for Core Synapse Block START ######################" %(args.Network, args.Dataset))
			path = load_pretrained(args.Network+'_'+args.Dataset)
			print(path)
			checkpoint = torch.load(path)
			Core_Synapse_LUT = Core_Synapse_(checkpoint)
			print("###################### %s_%s LUT for Core Synapse Block END ######################\n" %(args.Network, args.Dataset))

		else:
			print("You must prepare pretrained weigths first to use Neo!")

		print("###################### %s_%s LUT for Output management core START ######################" %(args.Network, args.Dataset))
		Output_manager_Pointer_LUT = Output_manager_Pointer_(args.Network, args.Dataset, 1)
		Output_manager_Destination_LUT = Output_manager_Destination_(args.Network, args.Dataset, 1)
		print("###################### %s_%s LUT for Output management core END ######################\n" %(args.Network, args.Dataset))


		print("###################### Instruction Packetize START ######################")
		Neo_ISA = ISA.instruction_encoder()
		print(Neo_ISA)

		Neo_ISA.active_core()
		print("Neo rx boundary offset North")
		Neo_ISA.rx_boundary_offset()
		print("Neo rx boundary offset East")
		Neo_ISA.rx_boundary_offset()
		print("Neo rx boundary offset West")
		Neo_ISA.rx_boundary_offset()
		Neo_ISA.NoC_pointer_write(NoC_pointer_LUT)
		Neo_ISA.NoC_destination_write(NoC_destination_LUT)
		Neo_ISA.track_membrane_potential()
		Neo_ISA.neuron_model_select(Core_neuron_model)
		Neo_ISA.threshold_write(Core_neuron_threshold)
		Neo_ISA.constant_write(Core_neuron_constant)
		Neo_ISA.TS_EFA_write(Core_TS_EFA_LUT)
		Neo_ISA.group_lut_write(Core_LaCERA_Group_LUT)
		Neo_ISA.layer_lut_write(Core_LaCERA_Layer_LUT)	
		Neo_ISA.connective_lut_write(Core_LaCERA_Coneective_LUT)
		Neo_ISA.synaptic_weight_write(Core_Synapse_LUT)
		Neo_ISA.output_manager_pointer_write(Output_manager_Pointer_LUT)
		Neo_ISA.output_manager_destination_write(Output_manager_Destination_LUT)
		print("###################### Instruction Packetize END ######################\n")


		print("###################### Configure %s_%s in Neo START ######################" %(args.Network, args.Dataset))
		# ser.open()
		# ISA_packet = Neo_ISA.instruction_packet_out()
		# uart_write(ISA_packet)
		ISA_packet = Neo_ISA.instruction_packet_out()
		uart_write_test(ISA_packet)
		print("###################### Configure %s_%s in Neo END ######################" %(args.Network, args.Dataset))		

		Neo_ISA.flush()

		_, test_loader = load_data(args.Dataset, batch_size=1)

		const = tau1 / (tau1 - tau2)
		decay1 = np.exp(-delta_t / tau1) 
		decay2 = np.exp(-delta_t / tau2)

		model = make_evaluation_model(args.Network+'_'+args.Dataset, T, delta_t, max_firing_rate, device).to(device)
		print(model)

		print("###################### Execute Neo START ######################")
		total, correct = 0, 0
		# Neo_ISA.batch_done()
		# ISA_packet = Neo_ISA.instruction_packet_out()
		# uart_write(ISA_packet)
		Neo_ISA.batch_done()
		ISA_packet = Neo_ISA.instruction_packet_out()
		uart_write_test(ISA_packet)
		Neo_ISA.flush()

		if (args.Dataset == 'MNIST') or (args.Dataset == 'NMNIST'):
			with torch.no_grad():
				for batch_idx, (inputs, targets) in enumerate(test_loader):
					if args.Network+'_'+args.Dataset == 'LeNet_MNIST':
						inputs = pad(inputs).to(device)
					else:
						inputs = inputs.to(device)
					outputs = model(inputs, Neo_ISA, num_classes, ser, uart_write_test)
					_, predicted = outputs.cpu().max(1)

					total += float(targets.size(0))
					correct += float(predicted.eq(targets).sum().item())

					if batch_idx % 10 == 0:
						acc = 100. * float(correct) / float(total)
						print(batch_idx, len(test_loader), 'Simulation Accuracy : %.5f' %acc)

				print('Neo Test Accuracy : %.5f' %(100. * float(correct) / float(total)))
				# ser.close()

		elif args.Dataset == 'DVS':
			with torch.no_grad():
				for batch_idx, (inputs, targets) in enumerate(test_loader):
					inputs = inputs.to(device)
					outputs = model(inputs, Neo_ISA, num_classes, ser, uart_write_test)
					_, predicted = outputs.cpu().max(1)

					labels_ = torch.reshape(torch.chunk(targets, T, dim=1)[0],(1,num_classes))
					_, labels_idx = labels_.max(1)

					total += float(labels_.size(0))
					correct += float(predicted.eq(labels_idx).sum().item())

					if batch_idx % 10 == 0:
						acc = 100. * float(correct) / float(total)
						print(batch_idx, len(test_loader), 'Simulation Accuracy : %.5f' %acc)
				# ser.close()
		print("###################### Execute Neo END ######################")

	else:
		print("Wrong command")


main()
