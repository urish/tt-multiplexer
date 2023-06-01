#
# OpenDB script for custom IO placement for the TT user blocks
#
# Copyright (c) 2023 Sylvain Munaut <tnt@246tNt.com>
# SPDX-License-Identifier: Apache-2.0
#

import os
import sys

sys.path.append('../../py')
import tt
import tt_odb

import click
sys.path.insert(0, os.path.join(os.environ.get("OPENLANE_ROOT"), "scripts", "odbpy"))
from reader import click_odb


@click.command()
@click_odb
def io_place(
	reader,
):

	# Load TinyTapeout
	tti = tt.TinyTapeout(modules=False)

	# Terminal name mapping
	bterm_map = {b.getName(): b for b in reader.block.getBTerms()}

	# Find die & layers
	die_area = reader.block.getDieArea()
	layer_ns = reader.tech.findLayer(tti.cfg.tt.spine.vlayer)

	# User block bottom
	for pn, pp in tti.layout.ply_block.items():
		tt_odb.place_pin(die_area, layer_ns, bterm_map.pop(pn), pp, 'N')

	sram_ply = [
		('ram_dout0',  32),
		('ram_din0',   32),
		('ram_addr0',  9),
		('ram_wmask0', 4),
		('ram_clk0',   None),
		('ram_csb0',   None),
		('ram_web0',   None),
	]
	sram_ply_e = tti.layout._ply_expand(sram_ply)
	print(sram_ply_e)

	tracks = tti.layout._ply_distribute(
			n_pins = len(sram_ply_e),
			start  = 0,
			end    = tti.layout.glb.block.width.units,
			step   = 0,
			layer  = tti.layout.cfg.tt.spine.vlayer,
			axis   = 'x',
		)

	ply_block = tti.layout._ply_finalize(sram_ply_e, tracks)

	for pn, pp in ply_block.items():
		tt_odb.place_pin(die_area, layer_ns, bterm_map.pop(pn), pp, 'S')


if __name__ == "__main__":
	io_place()
