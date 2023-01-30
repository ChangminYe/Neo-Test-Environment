`timescale 1ns / 1ps

//////////////////////////////////////////////////////////////////////////////////
// Company: Emerging Computong lab
// Engineer: ChangMin Ye

// Design Name: Neo_PCB_TEST
// Module Name: FPGA_instruction_encoder

// Description: generate instruction from uart interface
//////////////////////////////////////////////////////////////////////////////////

module FPGA_instruction_encoder
	(
	input logic clk,
	input logic rst,

	input logic data_from_pc_valid,
	input logic [7:0] data_from_pc,

	output logic instruction_valid,
	output logic [146:0] instruction 
	);

logic [4:0] counter;
logic instruction_valid;

always @(posedge clk) begin
	if(rst) counter <= 5'd0;
	else if(data_from_pc_valid) counter <= (counter==5'd20) ? 5'd1 : counter + 5'd1;
	else counter <= (counter==5'd20) ? 5'd0 : counter;
end

assign instruction_valid = (counter==5'd20);

always @(posedge clk) begin
	if(rst) instruction <= '0;
	else if(data_from_pc_valid) instruction <= {instruction[146-8:0],data_from_pc};
end

initial begin
	counter = 5'd0;
end

endmodule : FPGA_instruction_encoder