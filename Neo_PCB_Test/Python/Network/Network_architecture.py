import torch
import torch.nn as nn
from .Neuron import *

################################ GPU ################################
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#####################################################################

## cNet model for MNIST
class cNet_MNIST(nn.Module):
	def __init__(self, T=512, delta_t=2**(-10), max_firing_rate=200, batch_size=1, device=device, decay1=0, decay2=0, const=0, thresh=0):
		super(cNet_MNIST, self).__init__()
		self.conv1 = nn.Conv2d(1, 16, 4, stride=2, bias=False)
		self.conv2 = nn.Conv2d(16, 32, 3, bias=False)
		self.conv3 = nn.Conv2d(32, 64, 3, stride=2, bias=False)
		self.conv4 = nn.Conv2d(64, 10, 4, bias=False)
		self.fc1 = nn.Linear(40, 10, bias=False)
		self.T = T
		self.delta_t = delta_t
		self.max_firing_rate = max_firing_rate
		self.batch_size = batch_size
		self.device = device
		self.decay1 = decay1
		self.decay2 = decay2
		self.const = const
		self.thresh = thresh

	def forward(self, input):
		h1_mem1 = h1_mem2 = h1_spike = torch.reshape(torch.zeros(self.batch_size, 13*13*16, device=self.device), (self.batch_size,-1,13,13))
		h2_mem1 = h2_mem2 = h2_spike = torch.reshape(torch.zeros(self.batch_size, 11*11*32, device=self.device), (self.batch_size,-1,11,11))
		h3_mem1 = h3_mem2 = h3_spike = torch.reshape(torch.zeros(self.batch_size, 5*5*64, device=self.device), (self.batch_size,-1,5,5))
		h4_mem1 = h4_mem2 = h4_spike = torch.reshape(torch.zeros(self.batch_size, 2*2*10, device=self.device), (self.batch_size,-1,2,2))
		h5_sumspike = h5_mem1 = h5_mem2 = h5_spike = torch.reshape(torch.zeros(self.batch_size, 10, device=self.device), (self.batch_size,-1))

		for step in range(self.T): # simulation time steps

			x = input*self.max_firing_rate*self.delta_t > torch.rand(input.size(), device=self.device) # prob. firing

			h1_mem1, h1_mem2, h1_spike = mem_update(self.conv1, x.float(), h1_mem1, h1_mem2, h1_spike, self.decay1, self.decay2, self.const, self.thresh)
			h2_mem1, h2_mem2, h2_spike = mem_update(self.conv2, h1_spike, h2_mem1, h2_mem2, h2_spike, self.decay1, self.decay2, self.const, self.thresh)
			h3_mem1, h3_mem2, h3_spike = mem_update(self.conv3, h2_spike, h3_mem1, h3_mem2, h3_spike, self.decay1, self.decay2, self.const, self.thresh)
			h4_mem1, h4_mem2, h4_spike = mem_update(self.conv4, h3_spike, h4_mem1, h4_mem2, h4_spike, self.decay1, self.decay2, self.const, self.thresh)
			h5_mem1, h5_mem2, h5_spike = mem_update(self.fc1, torch.reshape(h4_spike,(self.batch_size,-1)), torch.reshape(h5_mem1,(self.batch_size,-1)), torch.reshape(h5_mem2,(self.batch_size,-1)), torch.reshape(h5_spike,(self.batch_size,-1)), self.decay1, self.decay2, self.const, self.thresh)
			h5_sumspike += h5_spike

		outputs = h5_sumspike / self.T

		return outputs

