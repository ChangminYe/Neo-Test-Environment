`timescale 1ns / 1ps

`include "../Neo_PCB_Parameter.sv"

//////////////////////////////////////////////////////////////////////////////////
// Company: Emerging Computong lab
// Engineer: ChangMin Ye

// Design Name: Neo_PCB_TEST
// Module Name: Neo_PCB_TEST

// Description: Top Wrapper module
//////////////////////////////////////////////////////////////////////////////////

module Neo_PCB_TEST
    (
    input logic usrclk_p, usrclk_n,
    input logic rst,

    input logic pushbtn_n,
    input logic pushbtn_e,
    input logic pushbtn_w,
    input logic pushbtn_s,

    // UART
    input logic rx_d_in,
    output logic tx_d_out,

    // FMC GPIO - clk, rst
    output logic fmc1_j2_1, fmc1_j2_2, 
    // FMC GPIO - Chip_sel
    output logic fmc1_j2_3, 
    // FMC GPIO - ISA_req
    output logic fmc1_j2_4,
    // FMC GPIO - ISA
    output logic [31:0] fmc1_j2_5_to_36,
    // FMC GPIO - ISA_ack
    input logic fmc1_j2_37,

    // FMC GPIO - North port_rx_req_in
    output logic fmc1_j1_1,
    // FMC GPIO - North port_rx_ack_out
    input logic fmc1_j1_2,
    // FMC GPIO - North port_rx_packet_out
    output logic [10:0] fmc1_j1_3_to_13,
    // FMC GPIO - North port_exe_valid_out
    output logic fmc1_j1_14,
    // FMC GPIO - North port_tx_ack_in
    output logic fmc1_j1_15,
    // FMC GPIO - North port_tx_req_out
    input logic fmc1_j1_16,
    // FMC GPIO - North port_tx_packet_in
    input logic [10:0] fmc1_j1_17_to_27,

    // FMC GPIO - East port_rx_req_in
    output logic fmc1_j3_1,
    // FMC GPIO - East port_rx_ack_out
    input logic fmc1_j3_2,
    // FMC GPIO - East port_rx_packet_out
    output logic [10:0] fmc1_j3_3_to_13,
    // FMC GPIO - East port_exe_valid_out
    output logic fmc1_j3_14,
    // FMC GPIO - East port_tx_ack_in
    output logic fmc1_j3_15,
    // FMC GPIO - East port_tx_req_out
    input logic fmc1_j3_16,
    // FMC GPIO - East port_tx_packet_in
    input logic [10:0] fmc1_j3_17_to_27,

    // FMC GPIO - West port_rx_req_in
    output logic fmc2_j3_11,
    // FMC GPIO - West port_rx_ack_out
    input logic fmc2_j3_12,
    // FMC GPIO - West port_rx_packet_out
    output logic [10:0] fmc2_j3_13_to_23,
    // FMC GPIO - West port_exe_valid_out
    output logic fmc2_j3_24,
    // FMC GPIO - West port_tx_ack_in
    output logic fmc2_j3_25,
    // FMC GPIO - West port_tx_req_out
    input logic fmc2_j3_26,
    // FMC GPIO - West port_tx_packet_in
    input logic [10:0] fmc2_j3_27_to_37,


    // FMC GPIO - Membrane valid
    input logic fmc2_j1_1,
    // FMC GPIO - Membrane
    input logic [15:0] fmc2_j1_2_to_17,

    // FMC GPIO - Neo_exe_end
    output logic fmc2_j3_1,
    // FMC GPIO - Neo_exe_valid_tx_north
    input logic fmc2_j3_2,
    // FMC GPIO - Neo_exe_valid_tx_east
    input logic fmc2_j3_3,
    // FMC GPIO - Neo_exe_valid_tx_west
    input logic fmc2_j3_4,
    // FMC GPIO - Neo_done_signal
    input logic fmc2_j3_5,

    // LED
    output logic [7:0] led
    );


