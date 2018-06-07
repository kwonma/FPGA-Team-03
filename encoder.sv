module snes_encoder (
	input logic clock,
	input logic reset,
	input logic load,
	input logic [N-1:0] d,
	output logic snes_output
	);

logic[N-1:0] q;

always_ff(posedge clk, posedge reset)
	if (reset)
		q <= 0;
	else if (load)
		q <= d;
	else
		q <= {1, q[N-1:1]};
		
assign snes_out = q[0];

endmodule