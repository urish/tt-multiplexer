/*
 * tt_prim_buf.v
 *
 * TT Primitive
 * Buffer
 *
 * Author: Sylvain Munaut <tnt@246tNt.com>
 */

`default_nettype none

module tt_prim_buf #(
	parameter integer HIGH_DRIVE = 0
)(
	input  wire a,
	output wire z
);

	generate
		if (HIGH_DRIVE) begin
			sky130_fd_sc_hd__buf_8 cell0_I (
`ifdef WITH_POWER
				.VPWR (1'b1),
				.VGND (1'b0),
				.VPB  (1'b1),
				.VNB  (1'b0),
`endif
				.A (a),
				.X (z)
			);
		end else begin
			sky130_fd_sc_hd__buf_2 cell0_I (
`ifdef WITH_POWER
				.VPWR (1'b1),
				.VGND (1'b0),
				.VPB  (1'b1),
				.VNB  (1'b0),
`endif
				.A (a),
				.X (z)
			);
		end
	endgenerate

endmodule // tt_prim_buf
