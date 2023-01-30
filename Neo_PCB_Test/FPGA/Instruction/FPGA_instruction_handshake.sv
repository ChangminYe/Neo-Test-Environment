`timescale 1ns / 1ps

//////////////////////////////////////////////////////////////////////////////////
// Company: Emerging Computong lab
// Engineer: ChangMin Ye

// Design Name: Neo_PCB_TEST
// Module Name: FPGA_instruction_handshake

// Description: generate instruction from uart interface
//////////////////////////////////////////////////////////////////////////////////

module FPGA_instruction_handshake
    (
    input logic clk,
    input logic rst,

    input logic instruction_valid,
    input logic [146:0] instruction,

    output logic instruction_req,
    output logic [32-1:0] instruction_chunked,
    input logic instruction_ack,

    output logic full
    );

localparam output_idle = 4'b0000;
localparam output_read = 4'b0001;
localparam output_read_delay = 4'b0010;
localparam output_req = 4'b0011;
localparam output_delay_1 = 4'b0100;
localparam output_delay_2 = 4'b0101;
localparam output_delay_3 = 4'b0110;
localparam output_delay_4 = 4'b0111;
localparam output_delay_5 = 4'b1000;

logic empty;
logic [146:0] d_out;
logic rd_en;
logic instruction_ack_d, instruction_ack_2d;
logic [2:0] counter;
logic ack_done;
logic [3:0] output_handshake_state;

always @(posedge clk) begin
    instruction_ack_d <= instruction_ack;
    instruction_ack_2d <= instruction_ack_d;
end

assign ack_done = instruction_ack_2d && (!instruction_ack_d);

always @(posedge clk) begin
    if(counter!=3'd5) counter <= ack_done ? counter + 1'b1 : counter;
    else counter <= 3'd0;
end

instruction_fifo instruction_fifo
    (
    .clk(clk),
    .srst(rst),
    .wr_en(instruction_valid),
    .din(instruction),
    .full(full),
    .rd_en(rd_en),
    .dout(d_out),
    .empty(empty)
    );

always @(posedge clk) begin
    if(rst) begin
        output_handshake_state <= output_idle;
        instruction_req <= '0;
        instruction_chunked <= '0;
    end
    else begin
        case(output_handshake_state)
            output_idle : begin
                if(!empty) output_handshake_state <= output_read;
                else output_handshake_state <= output_idle;
            end
            output_read : begin
                output_handshake_state <= output_read_delay;
                rd_en <= '1;
            end
            output_read_delay : begin
                output_handshake_state <= output_req;
                rd_en <= '0;
            end
            output_req : begin
                instruction_req <= '1;
                case(counter)
                    3'd0 : begin
                        output_handshake_state <= output_delay_1;
                        instruction_chunked <= {13'd0,d_out[146:128]};
                    end
                    3'd1 : begin
                        output_handshake_state <= output_delay_2;
                        instruction_chunked <= d_out [127:96];
                    end
                    3'd2 : begin
                        output_handshake_state <= output_delay_3;
                        instruction_chunked <= d_out [95:64];
                    end
                    3'd3 : begin
                        output_handshake_state <= output_delay_4;
                        instruction_chunked <= d_out [63:32];
                    end
                    3'd4 : begin
                        output_handshake_state <= output_delay_5;
                        instruction_chunked <= d_out [31:0];
                    end
                    default : begin
                        output_handshake_state <= output_req;
                        instruction_chunked <= 32'd0;
                    end
                endcase // counter
            end
            output_delay_1 : begin
                if(instruction_ack_2d) begin
                    output_handshake_state <= ack_done ? output_req : output_delay_1;
                    instruction_req <= '0;
                end
                else begin
                    output_handshake_state <= output_delay_1;
                    instruction_req <= '1;
                end
            end
            output_delay_2 : begin
                if(instruction_ack_2d) begin
                    output_handshake_state <= ack_done ? output_req : output_delay_2;
                    instruction_req <= '0;
                end
                else begin
                    output_handshake_state <= output_delay_2;
                    instruction_req <= '1;
                end
            end
            output_delay_3 : begin
                if(instruction_ack_2d) begin
                    output_handshake_state <= ack_done ? output_req : output_delay_3;
                    instruction_req <= '0;
                end
                else begin
                    output_handshake_state <= output_delay_3;
                    instruction_req <= '1;
                end
            end
            output_delay_4 : begin
                if(instruction_ack_2d) begin
                    output_handshake_state <= ack_done ? output_req : output_delay_4;
                    instruction_req <= '0;
                end
                else begin
                    output_handshake_state <= output_delay_4;
                    instruction_req <= '1;
                end
            end
            output_delay_5 : begin
                if(instruction_ack_2d) begin
                    output_handshake_state <= ack_done ? output_idle : output_delay_5;
                    instruction_req <= '0;
                end
                else begin
                    output_handshake_state <= output_delay_5;
                    instruction_req <= '1;
                end
            end
            default : begin
                output_handshake_state <= output_idle;
            end
        endcase // output_handshake_state
    end
end

initial begin
    instruction_ack_d = '0;
    instruction_ack_2d = '0;
    counter = '0;
    output_handshake_state = output_idle;
    rd_en = '0;
    instruction_req = '0;
    instruction_chunked = '0;
end

endmodule : FPGA_instruction_handshake
