`timescale 1ns / 1ps

`include "../Neo_PCB_Parameter.sv"

//////////////////////////////////////////////////////////////////////////////////
// Company: Emerging Computong lab
// Engineer: ChangMin Ye

// Design Name: Neo_PCB_TEST
// Module Name: FPGA_Neo_hanshake_rx

// Description: Packet input from Neo
//////////////////////////////////////////////////////////////////////////////////

module FPGA_Neo_hanshake_rx
	(
	input logic clk,
	input logic rst,

	input logic boundary_w_en,
	input logic [$clog2(`GLOBAL_NEURON)-1:0] chip_boundary_offset,

	input logic req_in,
	output logic ack_out,

	input logic [11-1:0] rx_packet_in,

	output logic ext_spike_out,
	output logic [5+1+$clog2(`GLOBAL_NEURON)-1:0] ext_packet_out,

	input logic chip_exe_valid,
	output logic chip_exe_valid_synchronized
	);

localparam input_idle   = 1'b0;
localparam input_sample = 1'b1;

logic [$clog2(`GLOBAL_NEURON)-1:0] offset_value;
logic input_handshake_state;
logic req_in_d, req_in_2d, req_in_3d;
logic req_done, req_done_d;
logic counter;
logic [10:0] rx_data_sample_0, rx_data_sample_1;
logic [5+1+$clog2(`GLOBAL_NEURON)-1:0] rx_data_sample_ready;
logic chip_exe_valid_d, chip_exe_valid_2d;

always @(posedge clk) begin
	if(rst) offset_value <= '0;
	else if(boundary_w_en) offset_value <= chip_boundary_offset;
end

always @(posedge clk) begin
	req_in_d <= req_in;
	req_in_2d <= req_in_d;
	req_in_3d <= req_in_2d;
end

assign ack_out = req_in_3d;

assign req_done = req_in_3d && (!req_in_2d);

always @(posedge clk) begin
	if(rst) counter <= '0;
	else counter <= (req_done) ? counter + 1'b1 : counter;
end

always @(posedge clk) begin
	req_done_d <= req_done;
end

assign ext_spike_out = (req_done_d&&(counter==1'b0));

always @(posedge clk) begin
	if(rst) input_handshake_state <= input_idle;
	else begin
		case(input_handshake_state)
			input_idle : begin
				if(req_in) input_handshake_state <= input_sample;
				else input_handshake_state <= input_idle;
			end
			input_sample : begin
				input_handshake_state <= req_done ? input_idle : input_sample;
				rx_data_sample_0 <= ((req_in_d|req_in_2d)&&(counter==1'b0)) ? rx_packet_in : rx_data_sample_0;
				rx_data_sample_1 <= ((req_in_d|req_in_2d)&&(counter==1'b1)) ? rx_packet_in : rx_data_sample_1;
			end
			default : begin
				input_handshake_state <= input_idle;
			end
		endcase // input_handshake_state
	end
end

assign rx_data_sample_ready = {rx_data_sample_1,rx_data_sample_0};

always @(posedge clk) begin
	if(rst) ext_packet_out <= '0;
	else if((req_done)&&(counter==1'b1)) ext_packet_out <= rx_data_sample_ready - {6'b0,offset_value};
end

always @(posedge clk) begin
	chip_exe_valid_d <= chip_exe_valid;
	chip_exe_valid_2d <= chip_exe_valid_d;
end

assign chip_exe_valid_synchronized = chip_exe_valid_2d;

initial begin
	offset_value = '0;
	req_in_d = '0;
	req_in_2d = '0;
	req_in_3d = '0;
	counter = '0;
	req_done_d = '0;
	input_handshake_state = input_idle;
	rx_data_sample_0 = '0;
	rx_data_sample_1 = '0;
	ext_packet_out = '0;
	chip_exe_valid_d = '0;
	chip_exe_valid_2d = '0;	
end

endmodule : FPGA_Neo_hanshake_rx