logic clk;
logic data_from_pc_valid;
logic [7:0] data_from_pc;
logic tx_busy;
logic tx_done;
logic data_out_fpga_valid;
logic [7:0] data_out_fpga;
logic instruction_req;
logic [32-1:0] instruction_chunked;
logic instruction_ack;
logic handshake_full;
logic target_membrane_out;
logic [16-1:0] target_membrane_potential;
logic rx_ack_out_north; //Function test
logic rx_ack_out_east;  // Function test
logic rx_ack_out_west;  // Function test
logic tx_ack_in_north;
logic tx_req_out_north;
logic [11-1:0] tx_data_chip_out_north;
logic tx_req_out_east;  // Function test
logic [11-1:0] tx_data_chip_out_east;   // Function test
logic tx_req_out_west;  // Function test
logic [11-1:0] tx_data_chip_out_west;   // Function test
logic exe_end_signal;
logic chip_exe_valid_tx_north;  // Function test
logic chip_exe_valid_tx_east;   // Function test
logic chip_exe_valid_tx_west;   // Function test
logic chip_done_signal;
logic fpga_to_pc_valid;
logic [21:0] fpga_to_pc_data_out;
logic [2:0] output_state;
logic fmc_out_clk;
logic fmc_out_rst;
logic fmc_out_chip_sel;
logic fmc_out_instruction_req;
logic [32-1:0] fmc_out_instruction_chunked;
logic fmc_in_instruction_ack;
logic fmc_in_target_membrane_out;
logic [16-1:0] fmc_in_target_membrane_potential;
logic fmc_out_rx_req_in_north;
logic fmc_in_rx_ack_out_north;
logic [11-1:0] fmc_out_rx_packet_in_north;
logic fmc_out_chip_exe_valid_north;
logic fmc_out_rx_req_in_east;
logic fmc_in_rx_ack_out_east;
logic [11-1:0] fmc_out_rx_packet_in_east;
logic fmc_out_chip_exe_valid_east;
logic fmc_out_rx_req_in_west;
logic fmc_in_rx_ack_out_west;
logic [11-1:0] fmc_out_rx_packet_in_west;
logic fmc_out_chip_exe_valid_west;
logic fmc_out_tx_ack_in_north;
logic fmc_in_tx_req_out_north;
logic [11-1:0] fmc_in_tx_data_chip_out_north;
logic fmc_out_tx_ack_in_east;
logic fmc_in_tx_req_out_east;
logic [11-1:0] fmc_in_tx_data_chip_out_east;
logic fcm_out_tx_ack_in_west;
logic fmc_in_tx_req_out_west;
logic [11-1:0] fmc_in_tx_data_chip_out_west;
logic fmc_out_exe_end_signal;
logic fmc_in_chip_exe_valid_tx_north;
logic fmc_in_chip_exe_valid_tx_east;
logic fmc_in_chip_exe_valid_tx_west;
logic fmc_in_chip_done_signal;

////////////////////// FMC1 - J2 //////////////////////
assign fmc1_j2_1 = fmc_out_clk;
assign fmc1_j2_2 = fmc_out_rst;
assign fmc1_j2_3 = fmc_out_chip_sel;
assign fmc1_j2_4 = fmc_out_instruction_req;
assign fmc1_j2_5_to_36 = fmc_out_instruction_chunked;
assign fmc_in_instruction_ack = fmc1_j2_37;
///////////////////////////////////////////////////////

////////////////////// FMC1 - J1 //////////////////////
assign fmc1_j1_1 = fmc_out_rx_req_in_north;
assign fmc_in_rx_ack_out_north = fmc1_j1_2;
assign fmc1_j1_3_to_13 = fmc_out_rx_packet_in_north;
assign fmc1_j1_14 = fmc_out_chip_exe_valid_north;
assign fmc1_j1_15 = fmc_out_tx_ack_in_north;
assign fmc_in_tx_req_out_north = fmc1_j1_16;
assign fmc_in_tx_data_chip_out_north = fmc1_j1_17_to_27;
///////////////////////////////////////////////////////

