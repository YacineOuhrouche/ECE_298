/*
 * Copyright (c) 2026 Yacine Ouhrouche
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_counter (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // Bidirectional pins: input path
    output wire [7:0] uio_out,  // Bidirectional pins: output path
    output wire [7:0] uio_oe,   // Bidirectional pins: output enable
    input  wire       ena,
    input  wire       clk,
    input  wire       rst_n
);

  reg [7:0] count;

  // Asynchronous reset and synchronous load
  always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
      count <= 8'b00000000;
    else if (ui_in[0])
      count <= uio_in;
    else
      count <= count + 8'd1;
  end

  // Dedicated outputs are unused
  assign uo_out = 8'b00000000;

  // Counter value on the bidirectional bus
  assign uio_out = count;

  // ui_in[1] = output enable
  // Disable output automatically while loading
  assign uio_oe = {8{ui_in[1] & ~ui_in[0]}};

  // Unused inputs
  wire _unused = &{ena, ui_in[7:2], 1'b0};

endmodule
