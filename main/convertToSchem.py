from pymsch import Block, Content, Schematic


schem=Schematic()
schem.set_tag('name', "subtitle")
schem.set_tag('description', 'A description for the schematic')
schem.add_block(Block(Content.LOGIC_PROCESSOR, 0, 0, "c2V0IG4gMA0Kc2V0IGxpIDA=", 0))
print(schem.write_str())
