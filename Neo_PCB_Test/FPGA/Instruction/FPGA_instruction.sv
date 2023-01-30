`timescale 1ns / 1ps

//////////////////////////////////////////////////////////////////////////////////
// Company: Emerging Computong lab
// Engineer: ChangMin Ye

// Design Name: Neo_PCB_TEST
// Module Name: FPGA_instruction

// Description: Instruction control
//////////////////////////////////////////////////////////////////////////////////

module FPGA_instruction
	(
	input logic clk,
	input logic rst,

	input logic data_from_pc_valid,
	input logic [7:0] data_from_pc,

	input logic instruction_ack,
	output logic instruction_req,
	output logic [32-1:0] instruction_chunked,
	
	output logic full
	);

logic instruction_valid;
logic [146:0] instruction;

FPGA_instruction_encoder FPGA_instruction_encoder
	(
	.clk(clk),
	.rst(rst),
	.data_from_pc_valid(data_from_pc_valid),
	.data_from_pc(data_from_pc),
	.instruction_valid(instruction_valid),
	.instruction(instruction)
	);

FPGA_instruction_handshake FPGA_instruction_handshake
    (
	.clk(clk),
	.rst(rst),
	.instruction_valid(instruction_valid),
	.instruction(instruction),
	.instruction_req(instruction_req),
	.instruction_chunked(instruction_chunked),
	.instruction_ack(instruction_ack),
	.full(full)
    );

endmodule : FPGA_instruction