## cNet model for DVS
class cNet_DVS(nn.Module):
	def __init__(self, T=300, batch_size=1, device=device, decay1=0, decay2=0, const=0, thresh=0):
		super(cNet_DVS, self).__init__()
		self.conv1 = nn.Conv2d(2, 16, 4, stride=2, bias=False)
		self.conv2 = nn.Conv2d(16, 32, 3, bias=False)
		self.conv3 = nn.Conv2d(32, 64, 3, stride=2, bias=False)
		self.conv4 = nn.Conv2d(64, 10, 4, bias=False)
		self.fc1 = nn.Linear(90, 11, bias=False)
		self.T = T
		self.batch_size = batch_size
		self.device = device
		self.decay1 = decay1
		self.decay2 = decay2
		self.const = const
		self.thresh = thresh

	def forward(self, input):
		h1_mem1 = h1_mem2 = h1_spike = torch.reshape(torch.zeros(self.batch_size, 15*15*16, device=self.device), (self.batch_size,-1,15,15))
		h2_mem1 = h2_mem2 = h2_spike = torch.reshape(torch.zeros(self.batch_size, 13*13*32, device=self.device), (self.batch_size,-1,13,13))
		h3_mem1 = h3_mem2 = h3_spike = torch.reshape(torch.zeros(self.batch_size, 6*6*64, device=self.device), (self.batch_size,-1,6,6))
		h4_mem1 = h4_mem2 = h4_spike = torch.reshape(torch.zeros(self.batch_size, 3*3*10, device=self.device), (self.batch_size,-1,3,3))
		h5_sumspike = h5_mem1 = h5_mem2 = h5_spike = torch.reshape(torch.zeros(self.batch_size, 11, device=self.device), (self.batch_size,-1))
		
		time_step_input = input.permute(1,0,2,4,3)

		for step in range(self.T): # simulation time steps
			x = torch.clamp(time_step_input[step],0,1)
			h1_mem1, h1_mem2, h1_spike = mem_update(self.conv1, x.float(), h1_mem1, h1_mem2, h1_spike, self.decay1, self.decay2, self.const, self.thresh)
			h2_mem1, h2_mem2, h2_spike = mem_update(self.conv2, h1_spike, h2_mem1, h2_mem2, h2_spike, self.decay1, self.decay2, self.const, self.thresh)
			h3_mem1, h3_mem2, h3_spike = mem_update(self.conv3, h2_spike, h3_mem1, h3_mem2, h3_spike, self.decay1, self.decay2, self.const, self.thresh)
			h4_mem1, h4_mem2, h4_spike = mem_update(self.conv4, h3_spike, h4_mem1, h4_mem2, h4_spike, self.decay1, self.decay2, self.const, self.thresh)
			h5_mem1, h5_mem2, h5_spike = mem_update(self.fc1, torch.reshape(h4_spike,(self.batch_size,-1)), torch.reshape(h5_mem1,(self.batch_size,-1)), torch.reshape(h5_mem2,(self.batch_size,-1)), torch.reshape(h5_spike,(self.batch_size,-1)), self.decay1, self.decay2, self.const, self.thresh)
			h5_sumspike += h5_spike

		outputs = h5_sumspike / self.T

		return outputs

## cNet model for NMNIST
class cNet_NMNIST(nn.Module):
	def __init__(self, T=60, batch_size=1, device=device, decay1=0, decay2=0, const=0, thresh=0):
		super(cNet_NMNIST, self).__init__()
		self.conv1 = nn.Conv2d(2, 16, 4, stride=2, bias=False)
		self.conv2 = nn.Conv2d(16, 32, 3, bias=False)
		self.conv3 = nn.Conv2d(32, 64, 3, stride=2, bias=False)
		self.conv4 = nn.Conv2d(64, 10, 4, bias=False)
		self.fc1 = nn.Linear(90, 10, bias=False)
		self.T = T
		self.batch_size = batch_size
		self.device = device
		self.decay1 = decay1
		self.decay2 = decay2
		self.const = const
		self.thresh = thresh

	def forward(self, input):
		h1_mem1 = h1_mem2 = h1_spike = torch.reshape(torch.zeros(self.batch_size, 15*15*16, device=self.device), (self.batch_size,-1,15,15))
		h2_mem1 = h2_mem2 = h2_spike = torch.reshape(torch.zeros(self.batch_size, 13*13*32, device=self.device), (self.batch_size,-1,13,13))
		h3_mem1 = h3_mem2 = h3_spike = torch.reshape(torch.zeros(self.batch_size, 6*6*64, device=self.device), (self.batch_size,-1,6,6))
		h4_mem1 = h4_mem2 = h4_spike = torch.reshape(torch.zeros(self.batch_size, 3*3*10, device=self.device), (self.batch_size,-1,3,3))
		h5_sumspike = h5_mem1 = h5_mem2 = h5_spike = torch.reshape(torch.zeros(self.batch_size, 10, device=self.device), (self.batch_size,-1))

		time_step_input = input.permute(4,0,1,2,3)

		for step in range(self.T): # simulation time steps
			x = torch.clamp(time_step_input[step],0,1)
			
			h1_mem1, h1_mem2, h1_spike = mem_update(self.conv1, x.float(), h1_mem1, h1_mem2, h1_spike, self.decay1, self.decay2, self.const, self.thresh)
			h2_mem1, h2_mem2, h2_spike = mem_update(self.conv2, h1_spike, h2_mem1, h2_mem2, h2_spike, self.decay1, self.decay2, self.const, self.thresh)
			h3_mem1, h3_mem2, h3_spike = mem_update(self.conv3, h2_spike, h3_mem1, h3_mem2, h3_spike, self.decay1, self.decay2, self.const, self.thresh)
			h4_mem1, h4_mem2, h4_spike = mem_update(self.conv4, h3_spike, h4_mem1, h4_mem2, h4_spike, self.decay1, self.decay2, self.const, self.thresh)
			h5_mem1, h5_mem2, h5_spike = mem_update(self.fc1, torch.reshape(h4_spike,(self.batch_size,-1)), torch.reshape(h5_mem1,(self.batch_size,-1)), torch.reshape(h5_mem2,(self.batch_size,-1)), torch.reshape(h5_spike,(self.batch_size,-1)), self.decay1, self.decay2, self.const, self.thresh)
			h5_sumspike += h5_spike

		outputs = h5_sumspike / self.T
		return outputs

