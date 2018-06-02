module compare #(parameter N=4)
				(input [3:0] a,
				output reg result);
	
	assign result = (a > N);
	
endmodule