import torch
import torchvision
import torchvision.transforms as transforms
import DVS_utils
from Network import Network_architecture
from torch.utils.data import DataLoader
from Dataset.pysnn.datasets import nmnist_train_test

def make_model(network, T, delta_t, max_firing_rate, batch_size, device, decay1, decay2, const, thresh):
	if network == "cNet_MNIST":
		return Network_architecture.cNet_MNIST(T, delta_t, max_firing_rate, batch_size, device, decay1, decay2, const, thresh)
	elif network == "cNet_DVS":
		return Network_architecture.cNet_DVS(T, batch_size, device, decay1, decay2, const, thresh)
	elif network == "cNet_NMNIST":
		return Network_architecture.cNet_NMNIST(T, batch_size, device, decay1, decay2, const, thresh)
	elif network == "LeNet_MNIST":
		return Network_architecture.LeNet_MNIST(T, delta_t, max_firing_rate, batch_size, device, decay1, decay2, const, thresh)
	elif network == "LeNet_DVS":
		return Network_architecture.LeNet_DVS(T, batch_size, device, decay1, decay2, const, thresh)
	elif network == "LeNet_NMNIST":
		return Network_architecture.LeNet_NMNIST(T, batch_size, device, decay1, decay2, const, thresh)
	else:
		print("Wrong command")


def make_evaluation_model(network, T, delta_t, max_firing_rate, device):
	if network == "cNet_MNIST":
		return Network_architecture.EVAL_cNet_MNIST(T, delta_t, max_firing_rate, device)
	elif network == "cNet_DVS":
		return Network_architecture.EVAL_cNet_DVS(T)
	elif network == "cNet_NMNIST":
		return Network_architecture.EVAL_cNet_NMNIST(T)
	elif network == "LeNet_MNIST":
		# return Network_architecture.EVAL_LeNet_MNIST(T, delta_t, max_firing_rate, device)
		return print("Not yet")
	elif network == "LeNet_DVS":
		# return Network_architecture.EVAL_LeNet_DVS(T, batch_size, device, decay1, decay2, const, thresh)
		return print("Not yet")
	elif network == "LeNet_NMNIST":
		# return Network_architecture.EVAL_LeNet_NMNIST(T, batch_size, device, decay1, decay2, const, thresh)
		return print("Not yet")
	else:
		print("Wrong command")


def load_pretrained(network):
	if network == "cNet_MNIST":
		return "./Pre_trained/ckptCNN_MNIST_cNet_archi_200hz_40ms_10ms_128step_0.1thr_adam_decay_e5.t7"
	elif network == "cNet_DVS":
		return "./Pre_trained/ckptCNN_DVS_cNet_5msdt_archi_50ms_10ms_300step_0.15th_decay_e5.t7"
	elif network == "cNet_NMNIST":
		return "./Pre_trained/ckptCNN_NMNIST_cNet_5msdt_archi_50ms_10ms_300step_0.1th.t7"
	elif network == "LeNet_MNIST":
		return "./Pre_trained/ckptCNN_MNIST_LeNet_archi_200hz_50ms_10ms_128step_0.15thr_adam_decay_e5.t7"
	elif network == "LeNet_DVS":
		return "./Pre_trained/ckptCNN_DVS_LeNet_5msdt_archi_50ms_10ms_300step_0.15th_adam_decay_e5.t7"
	elif network == "LeNet_NMNIST":
		return "./Pre_trained/ckptCNN_NMNIST_LeNet_5msdt_archi_50ms_10ms_300step_0.15th.t7"
	else:
		print("Wrong command")

def load_data(dataset, batch_size):
	if dataset == "MNIST":
		data_path =  '.Dataset/raw/'
		train_dataset = torchvision.datasets.MNIST(root=data_path, train=True, download=True, transform=transforms.ToTensor())
		train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
		test_set = torchvision.datasets.MNIST(root=data_path, train=False, download=True, transform=transforms.ToTensor())
		test_loader = torch.utils.data.DataLoader(test_set, batch_size=batch_size, shuffle=False, num_workers=0)

		return train_loader, test_loader

	elif dataset == "DVS":
		train_loader, test_loader = DVS_utils.load_data('DVS128-Gesture', 0, 4, 1, 1500, batch_size)  # num_workers, ds, dt, T, batch_size

		return train_loader, test_loader

	elif dataset == "NMNIST":
		root = "./Dataset/nmnist"
		num_workers = 0
		sampling_time = 1 #ms
		sample_length = 300

		train_dataset, test_dataset = nmnist_train_test(root, height=32, width=32, sampling_time=sampling_time, sample_length=sample_length)
		train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
		test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)

		return train_loader, test_loader

	else:
		print("Wrong command")