////////////////////// FMC1 - J3 //////////////////////
assign fmc1_j3_1 = fmc_out_rx_req_in_east;
assign fmc_in_rx_ack_out_east = fmc1_j3_2;
assign fmc1_j3_3_to_13 = fmc_out_rx_packet_in_east;
assign fmc1_j3_14 = fmc_out_chip_exe_valid_east;
assign fmc1_j3_15 = fmc_out_tx_ack_in_east;
assign fmc_in_tx_req_out_east = fmc1_j3_16;
assign fmc_in_tx_data_chip_out_east = fmc1_j3_17_to_27;
///////////////////////////////////////////////////////

////////////////////// FMC2 - J2 //////////////////////
assign fmc2_j3_11 = fmc_out_rx_req_in_west;
assign fmc_in_rx_ack_out_west = fmc2_j3_12;
assign fmc2_j3_13_to_23 = fmc_out_rx_packet_in_west;
assign fmc2_j3_24 = fmc_out_chip_exe_valid_west;
assign fmc2_j3_25 = fcm_out_tx_ack_in_west;
assign fmc_in_tx_req_out_west = fmc2_j3_26;
assign fmc_in_tx_data_chip_out_west = fmc2_j3_27_to_37;
///////////////////////////////////////////////////////

////////////////////// FMC2 - J1 //////////////////////
assign fmc_in_target_membrane_out = fmc2_j1_1;
assign fmc_in_target_membrane_potential = fmc2_j1_2_to_17;
///////////////////////////////////////////////////////

////////////////////// FMC2 - J3 //////////////////////
assign fmc2_j3_1 = fmc_out_exe_end_signal;
assign fmc_in_chip_exe_valid_tx_north = fmc2_j3_2;
assign fmc_in_chip_exe_valid_tx_east = fmc2_j3_3;
assign fmc_in_chip_exe_valid_tx_west = fmc2_j3_4;
assign fmc_in_chip_done_signal = fmc2_j3_5;
///////////////////////////////////////////////////////

clk_wiz_0 clock
    (
    .clk_in1_p(usrclk_p),
    .clk_in1_n(usrclk_n),
    .clk_out1(clk)
    );

FPGA_PC_uart_interface FPGA_PC_uart_interface
    (
    .clk(clk),
    .rst(rst),
    .rx_d_in(rx_d_in),
    .data_from_pc_valid(data_from_pc_valid),
    .data_from_pc(data_from_pc),
    .tx_d_out(tx_d_out),
    .data_out_fpga_valid(data_out_fpga_valid),
    .data_out_fpga(data_out_fpga),
    .tx_busy(tx_busy),
    .tx_done(tx_done)
    );

FPGA_instruction FPGA_instruction
    (
    .clk(clk),
    .rst(rst),
    .data_from_pc_valid(data_from_pc_valid),
    .data_from_pc(data_from_pc),
    .instruction_ack(instruction_ack),
    .instruction_req(instruction_req),
    .instruction_chunked(instruction_chunked),
    .full(handshake_full)
    );

