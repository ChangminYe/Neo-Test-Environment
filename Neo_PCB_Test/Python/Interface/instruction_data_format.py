import numpy as np
from FixedPoint import FXfamily, FXnum

class instruction_encoder:
    def __init__(self):
        self.instruction = ''
        self.uart_ready_data = []
        self.core_NoC_dummy = format(0, '05b')
        self.select = 0

    def getBit(self, y,x):
        return str((x>>y)&1)

    def tobin(self, x, count=8):
        shift = range(count-1, -1, -1)
        bits = map(lambda y: self.getBit(y, x), shift)
        return "".join(bits)
    
    def dummy_data(self):
        get_bin = lambda x, n: format(x, 'b').zfill(n)
        dummy = int(np.ceil(147/32)*32) - len(self.instruction)
        if(dummy!=0):
            dummy = get_bin(0,dummy)
        else:
            dummy = ''
        
        return dummy
    
    def active_core(self):
        opcode = format(1, '05b')
        active_core_bit_map = input("32 bit binary vector (31,30,29 . . . 0) ")
        self.instruction = active_core_bit_map+self.core_NoC_dummy+opcode
        self.instruction = self.dummy_data() + self.instruction
        # print(self.instruction, len(self.instruction))
        self.uart_ready_data.append(self.instruction)

    def input_event(self, list):
        opcode = format(2, '05b')
        # list - [destination core address,ghost,event neuron address]
        for inputs in range(len(list)):
            destination_core = format(list[inputs][0], '05b')
            ghost = format(list[inputs][1], '01b')
            event_address = format(list[inputs][2], '016b')
            self.instruction = destination_core+ghost+event_address+self.core_NoC_dummy+opcode
            self.instruction = self.dummy_data() + self.instruction
            # print(self.instruction, len(self.instruction))
            self.uart_ready_data.append(self.instruction)

    def time_step_exe_start(self):
        opcode = format(3, '05b')
        self.instruction = opcode
        self.instruction = self.dummy_data() + self.instruction
        # print(self.instruction, len(self.instruction))
        self.uart_ready_data.append(self.instruction)

    def batch_done(self):
        opcode = format(4, '05b')
        self.instruction = opcode
        self.instruction = self.dummy_data() + self.instruction
        # print(self.instruction, len(self.instruction))
        self.uart_ready_data.append(self.instruction)

    def rx_boundary_offset(self):
        opcode = format(5, '05b')
        rx_address_select = input("North, East, West : ")
        if(rx_address_select=="North"): rx_address = format(3, '05b')
        elif(rx_address_select=="East"): rx_address = format(7, '05b')
        elif(rx_address_select=="West"): rx_address = format(4, '05b')
        rx_boundary = format(int(input("offset value of %s : (0~65535) " %rx_address_select)), '016b')
        self.instruction = rx_boundary+rx_address+opcode
        self.instruction = self.dummy_data() + self.instruction
        self.uart_ready_data.append(self.instruction)

    def NoC_pointer_write(self, list):
        opcode = format(6, '05b')
        # list - [NoC address, pointer address, pointer word(start+end)]
        for datas in range(len(list)):
            NoC_address = format(int(list[datas][0]), '05b')
            pointer_address = format(int(list[datas][1]), '07b')
            pointer_word_A = format(int(list[datas][2]), '010b')
            pointer_word_B = format(int(list[datas][3]), '010b')
            self.instruction = pointer_word_A+pointer_word_B+pointer_address+NoC_address+opcode
            self.instruction = self.dummy_data() + self.instruction
            # print(self.instruction, len(self.instruction))
            self.uart_ready_data.append(self.instruction)  

    def NoC_destination_write(self, list):
        opcode = format(7, '05b')
        # list - [NoC address, destination address, destination word]
        for datas in range(len(list)):
            NoC_address = format(int(list[datas][0]), '05b')
            destination_address = format(int(list[datas][1]), '010b')
            destination_word = format(int(list[datas][2]), '05b')
            self.instruction = destination_word+destination_address+NoC_address+opcode
            self.instruction = self.dummy_data() + self.instruction
            # print(self.instruction, len(self.instruction))
            self.uart_ready_data.append(self.instruction)  

    def track_membrane_potential(self):
        opcode = format(8, '05b')
        self.select = int(input("Track membrane potential ? : \n [0] No \n [1] Yes"))

        if(self.select>=2):
            print("error")

        elif(self.select==1):
            target_neuron = int(input("Target neuron address : "))
            self.instruction = format(target_neuron, '016b')+format(self.select, '01b')+self.core_NoC_dummy+opcode
            self.instruction = self.dummy_data() + self.instruction
            # print(self.instruction, len(self.instruction))
            self.uart_ready_data.append(self.instruction)    

        else:
            self.instruction = format(self.select, '01b')+opcode
            self.instruction = self.dummy_data() + self.instruction
            # print(self.instruction, len(self.instruction))
            self.uart_ready_data.append(self.instruction)  

    def neuron_model_select(self,list):
        opcode = format(9, '05b')
        # list - [core address, neuron model(0:SRM, 1:LIF)]
        for datas in range(len(list)):
            core_address = format(list[datas][0], '05b')
            model = format(list[datas][1], '01b')
            self.instruction = model+core_address+opcode
            self.instruction = self.dummy_data() + self.instruction
            # print(self.instruction, len(self.instruction))
            self.uart_ready_data.append(self.instruction)

    def threshold_write(self, list):
        opcode = format(10, '05b')
        # list - [core address, threshold[Q10.6]]
        for datas in range(len(list)):
            core_address = format(list[datas][0], '05b')
            threshold = format(list[datas][1], '016b')
            self.instruction = threshold+core_address+opcode
            self.instruction = self.dummy_data() + self.instruction
            # print(self.instruction, len(self.instruction))
            self.uart_ready_data.append(self.instruction)

    def constant_write(self,list):
        opcode = format(11, '05b')
        # list - [core address, constant[Q5.6]] 
        for datas in range(len(list)):
            core_address = format(list[datas][0], '05b')
            constant = format(list[datas][1], '011b')
            self.instruction = constant+core_address+opcode
            self.instruction = self.dummy_data() + self.instruction
            # print(self.instruction, len(self.instruction))
            self.uart_ready_data.append(self.instruction)

    def TS_EFA_write(self,list):
        opcode = format(12, '05b')
        # list - [core address, ram sel, address, word]
        for datas in range(len(list)):
            core_address = format(list[datas][0], '05b')
            ram_sel = format(list[datas][1], '02b')
            efa_address = format(list[datas][2], '08b')
            efa_word = format(list[datas][3], '016b')
            self.instruction = efa_word+efa_address+ram_sel+core_address+opcode
            self.instruction = self.dummy_data() + self.instruction
            # print(self.instruction, len(self.instruction))
            self.uart_ready_data.append(self.instruction)

    def synaptic_weight_write(self,list):
        opcode = format(13, '05b')
        # list - [core address, LUT address, LUT word(16 weights)]
        for datas in range(len(list)):
            core_address = format(list[datas][0], '05b')
            lut_address = format(list[datas][1], '09b')
            lut_word = format(list[datas][2]) # 128b
            self.instruction = lut_word+lut_address+core_address+opcode
            self.instruction = self.dummy_data() + self.instruction
            # print(self.instruction, len(self.instruction))
            self.uart_ready_data.append(self.instruction)

    def group_lut_write(self,list):
        opcode = format(14, '05b')
        # list - [core address, LUT address, LUT word(L_id, g_w_id, g_h_id, g_c_id)]
        for datas in range(len(list)):
            core_address = format(list[datas][0], '05b')
            lut_address = format(list[datas][1], '010b')
            lut_word = format(list[datas][2], '05b') + format(list[datas][3], '05b') + format(list[datas][4], '05b') + format(list[datas][5], '05b')
            self.instruction = lut_word+lut_address+core_address+opcode
            self.instruction = self.dummy_data() + self.instruction
            # print(self.instruction, len(self.instruction))
            self.uart_ready_data.append(self.instruction)

    def layer_lut_write(self,list):
        opcode = format(15, '05b')
        # list - [core address, LUT address, LUT word(g_offset, #N, L_w, L_h, dim, connec_offset, #connec)]
        for datas in range(len(list)):
            core_address = format(int(list[datas][0]), '05b')
            lut_address = format(int(list[datas][1]), '05b')
            lut_word = format(int(list[datas][2]), '010b') + format(int(list[datas][3]), '016b') + format(int(list[datas][4]), '05b') + format(int(list[datas][5]), '05b') + format(int(list[datas][6]), '01b') + format(int(list[datas][7]), '08b') + format(int(list[datas][8]), '04b') 
            self.instruction = lut_word+lut_address+core_address+opcode
            self.instruction = self.dummy_data() + self.instruction
            # print(self.instruction, len(self.instruction))
            self.uart_ready_data.append(self.instruction)

    def connective_lut_write(self,list):
        opcode = format(16, '05b')
        # list - [core address, LUT address, LUT word]
        for datas in range(len(list)):
            core_address = format(int(list[datas][0]), '05b')
            lut_address = format(int(list[datas][1]), '08b')
            lut_word = format(int(list[datas][2]), '09b') + format(int(list[datas][3]), '05b') + format(int(list[datas][4]), '01b') + format(int(list[datas][5]), '01b') + format(int(list[datas][6]), '07b') + format(int(list[datas][7]), '03b') + format(int(list[datas][8]), '03b') + format(int(list[datas][9]), '02b') + self.tobin(FXnum(int(list[datas][10]),FXfamily(1,2)).scaledval, 2) + format(int(list[datas][11]), '03b') + format(int(list[datas][12]), '03b') + format(int(list[datas][13]), '02b') + self.tobin(FXnum(int(list[datas][14]),FXfamily(1,2)).scaledval, 2) + format(int(list[datas][15]), '07b') + format(int(list[datas][16]), '07b') 
            self.instruction = lut_word+lut_address+core_address+opcode
            self.instruction = self.dummy_data() + self.instruction
            # print(self.instruction, len(self.instruction))
            self.uart_ready_data.append(self.instruction)

    def output_manager_pointer_write(self,list):
        opcode = format(17, '05b')
        # list - [pointer address, pointer word(start+end)]
        for datas in range(len(list)):
            core_address = format(0, '05b')
            pointer_address = format(int(list[datas][0]), '010b')
            pointer_word_A = format(int(list[datas][1]), '010b')
            pointer_word_B = format(int(list[datas][2]), '010b')
            self.instruction = pointer_word_A+pointer_word_B+pointer_address+core_address+opcode
            self.instruction = self.dummy_data() + self.instruction
            # print(self.instruction, len(self.instruction))
            self.uart_ready_data.append(self.instruction)

    def output_manager_destination_write(self,list):
        opcode = format(18, '05b')
        # list - [destination address, destination word(chip out+core)]
        for datas in range(len(list)):
            core_address = format(0, '05b')
            destination_address = format(int(list[datas][0]), '010b')
            destination_word_A = format(int(list[datas][1]), '02b')
            destination_word_B = format(int(list[datas][2]), '05b')
            self.instruction = destination_word_A+destination_word_B+destination_address+core_address+opcode
            self.instruction = self.dummy_data() + self.instruction
            # print(self.instruction, len(self.instruction))
            self.uart_ready_data.append(self.instruction) 

    def instruction_packet_out(self):
        return self.uart_ready_data

    def flush(self):
        self.uart_ready_data = []

