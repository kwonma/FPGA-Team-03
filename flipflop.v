module ff(input s, r,
		  output reg q);
		  
	always @(s)
		begin
			if(s) q = 1;
			else  q = 0;
		end 

endmodule		