FPGA_GPIO FPGA_GPIO
    (
    // Clock and Reset 
    .clk(clk), .rst(rst),
    .fmc_out_clk(fmc_out_clk), .fmc_out_rst(fmc_out_rst),

    // Chip selection
    .fmc_out_chip_sel(fmc_out_chip_sel),

    // Instruction
    .instruction_req(instruction_req), .instruction_chunked(instruction_chunked), .instruction_ack(instruction_ack),
    .fmc_out_instruction_req(fmc_out_instruction_req), .fmc_out_instruction_chunked(fmc_out_instruction_chunked), .fmc_in_instruction_ack(fmc_in_instruction_ack),
    
    // Membrane
    .target_membrane_out(target_membrane_out), .target_membrane_potential(target_membrane_potential),
    .fmc_in_target_membrane_out(fmc_in_target_membrane_out), .fmc_in_target_membrane_potential(fmc_in_target_membrane_potential),

    // RX North port
    .fmc_out_rx_req_in_north(fmc_out_rx_req_in_north), .fmc_in_rx_ack_out_north(fmc_in_rx_ack_out_north), .fmc_out_rx_packet_in_north(fmc_out_rx_packet_in_north), .fmc_out_chip_exe_valid_north(fmc_out_chip_exe_valid_north),
    .rx_ack_out_north(rx_ack_out_north),

    // RX East port
    .fmc_out_rx_req_in_east(fmc_out_rx_req_in_east), .fmc_in_rx_ack_out_east(fmc_in_rx_ack_out_east), .fmc_out_rx_packet_in_east(fmc_out_rx_packet_in_east), .fmc_out_chip_exe_valid_east(fmc_out_chip_exe_valid_east),
    .rx_ack_out_east(rx_ack_out_east),

    // RX West port
    .fmc_out_rx_req_in_west(fmc_out_rx_req_in_west), .fmc_in_rx_ack_out_west(fmc_in_rx_ack_out_west), .fmc_out_rx_packet_in_west(fmc_out_rx_packet_in_west), .fmc_out_chip_exe_valid_west(fmc_out_chip_exe_valid_west),
    .rx_ack_out_west(rx_ack_out_west),

    // TX North port
    .tx_ack_in_north(tx_ack_in_north), .tx_req_out_north(tx_req_out_north), .tx_data_chip_out_north(tx_data_chip_out_north),
    .fmc_out_tx_ack_in_north(fmc_out_tx_ack_in_north), .fmc_in_tx_req_out_north(fmc_in_tx_req_out_north), .fmc_in_tx_data_chip_out_north(fmc_in_tx_data_chip_out_north),

    // TX East port
    .fmc_out_tx_ack_in_east(fmc_out_tx_ack_in_east), .fmc_in_tx_req_out_east(fmc_in_tx_req_out_east), .fmc_in_tx_data_chip_out_east(fmc_in_tx_data_chip_out_east),
    .tx_req_out_east(tx_req_out_east), .tx_data_chip_out_east(tx_data_chip_out_east),

    // TX West port
    .fcm_out_tx_ack_in_west(fcm_out_tx_ack_in_west), .fmc_in_tx_req_out_west(fmc_in_tx_req_out_west), .fmc_in_tx_data_chip_out_west(fmc_in_tx_data_chip_out_west),
    .tx_req_out_west(tx_req_out_west), .tx_data_chip_out_west(tx_data_chip_out_west),

    // Neo Control
    .exe_end_signal(exe_end_signal), .chip_exe_valid_tx_north(chip_exe_valid_tx_north), .chip_exe_valid_tx_east(chip_exe_valid_tx_east), .chip_exe_valid_tx_west(chip_exe_valid_tx_west), .chip_done_signal(chip_done_signal),
    .fmc_out_exe_end_signal(fmc_out_exe_end_signal), .fmc_in_chip_exe_valid_tx_north(fmc_in_chip_exe_valid_tx_north), .fmc_in_chip_exe_valid_tx_east(fmc_in_chip_exe_valid_tx_east), .fmc_in_chip_exe_valid_tx_west(fmc_in_chip_exe_valid_tx_west), .fmc_in_chip_done_signal(fmc_in_chip_done_signal)
    );

FPGA_Neo_hanshake_rx FPGA_Neo_hanshake_rx
    (
    .clk(clk),
    .rst(rst),
    .boundary_w_en(),
    .chip_boundary_offset(),
    .req_in(tx_req_out_north),
    .ack_out(tx_ack_in_north),
    .rx_packet_in(tx_data_chip_out_north),
    .ext_spike_out(fpga_to_pc_valid),
    .ext_packet_out(fpga_to_pc_data_out),
    .chip_exe_valid(),
    .chip_exe_valid_synchronized()
    );

FPGA_AER_output_control FPGA_AER_output_control
    (
    .clk(clk),
    .rst(rst),
    .chip_done_signal(chip_done_signal),
    .exe_end_signal(exe_end_signal),
    .fpga_to_pc_valid(fpga_to_pc_valid),
    .fpga_to_pc_data_out(fpga_to_pc_data_out),
    .tx_busy(tx_busy),
    .tx_done(tx_done),
    .data_out_fpga_valid(data_out_fpga_valid),
    .data_out_fpga(data_out_fpga),
    .output_state(output_state)
    );


//////////////////////////////////////////// LED TEST Control ////////////////////////////////////////////
logic [7:0] reg_north_port_test_point;
logic [7:0] reg_east_port_test_point_0, reg_east_port_test_point_1;
logic [7:0] reg_west_port_test_point_0, reg_west_port_test_point_1;
logic [7:0] reg_fpga_test_point;