## LeNet model for MNIST
class LeNet_MNIST(nn.Module):
	def __init__(self, T=512, delta_t=2**(-10), max_firing_rate=200, batch_size=1, device=device, decay1=0, decay2=0, const=0, thresh=0):
		super(LeNet_MNIST, self).__init__()
		self.conv1 = nn.Conv2d(1, 6, 5, stride=1, bias=False)
		self.pool1 = nn.AvgPool2d(2,2)
		self.conv2 = nn.Conv2d(6, 16, 5, stride=1, bias=False)
		self.pool2 = nn.AvgPool2d(2,2)
		self.conv3 = nn.Conv2d(16, 120, 5, stride=1, bias=False)
		self.fc1 = nn.Linear(120, 84, bias=False)
		self.fc2 = nn.Linear(84, 10, bias=False)
		self.T = T
		self.delta_t = delta_t
		self.max_firing_rate = max_firing_rate
		self.batch_size = batch_size
		self.device = device
		self.decay1 = decay1
		self.decay2 = decay2
		self.const = const
		self.thresh = thresh

	def forward(self, input):
		h1_mem1 = h1_mem2 = h1_spike = torch.reshape(torch.zeros(self.batch_size, 28*28*6, device=self.device), (self.batch_size,-1,28,28))
		h2_mem1 = h2_mem2 = h2_spike = torch.reshape(torch.zeros(self.batch_size, 14*14*6, device=self.device), (self.batch_size,-1,14,14))
		h3_mem1 = h3_mem2 = h3_spike = torch.reshape(torch.zeros(self.batch_size, 10*10*16, device=self.device), (self.batch_size,-1,10,10))
		h4_mem1 = h4_mem2 = h4_spike = torch.reshape(torch.zeros(self.batch_size, 5*5*16, device=self.device), (self.batch_size,-1,5,5))
		h5_mem1 = h5_mem2 = h5_spike = torch.reshape(torch.zeros(self.batch_size, 120, device=self.device), (self.batch_size,-1,1,1))
		h6_mem1 = h6_mem2 = h6_spike = torch.reshape(torch.zeros(self.batch_size, 84, device=self.device), (self.batch_size,-1))
		h7_sumspike = h7_mem1 = h7_mem2 = h7_spike = torch.reshape(torch.zeros(self.batch_size, 10, device=self.device), (self.batch_size,-1))

		for step in range(self.T): # simulation time steps
			x = input*self.max_firing_rate*self.delta_t > torch.rand(input.size(), device=self.device) # prob. firing

			h1_mem1, h1_mem2, h1_spike = mem_update(self.conv1, x.float(), h1_mem1, h1_mem2, h1_spike, self.decay1, self.decay2, self.const, self.thresh)
			h2_mem1, h2_mem2, h2_spike = mem_update(self.pool1, h1_spike, h2_mem1, h2_mem2, h2_spike, self.decay1, self.decay2, self.const, self.thresh)
			h3_mem1, h3_mem2, h3_spike = mem_update(self.conv2, h2_spike, h3_mem1, h3_mem2, h3_spike, self.decay1, self.decay2, self.const, self.thresh)
			h4_mem1, h4_mem2, h4_spike = mem_update(self.pool2, h3_spike, h4_mem1, h4_mem2, h4_spike, self.decay1, self.decay2, self.const, self.thresh)
			h5_mem1, h5_mem2, h5_spike = mem_update(self.conv3, h4_spike, h5_mem1, h5_mem2, h5_spike, self.decay1, self.decay2, self.const, self.thresh)
			h6_mem1, h6_mem2, h6_spike = mem_update(self.fc1, torch.reshape(h5_spike,(self.batch_size,-1)), torch.reshape(h6_mem1,(self.batch_size,-1)), torch.reshape(h6_mem2,(self.batch_size,-1)), torch.reshape(h6_spike,(self.batch_size,-1)), self.decay1, self.decay2, self.const, self.thresh)
			h7_mem1, h7_mem2, h7_spike = mem_update(self.fc2, h6_spike, h7_mem1, h7_mem2, h7_spike, self.decay1, self.decay2, self.const, self.thresh)
			h7_sumspike += h7_spike

		outputs = h7_sumspike / self.T

		return outputs

