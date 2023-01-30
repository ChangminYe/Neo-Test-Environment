import torch
from FixedPoint import FXfamily, FXnum

def getBit(y,x):
	return str((x>>y)&1)

def tobin(x, count=8):
	shift = range(count-1, -1, -1)
	bits = map(lambda y: getBit(y, x), shift)
	return "".join(bits)

def weight_fixed_point(x):
	if x > 1.984375:
		x_to_b = tobin(FXnum(1.984375,FXfamily(6,2)).scaledval, 8)
	elif x < -1.984375:
		x_to_b = tobin(FXnum(-1.984375,FXfamily(6,2)).scaledval, 8)
	else:
		x_to_b = tobin(FXnum(x,FXfamily(6,2)).scaledval, 8)

	return x_to_b

def Core_Synapse_(checkpoint):
	synapse_conv1 = checkpoint['net']['conv1.weight'].detach().cpu().numpy()
	synapse_conv2 = checkpoint['net']['conv2.weight'].detach().cpu().numpy()
	synapse_conv3 = checkpoint['net']['conv3.weight'].detach().cpu().numpy()
	synapse_conv4 = checkpoint['net']['conv4.weight'].detach().cpu().numpy()
	synapse_fc1 = checkpoint['net']['fc1.weight'].detach().cpu().numpy()

	print("********** Weight Quantization and Partition START **********")
	print("!! Compiler is not ready only manual partition is provided !!")
	syn_lut_core_2 = []

	synapse_conv1_chunk1 = synapse_conv1[:8,...]

	index = 0
	for post_channel in range(synapse_conv1_chunk1.shape[0]):
		for pre_channel in range(synapse_conv1_chunk1.shape[1]):
			for height in range(synapse_conv1_chunk1.shape[2]):
				for width in range(synapse_conv1_chunk1.shape[3]):
					syn_lut_core_2.append([2,index,weight_fixed_point(synapse_conv1_chunk1[post_channel][pre_channel][height][width])])
					index += 1

	syn_lut_core_3 = []

	synapse_conv1_chunk2 = synapse_conv1[8:,...]

	index = 0
	for post_channel in range(synapse_conv1_chunk2.shape[0]):
		for pre_channel in range(synapse_conv1_chunk2.shape[1]):
			for height in range(synapse_conv1_chunk2.shape[2]):
				for width in range(synapse_conv1_chunk2.shape[3]):
					syn_lut_core_3.append([3,index,weight_fixed_point(synapse_conv1_chunk2[post_channel][pre_channel][height][width])])
					index += 1

	syn_lut_core_4 = []

	synapse_conv2_chunk1 = synapse_conv2[:12,:8,...]
	synapse_conv2_chunk2 = synapse_conv2[:12,8:,...]

	index = 0
	for post_channel in range(synapse_conv2_chunk1.shape[0]):
		for pre_channel in range(synapse_conv2_chunk1.shape[1]):
			for height in range(synapse_conv2_chunk1.shape[2]):
				for width in range(synapse_conv2_chunk1.shape[3]):
					syn_lut_core_4.append([4,index,weight_fixed_point(synapse_conv2_chunk1[post_channel][pre_channel][height][width])])
					index += 1

	while index%64!=0:
		syn_lut_core_4.append([4,index,weight_fixed_point(0)])
		index += 1

	for post_channel in range(synapse_conv2_chunk2.shape[0]):
		for pre_channel in range(synapse_conv2_chunk2.shape[1]):
			for height in range(synapse_conv2_chunk2.shape[2]):
				for width in range(synapse_conv2_chunk2.shape[3]):
					syn_lut_core_4.append([4,index,weight_fixed_point(synapse_conv2_chunk2[post_channel][pre_channel][height][width])])
					index += 1

	while index%64!=0:
		syn_lut_core_4.append([4,index,weight_fixed_point(0)])
		index += 1

	syn_lut_core_5 = []

	synapse_conv2_chunk3 = synapse_conv2[12:24,:8,...]
	synapse_conv2_chunk4 = synapse_conv2[12:24,8:,...]

	index = 0
	for post_channel in range(synapse_conv2_chunk3.shape[0]):
		for pre_channel in range(synapse_conv2_chunk3.shape[1]):
			for height in range(synapse_conv2_chunk3.shape[2]):
				for width in range(synapse_conv2_chunk3.shape[3]):
					syn_lut_core_5.append([5,index,weight_fixed_point(synapse_conv2_chunk3[post_channel][pre_channel][height][width])])
					index += 1

	while index%64!=0:
		syn_lut_core_5.append([5,index,weight_fixed_point(0)])
		index += 1

	for post_channel in range(synapse_conv2_chunk4.shape[0]):
		for pre_channel in range(synapse_conv2_chunk4.shape[1]):
			for height in range(synapse_conv2_chunk4.shape[2]):
				for width in range(synapse_conv2_chunk4.shape[3]):
					syn_lut_core_5.append([5,index,weight_fixed_point(synapse_conv2_chunk4[post_channel][pre_channel][height][width])])
					index += 1

	while index%64!=0:
		syn_lut_core_5.append([5,index,weight_fixed_point(0)])
		index += 1

	syn_lut_core_6 = []

	synapse_conv2_chunk5 = synapse_conv2[24:32,:8,...]
	synapse_conv2_chunk6 = synapse_conv2[24:32,8:,...]
	synapse_conv3_chunk1 = synapse_conv3[:12,:12,...]
	synapse_conv3_chunk2 = synapse_conv3[:12,12:24,...]
	synapse_conv3_chunk3 = synapse_conv3[:12,24:32,...]

	index = 0
	for post_channel in range(synapse_conv2_chunk5.shape[0]):
		for pre_channel in range(synapse_conv2_chunk5.shape[1]):
			for height in range(synapse_conv2_chunk5.shape[2]):
				for width in range(synapse_conv2_chunk5.shape[3]):
					syn_lut_core_6.append([6,index,weight_fixed_point(synapse_conv2_chunk5[post_channel][pre_channel][height][width])])
					index += 1

	for post_channel in range(synapse_conv2_chunk6.shape[0]):
		for pre_channel in range(synapse_conv2_chunk6.shape[1]):
			for height in range(synapse_conv2_chunk6.shape[2]):
				for width in range(synapse_conv2_chunk6.shape[3]):
					syn_lut_core_6.append([6,index,weight_fixed_point(synapse_conv2_chunk6[post_channel][pre_channel][height][width])])
					index += 1

	for post_channel in range(synapse_conv3_chunk1.shape[0]):
		for pre_channel in range(synapse_conv3_chunk1.shape[1]):
			for height in range(synapse_conv3_chunk1.shape[2]):
				for width in range(synapse_conv3_chunk1.shape[3]):
					syn_lut_core_6.append([6,index,weight_fixed_point(synapse_conv3_chunk1[post_channel][pre_channel][height][width])])
					index += 1

	while index%64!=0:
		syn_lut_core_6.append([6,index,weight_fixed_point(0)])
		index += 1

	for post_channel in range(synapse_conv3_chunk2.shape[0]):
		for pre_channel in range(synapse_conv3_chunk2.shape[1]):
			for height in range(synapse_conv3_chunk2.shape[2]):
				for width in range(synapse_conv3_chunk2.shape[3]):
					syn_lut_core_6.append([6,index,weight_fixed_point(synapse_conv3_chunk2[post_channel][pre_channel][height][width])])
					index += 1

	while index%64!=0:
		syn_lut_core_6.append([6,index,weight_fixed_point(0)])
		index += 1

	for post_channel in range(synapse_conv3_chunk3.shape[0]):
		for pre_channel in range(synapse_conv3_chunk3.shape[1]):
			for height in range(synapse_conv3_chunk3.shape[2]):
				for width in range(synapse_conv3_chunk3.shape[3]):
					syn_lut_core_6.append([6,index,weight_fixed_point(synapse_conv3_chunk3[post_channel][pre_channel][height][width])])
					index += 1

	while index%64!=0:
		syn_lut_core_6.append([6,index,weight_fixed_point(0)])
		index += 1

	syn_lut_core_7 = []

	synapse_conv3_chunk4 = synapse_conv3[12:44,:12,...]
	synapse_conv3_chunk5 = synapse_conv3[12:44,12:24,...]
	synapse_conv3_chunk6 = synapse_conv3[12:44,24:32,...]

	index = 0
	for post_channel in range(synapse_conv3_chunk4.shape[0]):
		for pre_channel in range(synapse_conv3_chunk4.shape[1]):
			for height in range(synapse_conv3_chunk4.shape[2]):
				for width in range(synapse_conv3_chunk4.shape[3]):
					syn_lut_core_7.append([7,index,weight_fixed_point(synapse_conv3_chunk4[post_channel][pre_channel][height][width])])
					index += 1

	for post_channel in range(synapse_conv3_chunk5.shape[0]):
		for pre_channel in range(synapse_conv3_chunk5.shape[1]):
			for height in range(synapse_conv3_chunk5.shape[2]):
				for width in range(synapse_conv3_chunk5.shape[3]):
					syn_lut_core_7.append([7,index,weight_fixed_point(synapse_conv3_chunk5[post_channel][pre_channel][height][width])])
					index += 1

	for post_channel in range(synapse_conv3_chunk6.shape[0]):
		for pre_channel in range(synapse_conv3_chunk6.shape[1]):
			for height in range(synapse_conv3_chunk6.shape[2]):
				for width in range(synapse_conv3_chunk6.shape[3]):
					syn_lut_core_7.append([7,index,weight_fixed_point(synapse_conv3_chunk6[post_channel][pre_channel][height][width])])
					index += 1

	syn_lut_core_8 = []

	synapse_conv3_chunk7 = synapse_conv3[44:64,:12,...]
	synapse_conv3_chunk8 = synapse_conv3[44:64,12:24,...]
	synapse_conv3_chunk9 = synapse_conv3[44:64,24:32,...]
	synapse_conv4_chunk1 = synapse_conv4[:,:12,...]
	synapse_conv4_chunk2 = synapse_conv4[:,12:44,...]
	synapse_conv4_chunk3 = synapse_conv4[:,44:64,...]

	index = 0
	for post_channel in range(synapse_conv3_chunk7.shape[0]):
		for pre_channel in range(synapse_conv3_chunk7.shape[1]):
			for height in range(synapse_conv3_chunk7.shape[2]):
				for width in range(synapse_conv3_chunk7.shape[3]):
					syn_lut_core_8.append([8,index,weight_fixed_point(synapse_conv3_chunk7[post_channel][pre_channel][height][width])])
					index += 1

	while index%64!=0:
		syn_lut_core_8.append([8,index,weight_fixed_point(0)])
		index += 1

	for post_channel in range(synapse_conv3_chunk8.shape[0]):
		for pre_channel in range(synapse_conv3_chunk8.shape[1]):
			for height in range(synapse_conv3_chunk8.shape[2]):
				for width in range(synapse_conv3_chunk8.shape[3]):
					syn_lut_core_8.append([8,index,weight_fixed_point(synapse_conv3_chunk8[post_channel][pre_channel][height][width])])
					index += 1

	while index%64!=0:
		syn_lut_core_8.append([8,index,weight_fixed_point(0)])
		index += 1

	for post_channel in range(synapse_conv3_chunk9.shape[0]):
		for pre_channel in range(synapse_conv3_chunk9.shape[1]):
			for height in range(synapse_conv3_chunk9.shape[2]):
				for width in range(synapse_conv3_chunk9.shape[3]):
					syn_lut_core_8.append([8,index,weight_fixed_point(synapse_conv3_chunk9[post_channel][pre_channel][height][width])])
					index += 1

	while index%64!=0:
		syn_lut_core_8.append([8,index,weight_fixed_point(0)])
		index += 1

	for post_channel in range(12):
		for pre_channel in range(synapse_conv4_chunk1.shape[1]):
			for height in range(synapse_conv4_chunk1.shape[2]):
				for width in range(synapse_conv4_chunk1.shape[3]):
					if(post_channel<synapse_conv4_chunk1.shape[0]):
						syn_lut_core_8.append([8,index,weight_fixed_point(synapse_conv4_chunk1[post_channel][pre_channel][height][width])])
					else:
						syn_lut_core_8.append([8,index,weight_fixed_point(0)])
					index += 1

	for post_channel in range(12):
		for pre_channel in range(synapse_conv4_chunk2.shape[1]):
			for height in range(synapse_conv4_chunk2.shape[2]):
				for width in range(synapse_conv4_chunk2.shape[3]):
					if(post_channel<synapse_conv4_chunk2.shape[0]):
						syn_lut_core_8.append([8,index,weight_fixed_point(synapse_conv4_chunk2[post_channel][pre_channel][height][width])])
					else:
						syn_lut_core_8.append([8,index,weight_fixed_point(0)])
					index += 1

	for post_channel in range(12):
		for pre_channel in range(synapse_conv4_chunk3.shape[1]):
			for height in range(synapse_conv4_chunk3.shape[2]):
				for width in range(synapse_conv4_chunk3.shape[3]):
					if(post_channel<synapse_conv4_chunk3.shape[0]):
						syn_lut_core_8.append([8,index,weight_fixed_point(synapse_conv4_chunk3[post_channel][pre_channel][height][width])])
					else:
						syn_lut_core_8.append([8,index,weight_fixed_point(0)])
					index += 1

	for post_neuron in range(64):
		for pre_neuron in range(192):
			if(post_neuron>9):
				syn_lut_core_8.append([8,index,weight_fixed_point(0)])
			else:
				grp_id = pre_neuron//64
				z_id = (pre_neuron-(64*grp_id))//16 + 4*grp_id
				y_id = ((pre_neuron-(64*grp_id)) - 16*((pre_neuron-(64*grp_id))//16))//4
				x_id = pre_neuron-(64*grp_id) - 16*((pre_neuron-(64*grp_id))//16) - 4*(((pre_neuron-(64*grp_id)) - 16*((pre_neuron-(64*grp_id))//16))//4)

				if((x_id<2) and (y_id<2) and (z_id<10)):
					i = z_id*4 + y_id*2 + x_id
					syn_lut_core_8.append([8,index,weight_fixed_point(synapse_fc1[post_neuron][i])])
				else:
					syn_lut_core_8.append([8,index,weight_fixed_point(0)])
			index += 1

	syn_lut = []
	lut_address = 0; counter = 1; word = ''
	for core_synapse_id in range(len(syn_lut_core_2)):
		weight_fixp16 = syn_lut_core_2[core_synapse_id][2]
		word = weight_fixp16 + word
		if(counter%64==0):
			syn_lut.append([syn_lut_core_2[core_synapse_id][0], lut_address, word[-128:]])
			syn_lut.append([syn_lut_core_2[core_synapse_id][0], lut_address, word[-256:-128]])
			syn_lut.append([syn_lut_core_2[core_synapse_id][0], lut_address, word[-384:-256]])
			syn_lut.append([syn_lut_core_2[core_synapse_id][0], lut_address, word[-512:-384]])
			lut_address += 1
			word = ''
		counter += 1

	lut_address = 0; counter = 1; word = ''
	for core_synapse_id in range(len(syn_lut_core_3)):
		weight_fixp16 = syn_lut_core_3[core_synapse_id][2]
		word = weight_fixp16 + word
		if(counter%64==0):
			syn_lut.append([syn_lut_core_3[core_synapse_id][0], lut_address, word[-128:]])
			syn_lut.append([syn_lut_core_3[core_synapse_id][0], lut_address, word[-256:-128]])
			syn_lut.append([syn_lut_core_3[core_synapse_id][0], lut_address, word[-384:-256]])
			syn_lut.append([syn_lut_core_3[core_synapse_id][0], lut_address, word[-512:-384]])
			lut_address += 1
			word = ''
		counter += 1

	lut_address = 0; counter = 1; word = ''
	for core_synapse_id in range(len(syn_lut_core_4)):
		weight_fixp16 = syn_lut_core_4[core_synapse_id][2]
		word = weight_fixp16 + word
		if(counter%64==0):
			syn_lut.append([syn_lut_core_4[core_synapse_id][0], lut_address, word[-128:]])
			syn_lut.append([syn_lut_core_4[core_synapse_id][0], lut_address, word[-256:-128]])
			syn_lut.append([syn_lut_core_4[core_synapse_id][0], lut_address, word[-384:-256]])
			syn_lut.append([syn_lut_core_4[core_synapse_id][0], lut_address, word[-512:-384]])
			lut_address += 1
			word = ''
		counter += 1

	lut_address = 0; counter = 1; word = ''
	for core_synapse_id in range(len(syn_lut_core_5)):
		weight_fixp16 = syn_lut_core_5[core_synapse_id][2]
		word = weight_fixp16 + word
		if(counter%64==0):
			syn_lut.append([syn_lut_core_5[core_synapse_id][0], lut_address, word[-128:]])
			syn_lut.append([syn_lut_core_5[core_synapse_id][0], lut_address, word[-256:-128]])
			syn_lut.append([syn_lut_core_5[core_synapse_id][0], lut_address, word[-384:-256]])
			syn_lut.append([syn_lut_core_5[core_synapse_id][0], lut_address, word[-512:-384]])
			lut_address += 1
			word = ''
		counter += 1

	lut_address = 0; counter = 1; word = ''
	for core_synapse_id in range(len(syn_lut_core_6)):
		weight_fixp16 = syn_lut_core_6[core_synapse_id][2]
		word = weight_fixp16 + word
		if(counter%64==0):
			syn_lut.append([syn_lut_core_6[core_synapse_id][0], lut_address, word[-128:]])
			syn_lut.append([syn_lut_core_6[core_synapse_id][0], lut_address, word[-256:-128]])
			syn_lut.append([syn_lut_core_6[core_synapse_id][0], lut_address, word[-384:-256]])
			syn_lut.append([syn_lut_core_6[core_synapse_id][0], lut_address, word[-512:-384]])
			lut_address += 1
			word = ''
		counter += 1

	lut_address = 0; counter = 1; word = ''
	for core_synapse_id in range(len(syn_lut_core_7)):
		weight_fixp16 = syn_lut_core_7[core_synapse_id][2]
		word = weight_fixp16 + word
		if(counter%64==0):
			syn_lut.append([syn_lut_core_7[core_synapse_id][0], lut_address, word[-128:]])
			syn_lut.append([syn_lut_core_7[core_synapse_id][0], lut_address, word[-256:-128]])
			syn_lut.append([syn_lut_core_7[core_synapse_id][0], lut_address, word[-384:-256]])
			syn_lut.append([syn_lut_core_7[core_synapse_id][0], lut_address, word[-512:-384]])
			lut_address += 1
			word = ''
		counter += 1

	lut_address = 0; counter = 1; word = ''
	for core_synapse_id in range(len(syn_lut_core_8)):
		weight_fixp16 = syn_lut_core_8[core_synapse_id][2]
		word = weight_fixp16 + word
		if(counter%64==0):
			syn_lut.append([syn_lut_core_8[core_synapse_id][0], lut_address, word[-128:]])
			syn_lut.append([syn_lut_core_8[core_synapse_id][0], lut_address, word[-256:-128]])
			syn_lut.append([syn_lut_core_8[core_synapse_id][0], lut_address, word[-384:-256]])
			syn_lut.append([syn_lut_core_8[core_synapse_id][0], lut_address, word[-512:-384]])
			lut_address += 1
			word = ''
		counter += 1
	print("********** Weight Quantization and Partition END **********\n")
	return syn_lut
