logic pushbtn_n_d;
logic pushbtn_e_d;
logic pushbtn_w_d;

logic [1:0] counter_pushbtn_n;
logic [1:0] counter_pushbtn_e;
logic [1:0] counter_pushbtn_w;

// North port LED
always @(posedge clk) begin
    if(rst) reg_north_port_test_point <= 8'd0;
    else reg_north_port_test_point <= {rx_ack_out_north,6'd0,chip_exe_valid_tx_north};
end

always @(posedge clk) begin
    if(rst) pushbtn_n_d <= 1'b0;
    else pushbtn_n_d <= pushbtn_n;
end

always @(posedge clk) begin
    if(rst) counter_pushbtn_n <= 2'd0;
    else if(pushbtn_s) counter_pushbtn_n <= 2'd0;
    else counter_pushbtn_n <= (pushbtn_n_d && (!pushbtn_n)) ? counter_pushbtn_n + 1'b1 : counter_pushbtn_n;
end

// East port LED
always @(posedge clk) begin
    if(rst) begin
        reg_east_port_test_point_0 <= 8'd0;
        reg_east_port_test_point_1 <= 8'd0;
    end
    else begin
        reg_east_port_test_point_0 <= {tx_data_chip_out_east[6:0],chip_exe_valid_tx_east};
        reg_east_port_test_point_1 <= {rx_ack_out_east,tx_req_out_east,5'd0,tx_data_chip_out_east[7]};
    end
end

always @(posedge clk) begin
    if(rst) pushbtn_e_d <= 1'b0;
    else pushbtn_e_d <= pushbtn_e;
end

always @(posedge clk) begin
    if(rst) counter_pushbtn_e <= 2'd0;
    else if(pushbtn_s) counter_pushbtn_e <= 2'd0;
    else counter_pushbtn_e <= (pushbtn_e_d && (!pushbtn_e)) ? counter_pushbtn_e + 1'b1 : counter_pushbtn_e;
end

// West port LED
always @(posedge clk) begin
    if(rst) begin
        reg_west_port_test_point_0 <= 8'd0;
        reg_west_port_test_point_1 <= 8'd0;
    end
    else begin
        reg_west_port_test_point_0 <= {tx_data_chip_out_west[6:0],chip_exe_valid_tx_west};
        reg_west_port_test_point_1 <= {rx_ack_out_west,tx_req_out_west,5'd0,tx_data_chip_out_west[7]};
    end
end

always @(posedge clk) begin
    if(rst) pushbtn_w_d <= 1'b0;
    else pushbtn_w_d <= pushbtn_w;
end

always @(posedge clk) begin
    if(rst) counter_pushbtn_w <= 2'd0;
    else if(pushbtn_s) counter_pushbtn_w <= 2'd0;
    else counter_pushbtn_w <= (pushbtn_w_d && (!pushbtn_w)) ? counter_pushbtn_w + 1'b1 : counter_pushbtn_w;
end

// FPGA LED
always @(posedge clk) begin
    if(rst) reg_fpga_test_point <= 8'd0;
    else reg_fpga_test_point <= {handshake_full,3'b000,output_state};;
end


always @(posedge clk) begin
    if(rst) led <= 8'd0;
    else if(counter_pushbtn_n!=2'd0) led <= reg_north_port_test_point;
    else if(counter_pushbtn_e!=2'd0) led <= (counter_pushbtn_e==2'd1) ? reg_east_port_test_point_0 : ((counter_pushbtn_e==2'd2) ? reg_east_port_test_point_1 : reg_fpga_test_point);
    else if(counter_pushbtn_w!=2'd0) led <= (counter_pushbtn_w==2'd1) ? reg_west_port_test_point_0 : ((counter_pushbtn_w==2'd2) ? reg_west_port_test_point_1 : reg_fpga_test_point);
    else led <= reg_fpga_test_point;
end
//////////////////////////////////////////////////////////////////////////////////////////////////////////

endmodule : Neo_PCB_TEST