## LeNet model for DVS
class LeNet_DVS(nn.Module):
	def __init__(self, T=300, batch_size=1, device=device, decay1=0, decay2=0, const=0, thresh=0):
		super(LeNet_DVS, self).__init__()
		self.conv1 = nn.Conv2d(2, 6, 5, stride=1, bias=False)
		self.pool1 = nn.AvgPool2d(2,2)
		self.conv2 = nn.Conv2d(6, 16, 5, stride=1, bias=False)
		self.pool2 = nn.AvgPool2d(2,2)
		self.conv3 = nn.Conv2d(16, 120, 5, stride=1, bias=False)
		self.fc1 = nn.Linear(120, 84, bias=False)
		self.fc2 = nn.Linear(84, 11, bias=False)
		self.T = T
		self.batch_size = batch_size
		self.device = device
		self.decay1 = decay1
		self.decay2 = decay2
		self.const = const
		self.thresh = thresh

	def forward(self, input):
		h1_mem1 = h1_mem2 = h1_spike = torch.reshape(torch.zeros(self.batch_size, 28*28*6, device=self.device), (self.batch_size,-1,28,28))
		h2_mem1 = h2_mem2 = h2_spike = torch.reshape(torch.zeros(self.batch_size, 14*14*6, device=self.device), (self.batch_size,-1,14,14))
		h3_mem1 = h3_mem2 = h3_spike = torch.reshape(torch.zeros(self.batch_size, 10*10*16, device=self.device), (self.batch_size,-1,10,10))
		h4_mem1 = h4_mem2 = h4_spike = torch.reshape(torch.zeros(self.batch_size, 5*5*16, device=self.device), (self.batch_size,-1,5,5))
		h5_mem1 = h5_mem2 = h5_spike = torch.reshape(torch.zeros(self.batch_size, 120, device=self.device), (self.batch_size,-1,1,1))
		h6_mem1 = h6_mem2 = h6_spike = torch.reshape(torch.zeros(self.batch_size, 84, device=self.device), (self.batch_size,-1))
		h7_sumspike = h7_mem1 = h7_mem2 = h7_spike = torch.reshape(torch.zeros(self.batch_size, 11, device=self.device), (self.batch_size,-1))

		time_step_input = input.permute(1,0,2,4,3)

		for step in range(self.T): # simulation time steps
			x = torch.clamp(time_step_input[step],0,1)
			h1_mem1, h1_mem2, h1_spike = mem_update(self.conv1, x.float(), h1_mem1, h1_mem2, h1_spike, self.decay1, self.decay2, self.const, self.thresh)
			h2_mem1, h2_mem2, h2_spike = mem_update(self.pool1, h1_spike, h2_mem1, h2_mem2, h2_spike, self.decay1, self.decay2, self.const, self.thresh)
			h3_mem1, h3_mem2, h3_spike = mem_update(self.conv2, h2_spike, h3_mem1, h3_mem2, h3_spike, self.decay1, self.decay2, self.const, self.thresh)
			h4_mem1, h4_mem2, h4_spike = mem_update(self.pool2, h3_spike, h4_mem1, h4_mem2, h4_spike, self.decay1, self.decay2, self.const, self.thresh)
			h5_mem1, h5_mem2, h5_spike = mem_update(self.conv3, h4_spike, h5_mem1, h5_mem2, h5_spike, self.decay1, self.decay2, self.const, self.thresh)
			h6_mem1, h6_mem2, h6_spike = mem_update(self.fc1, torch.reshape(h5_spike,(self.batch_size,-1)), torch.reshape(h6_mem1,(self.batch_size,-1)), torch.reshape(h6_mem2,(self.batch_size,-1)), torch.reshape(h6_spike,(self.batch_size,-1)), self.decay1, self.decay2, self.const, self.thresh)
			h7_mem1, h7_mem2, h7_spike = mem_update(self.fc2, h6_spike, h7_mem1, h7_mem2, h7_spike, self.decay1, self.decay2, self.const, self.thresh)
			h7_sumspike += h7_spike

		outputs = h7_sumspike / self.T

		return outputs

