module multiplexer(
	input [3:0] key_mux,
	input [3:0] ir_mux,
	input [3:0] b_mux,
	input [1:0] dip,
	output logic [8:0] mux_en
	);
	
always_comb	begin
		case(dip)
			0:		mux_en = key_mux;
			1:		mux_en = ir_mux;
			2:		mux_en = b_mux;
		endcase
	end

endmodule