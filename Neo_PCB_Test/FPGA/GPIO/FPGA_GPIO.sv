`timescale 1ns / 1ps

//////////////////////////////////////////////////////////////////////////////////
// Company: Emerging Computong lab
// Engineer: ChangMin Ye

// Design Name: Neo_PCB_TEST
// Module Name: FPGA_GPIO

// Description: GPIO Neo <-> FPGA
//////////////////////////////////////////////////////////////////////////////////

module FPGA_GPIO
	(
	// Clock and Reset 
	input logic clk,
	input logic rst,

	output logic fmc_out_clk,
	output logic fmc_out_rst,

	// Chip selection
	output logic fmc_out_chip_sel,

	// Instruction
	input logic instruction_req,
	input logic [32-1:0] instruction_chunked,
	output logic instruction_ack,

	output logic fmc_out_instruction_req,
	output logic [32-1:0] fmc_out_instruction_chunked,
	input logic fmc_in_instruction_ack,
	
	// Membrane
	output logic target_membrane_out,
	output logic [16-1:0] target_membrane_potential,

	input logic fmc_in_target_membrane_out,
	input logic [16-1:0] fmc_in_target_membrane_potential,

	// RX North port
	output logic fmc_out_rx_req_in_north,
	input logic fmc_in_rx_ack_out_north,
	output logic [11-1:0] fmc_out_rx_packet_in_north,
	output logic fmc_out_chip_exe_valid_north,

	output logic rx_ack_out_north,

	// RX East port
	output logic fmc_out_rx_req_in_east,
	input logic fmc_in_rx_ack_out_east,
	output logic [11-1:0] fmc_out_rx_packet_in_east,
	output logic fmc_out_chip_exe_valid_east,

	output logic rx_ack_out_east,

	// RX West port
	output logic fmc_out_rx_req_in_west,
	input logic fmc_in_rx_ack_out_west,
	output logic [11-1:0] fmc_out_rx_packet_in_west,
	output logic fmc_out_chip_exe_valid_west,

	output logic rx_ack_out_west,

	// TX North port
	input logic tx_ack_in_north,
	output logic tx_req_out_north,
	output logic [11-1:0] tx_data_chip_out_north,

	output logic fmc_out_tx_ack_in_north,
	input logic fmc_in_tx_req_out_north,
	input logic [11-1:0] fmc_in_tx_data_chip_out_north,

	// TX East port
	output logic fmc_out_tx_ack_in_east,
	input logic fmc_in_tx_req_out_east,
	input logic [11-1:0] fmc_in_tx_data_chip_out_east,

	output logic tx_req_out_east,
	output logic [11-1:0] tx_data_chip_out_east,

	// TX West port
	output logic fcm_out_tx_ack_in_west,
	input logic fmc_in_tx_req_out_west,
	input logic [11-1:0] fmc_in_tx_data_chip_out_west,

	output logic tx_req_out_west,
	output logic [11-1:0] tx_data_chip_out_west,

	// Neo Control
	input logic exe_end_signal,
	output logic chip_exe_valid_tx_north,
	output logic chip_exe_valid_tx_east,
	output logic chip_exe_valid_tx_west,
	output logic chip_done_signal,

	output logic fmc_out_exe_end_signal,
	input logic fmc_in_chip_exe_valid_tx_north,
	input logic fmc_in_chip_exe_valid_tx_east,
	input logic fmc_in_chip_exe_valid_tx_west,
	input logic fmc_in_chip_done_signal
	);

// Clock and Reset 
assign fmc_out_clk = clk;
assign fmc_out_rst = rst;

// Chip selection
assign fmc_out_chip_sel = 1'b1;

// Instruction
assign fmc_out_instruction_req = instruction_req;
assign fmc_out_instruction_chunked = instruction_chunked;
assign instruction_ack = fmc_in_instruction_ack;

// Membrane
assign target_membrane_out = fmc_in_target_membrane_out;
assign target_membrane_potential = fmc_in_target_membrane_potential;

// RX North port
assign fmc_out_rx_req_in_north = 1'b0;
assign fmc_out_rx_packet_in_north = 11'd0;
assign fmc_out_chip_exe_valid_north = 1'b1;

always @(posedge clk) begin
	if(rst) rx_ack_out_north <= 1'b0;
	else rx_ack_out_north <= fmc_in_rx_ack_out_north;
end

// RX East port
assign fmc_out_rx_req_in_east = 1'b0;
assign fmc_out_rx_packet_in_east = 11'd0;
assign fmc_out_chip_exe_valid_east = 1'b1;

always @(posedge clk) begin
	if(rst) rx_ack_out_east <= 1'b0;
	else rx_ack_out_east <= fmc_in_rx_ack_out_east;
end

// RX West port
assign fmc_out_rx_req_in_west = 1'b0;
assign fmc_out_rx_packet_in_west = 11'd0;
assign fmc_out_chip_exe_valid_west = 1'b1;

always @(posedge clk) begin
	if(rst) rx_ack_out_west <= 1'b0;
	else rx_ack_out_west <= fmc_in_rx_ack_out_west;
end

// TX North port
assign fmc_out_tx_ack_in_north = tx_ack_in_north;
assign tx_req_out_north = fmc_in_tx_req_out_north;
assign tx_data_chip_out_north = fmc_in_tx_data_chip_out_north;

// TX East port
assign fmc_out_tx_ack_in_east = 1'b0;

always @(posedge clk) begin
	if(rst) begin
		tx_req_out_east <= 1'b0;
		tx_data_chip_out_east <= 11'd0;
	end
	else begin
		tx_req_out_east <= fmc_in_tx_req_out_east;
		tx_data_chip_out_east <= fmc_in_tx_data_chip_out_east;
	end
end

// TX West port
assign fcm_out_tx_ack_in_west = 1'b0;

always @(posedge clk) begin
	if(rst) begin
		tx_req_out_west <= 1'b0;
		tx_data_chip_out_west <= 11'd0;
	end
	else begin
		tx_req_out_west <= fmc_in_tx_req_out_west;
		tx_data_chip_out_west <= fmc_in_tx_data_chip_out_west;
	end
end

// Neo Control
assign fmc_out_exe_end_signal = exe_end_signal;
assign chip_done_signal = fmc_in_chip_done_signal;


always @(posedge clk) begin
	if(rst) begin
		chip_exe_valid_tx_north <= 1'b0;
		chip_exe_valid_tx_east <= 1'b0;
		chip_exe_valid_tx_west <= 1'b0;
	end
	else begin
		chip_exe_valid_tx_north <= fmc_in_chip_exe_valid_tx_north;
		chip_exe_valid_tx_east <= fmc_in_chip_exe_valid_tx_east;
		chip_exe_valid_tx_west <= fmc_in_chip_exe_valid_tx_west;
	end
end

endmodule : FPGA_GPIO