## LeNet model for NMNIST
class LeNet_NMNIST(nn.Module):
	def __init__(self, T=60, batch_size=1, device=device, decay1=0, decay2=0, const=0, thresh=0):
		super(LeNet_NMNIST, self).__init__()
		self.conv1 = nn.Conv2d(2, 6, 5, stride=1, bias=False)
		self.pool1 = nn.AvgPool2d(2,2)
		self.conv2 = nn.Conv2d(6, 16, 5, stride=1, bias=False)
		self.pool2 = nn.AvgPool2d(2,2)
		self.conv3 = nn.Conv2d(16, 120, 5, stride=1, bias=False)
		self.fc1 = nn.Linear(120, 84, bias=False)
		self.fc2 = nn.Linear(84, 10, bias=False)
		self.T = T
		self.batch_size = batch_size
		self.device = device
		self.decay1 = decay1
		self.decay2 = decay2
		self.const = const
		self.thresh = thresh

	def forward(self, input):
		h1_mem1 = h1_mem2 = h1_spike = torch.reshape(torch.zeros(self.batch_size, 28*28*6, device=self.device), (self.batch_size,-1,28,28))
		h2_mem1 = h2_mem2 = h2_spike = torch.reshape(torch.zeros(self.batch_size, 14*14*6, device=self.device), (self.batch_size,-1,14,14))
		h3_mem1 = h3_mem2 = h3_spike = torch.reshape(torch.zeros(self.batch_size, 10*10*16, device=self.device), (self.batch_size,-1,10,10))
		h4_mem1 = h4_mem2 = h4_spike = torch.reshape(torch.zeros(self.batch_size, 5*5*16, device=self.device), (self.batch_size,-1,5,5))
		h5_mem1 = h5_mem2 = h5_spike = torch.reshape(torch.zeros(self.batch_size, 120, device=self.device), (self.batch_size,-1,1,1))
		h6_mem1 = h6_mem2 = h6_spike = torch.reshape(torch.zeros(self.batch_size, 84, device=self.device), (self.batch_size,-1))
		h7_sumspike = h7_mem1 = h7_mem2 = h7_spike = torch.reshape(torch.zeros(self.batch_size, 10, device=self.device), (self.batch_size,-1))

		time_step_input = input.permute(4,0,1,2,3)

		for step in range(self.T): # simulation time steps
			x = torch.clamp(time_step_input[step],0,1)
			
			h1_mem1, h1_mem2, h1_spike = mem_update(self.conv1, x.float(), h1_mem1, h1_mem2, h1_spike, self.decay1, self.decay2, self.const, self.thresh)
			h2_mem1, h2_mem2, h2_spike = mem_update(self.pool1, h1_spike, h2_mem1, h2_mem2, h2_spike, self.decay1, self.decay2, self.const, self.thresh)
			h3_mem1, h3_mem2, h3_spike = mem_update(self.conv2, h2_spike, h3_mem1, h3_mem2, h3_spike, self.decay1, self.decay2, self.const, self.thresh)
			h4_mem1, h4_mem2, h4_spike = mem_update(self.pool2, h3_spike, h4_mem1, h4_mem2, h4_spike, self.decay1, self.decay2, self.const, self.thresh)
			h5_mem1, h5_mem2, h5_spike = mem_update(self.conv3, h4_spike, h5_mem1, h5_mem2, h5_spike, self.decay1, self.decay2, self.const, self.thresh)
			h6_mem1, h6_mem2, h6_spike = mem_update(self.fc1, torch.reshape(h5_spike,(self.batch_size,-1)), torch.reshape(h6_mem1,(self.batch_size,-1)), torch.reshape(h6_mem2,(self.batch_size,-1)), torch.reshape(h6_spike,(self.batch_size,-1)), self.decay1, self.decay2, self.const, self.thresh)
			h7_mem1, h7_mem2, h7_spike = mem_update(self.fc2, h6_spike, h7_mem1, h7_mem2, h7_spike, self.decay1, self.decay2, self.const, self.thresh)
			h7_sumspike += h7_spike

		outputs = h7_sumspike / self.T
		return outputs


