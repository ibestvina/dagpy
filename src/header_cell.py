from IPython.display import display_javascript
def start_new_dagpy_block():
    header_code = """### Block_id\\n\\n##### Description\\n\\n##### Parents\\n\\n##### Filter\\n\\n##### File\\n"""
    display_javascript("""var t_cell = IPython.notebook.get_selected_cell()
    var t_index  = IPython.notebook.get_cells().indexOf(t_cell)-1
    var t_cell = IPython.notebook.get_cell(t_index)
    t_cell.set_text("{header_code}");
    t_cell.metadata = {{"dagpy": {{"cell_type": "delimiter"}}}};
    IPython.notebook.to_markdown(t_index);
    IPython.notebook.get_cell(t_index).render();""".format(header_code = header_code), raw=True)
