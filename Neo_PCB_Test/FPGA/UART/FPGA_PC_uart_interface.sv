`timescale 1ns / 1ps

//////////////////////////////////////////////////////////////////////////////////
// Company: Emerging Computong lab
// Engineer: ChangMin Ye

// Design Name: Neo_PCB_TEST
// Module Name: FPGA_PC_uart_interface

// Description: chip-host uart serial interface

//				1) uart rx : data from host, input to FPGA
//				2) uart tx : data from FPGA, output to host
//////////////////////////////////////////////////////////////////////////////////

module FPGA_PC_uart_interface
	(
	input logic clk,
	input logic rst,

	input logic rx_d_in,
	output logic data_from_pc_valid,
	output logic [7:0] data_from_pc,

	output logic tx_d_out,

	input logic data_out_fpga_valid,
	input logic [7:0] data_out_fpga,
	output logic tx_busy,
	output logic tx_done
	);

//////// Uart serial rx input ////////
uart_rx uart_rx
	(
	.i_Rst_L(rst),
	.i_Clock(clk),
	.i_RX_Serial(rx_d_in),
	.o_RX_DV(data_from_pc_valid),
	.o_RX_Byte(data_from_pc)
   );
//////////////////////////////////////


//////// Uart serial tx output ////////
uart_tx uart_tx
  (
	.i_Rst_L(rst),
	.i_Clock(clk),
	.i_TX_DV(data_out_fpga_valid),
	.i_TX_Byte(data_out_fpga), 
	.o_TX_Active(tx_busy),
	.o_TX_Serial(tx_d_out),
	.o_TX_Done(tx_done)
   );
///////////////////////////////////////

endmodule : FPGA_PC_uart_interface