## (Neo Evaluation) cNet model for MNIST 
class EVAL_cNet_MNIST(nn.Module):
	def __init__(self, T=512, delta_t=2**(-10), max_firing_rate=200, device=device):
		super(EVAL_cNet_MNIST, self).__init__()
		self.T = T
		self.delta_t = delta_t
		self.max_firing_rate = max_firing_rate
		self.device = device

	def forward(self, input, Neo_ISA, num_classes, ser, UART):
		o_layer_spike = torch.zeros(1, num_classes)

		for step in range(self.T): # Emulation time steps
			x = input*self.max_firing_rate*self.delta_t > torch.rand(input.size(), device=self.device) # prob. firing
			MNIST_input = torch.where(x)
			input_spikes = []

			for spikes in range(len(MNIST_input[0])):
				i_c_index = MNIST_input[1][spikes]
				i_h_index = MNIST_input[2][spikes]
				i_w_index = MNIST_input[3][spikes]
				c_grp_upd = i_c_index//4
				h_grp_upd = i_h_index//4
				w_grp_upd = i_w_index//4
				c_encode_index = i_c_index%4
				h_encode_index = i_h_index%4
				w_encode_index = i_w_index%4
				grp_update = 64*(w_grp_upd+(h_grp_upd*8)+(c_grp_upd*64))
				index_LaCERA_encode = w_encode_index+(h_encode_index*4)+(c_encode_index*16)
				input_index = grp_update+index_LaCERA_encode
				input_spikes.append([2,0,input_index])
				input_spikes.append([3,0,input_index])
			if(len(input_spikes)==0):
				input_spikes.append([2,1,0])	# dummy
				input_spikes.append([3,1,0])	# dummy

			Neo_ISA.input_event(input_spikes)
			Neo_ISA.time_step_exe_start()
			ISA_packet = Neo_ISA.instruction_packet_out()
			UART(ISA_packet)
			Neo_ISA.flush()

			# while True:
			# 	d_out = ser.read(3)
			# 	if(d_out != b''):
			# 		d_out = int.from_bytes(d_out, "little")

			# 		if(d_out==16777215):
			# 			break
			# 		elif(64*279<=d_out<=64*279+10-1):
			# 			o_layer_spike[0][d_out-64*279] += 1
			# 		elif(d_out>131071):
			# 			print(d_out, "error")

		Neo_ISA.batch_done()
		ISA_packet = Neo_ISA.instruction_packet_out()
		UART(ISA_packet)
		Neo_ISA.flush()

		output_Neo = o_layer_spike / self.T

		return output_Neo

