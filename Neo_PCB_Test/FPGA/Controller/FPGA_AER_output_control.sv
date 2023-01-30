`timescale 1ns / 1ps

//////////////////////////////////////////////////////////////////////////////////
// Company: Emerging Computong lab
// Engineer: ChangMin Ye

// Design Name: Neo_PCB_TEST
// Module Name: FPGA_AER_output_control

// Description: Output Data to host python interface
//              1) Event Packet
//              2) Time step done signal 
//////////////////////////////////////////////////////////////////////////////////

module FPGA_AER_output_control
    (
    input logic clk,
    input logic rst,

    input logic chip_done_signal,
    output logic exe_end_signal,

    input logic fpga_to_pc_valid,
    input logic [21:0] fpga_to_pc_data_out,

    input logic tx_busy,
    input logic tx_done,
    output logic data_out_fpga_valid,
    output logic [7:0] data_out_fpga,
    output logic [2:0] output_state
    );

localparam [2:0] state_idle = 3'b000;
localparam [2:0] state_chip_done_ready = 3'b001;
localparam [2:0] state_event_output_busy = 3'b010;
localparam [2:0] state_output_done = 3'b011;

logic full, empty;
logic host_output_req;
logic output_data_read_enable, output_data_read_enable_d, output_data_read_enable_2d;
logic tx_done_d, tx_done_2d;
logic [21:0] output_data_ready;
logic [2:0] output_state;
logic [1:0] counter;
logic output_data_emulate_done, output_data_emulate_done_d;
logic chip_done_signal_d, chip_done_signal_2d;

fpga_output_event_fifo fpga_output_event_fifo
    (
    .clk(clk),
    .srst(rst),
    .wr_en(fpga_to_pc_valid),
    .din(fpga_to_pc_data_out),
    .full(full),
    .rd_en(output_data_read_enable),
    .dout(output_data_ready),
    .empty(empty)
    );

assign host_output_req = !empty;

always @(posedge clk) begin
    chip_done_signal_d <= chip_done_signal;
    chip_done_signal_2d <= chip_done_signal_d;
end

always @(posedge clk) begin
    if(rst) begin
        output_state <= state_idle;
        counter <= '0;
        exe_end_signal <= '0;
    end
    else begin
        case(output_state)
            state_idle : begin
                if(chip_done_signal_2d) begin
                    output_state <= state_chip_done_ready;
                    exe_end_signal <= '1;
                end
                else output_state <= state_idle;
            end
            state_chip_done_ready : begin
                exe_end_signal <= '0;
                if(chip_done_signal_2d) output_state <= state_chip_done_ready;
                else begin
                    output_state <= host_output_req ? state_event_output_busy : state_output_done;
                    counter <= host_output_req ? 2'd3 : 2'd2;
                end
            end
            state_event_output_busy : begin
                if(host_output_req) begin
                    if(counter==3) begin
                        output_data_read_enable <= '1;
                        counter <= counter - 1'b1;
                    end
                    else begin
                        output_data_read_enable <= '0;
                        data_out_fpga <= (counter==2'd2) ? output_data_ready[7:0] : ((counter==2'd1) ? output_data_ready[15:8] : ((counter==2'd0) ? {2'd0,output_data_ready[21:16]} : 8'd0));
                        counter <= tx_done ? ((counter!=0) ? counter - 1'b1 : 2'd3) : counter;
                    end
                end
                else begin
                    output_state <= ((counter==2'd0)&&tx_done) ? state_output_done : state_event_output_busy;
                    output_data_read_enable <= '0;
                    data_out_fpga <= (counter==2'd2) ? output_data_ready[7:0] : ((counter==2'd1) ? output_data_ready[15:8] : ((counter==2'd0) ? {2'd0,output_data_ready[21:16]} : 8'd0));
                    counter <= tx_done ? ((counter!=0) ? counter - 1'b1 : 2'd2) : counter;
                end             
            end
            state_output_done : begin
                if(counter!=0) begin
                    data_out_fpga <= (counter==2'd2) ? 8'b11111111 : ((counter==2'd1) ? 8'b11111111 : ((counter==2'd0) ? 8'b11111111 : '0));
                    counter       <= tx_done ? counter - 1'b1 : counter;
                end
                else begin
                    output_state <= (counter==2'd0) ? state_idle : state_output_done;
                end
            end
            default : begin
                output_state <= state_idle;
            end
        endcase // output_state
    end
end

always @(posedge clk) begin
    output_data_read_enable_d <= output_data_read_enable;
    output_data_read_enable_2d <= output_data_read_enable_d;

    tx_done_d <= tx_done;
    tx_done_2d <= ((output_state==state_event_output_busy)&&(counter==2'd3)) ? '0 : tx_done_d;
end

assign output_data_emulate_done = ((output_state==state_output_done)&&(!tx_busy)&&(!tx_done));

always @(posedge clk) begin
    output_data_emulate_done_d <= output_data_emulate_done;
end

assign data_out_fpga_valid = (((output_state==state_event_output_busy)&&(counter==4'd0)&&(tx_done_2d)) | ((output_state==state_event_output_busy)&&(counter==4'd1)&&(tx_done_2d)) | ((output_state==state_event_output_busy)&&(counter==4'd2)&&(tx_done_2d)) | output_data_read_enable_2d | output_data_emulate_done_d);

initial begin
    output_data_read_enable = '0;
    output_data_read_enable_d = '0;
    output_data_read_enable_2d = '0;
    tx_done_d = '0;
    tx_done_2d = '0;
    output_state = '0;
    counter = '0;
    output_data_emulate_done_d = '0;
    chip_done_signal_d = '0;
    chip_done_signal_2d = '0;
end

endmodule : FPGA_AER_output_control