## (Neo Evaluation) cNet model for DVS
class EVAL_cNet_DVS(nn.Module):
	def __init__(self, T=300):
		super(EVAL_cNet_DVS, self).__init__()
		self.T = T

	def forward(self, input, Neo_ISA, num_classes, ser, UART):
		o_layer_spike = torch.zeros(1, num_classes)

		time_step_input = input.permute(1,0,2,4,3)

		for step in range(self.T): # simulation time steps
			x = torch.clamp(time_step_input[step],0,1)
			DVS_input = torch.where(x)
			input_spikes = []

			for spikes in range(len(dvs_input[0])):
				i_c_index = dvs_input[1][spikes]
				i_h_index = dvs_input[2][spikes]
				i_w_index = dvs_input[3][spikes]
				c_grp_upd = i_c_index//4
				h_grp_upd = i_h_index//4
				w_grp_upd = i_w_index//4
				c_decode_index = i_c_index%4
				h_decode_index = i_h_index%4
				w_decode_index = i_w_index%4
				grp_update = 64*(w_grp_upd+(h_grp_upd*8)+(c_grp_upd*64))
				index_dec = w_decode_index+(h_decode_index*4)+(c_decode_index*16)
				input_index = grp_update+index_dec
				input_spikes.append([2,0,input_index])
				input_spikes.append([3,0,input_index])
			input_spikes.append([2,1,0])	# dummy
			input_spikes.append([3,1,0])	# dummy			

			Neo_ISA.input_event(input_spikes)
			Neo_ISA.time_step_exe_start()
			ISA_packet = Neo_ISA.instruction_packet_out()
			UART(ISA_packet)
			Neo_ISA.flush()

			# while True:
			# 	d_out = ser.read(3)
			# 	if(d_out != b''):
			# 		d_out = int.from_bytes(d_out, "little")

			# 		if(d_out==16777215):
			# 			break
			# 		elif(20672<=d_out<=20672+11-1):
			# 			o_layer_spike[0][d_out-20672] += 1
			# 		elif(d_out>131071):
			# 			print(d_out, "error")

		Neo_ISA.batch_done()
		ISA_packet = Neo_ISA.instruction_packet_out()
		UART(ISA_packet)
		Neo_ISA.flush()

		output_Neo = o_layer_spike / self.T

		return output_Neo

## (Neo Evaluation) cNet model for NMNIST
class EVAL_cNet_NMNIST(nn.Module):
	def __init__(self, T=60):
		super(EVAL_cNet_NMNIST, self).__init__()
		self.T = T

	def forward(self, input, Neo_ISA, num_classes, ser, UART):
		o_layer_spike = torch.zeros(1, num_classes)

		time_step_input = input.permute(4,0,1,2,3)

		for step in range(self.T): # simulation time steps
			x = torch.clamp(time_step_input[step],0,1)
			nmnist_input = torch.where(x)
			input_spikes = []

			for spikes in range(len(nmnist_input[0])):
				i_c_index = nmnist_input[1][spikes]
				i_h_index = nmnist_input[2][spikes]
				i_w_index = nmnist_input[3][spikes]
				c_grp_upd = i_c_index//4
				h_grp_upd = i_h_index//4
				w_grp_upd = i_w_index//4
				c_decode_index = i_c_index%4
				h_decode_index = i_h_index%4
				w_decode_index = i_w_index%4
				grp_update = 64*(w_grp_upd+(h_grp_upd*8)+(c_grp_upd*64))
				index_dec = w_decode_index+(h_decode_index*4)+(c_decode_index*16)
				input_index = grp_update+index_dec
				input_spikes.append([2,0,input_index])
				input_spikes.append([3,0,input_index])
			input_spikes.append([2,1,0])	# dummy
			input_spikes.append([3,1,0])	# dummy			

			Neo_ISA.input_event(input_spikes)
			Neo_ISA.time_step_exe_start()
			ISA_packet = Neo_ISA.instruction_packet_out()
			UART(ISA_packet)
			Neo_ISA.flush()

			# while True:
			# 	d_out = ser.read(3)
			# 	if(d_out != b''):
			# 		d_out = int.from_bytes(d_out, "little")

			# 		if(d_out==16777215):
			# 			break
					# elif(20672<=d_out<=20672+10-1):
					# 	o_layer_spike[0][d_out-20672] += 1
			# 		elif(d_out>131071):
			# 			print(d_out, "error")

		Neo_ISA.batch_done()
		ISA_packet = Neo_ISA.instruction_packet_out()
		UART(ISA_packet)
		Neo_ISA.flush()

		output_Neo = o_layer_spike / self.T

		return output_Neo

