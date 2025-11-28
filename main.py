from __future__ import annotations
import pmp_manip

from node import Node, InstructionList

def configure(gen_opcode_info_dir: str) -> None:
    cfg = pmp_manip.get_default_config()
    cfg.ext_info_gen.gen_opcode_info_dir = gen_opcode_info_dir
    cfg.ext_info_gen.is_trusted_extension_origin_handler = lambda source: source.startswith(
        "https://raw.githubusercontent.com/GermanCodeEngineer/PM-Extensions/")
    pmp_manip.init_config(cfg)

def convert_python_to_pm(ast: Node) -> pmp_manip.SRProject:
    project = pmp_manip.SRProject.create_empty()
    project.extensions.append(pmp_manip.SRCustomExtension(
        id="gceClassesOOP",  
        url="https://raw.githubusercontent.com/GermanCodeEngineer/PM-Extensions/refs/heads/main/extensions/classes.js",
    ))
    instructions = ast.to_block().as_instructions()
    project.stage.scripts.append(pmp_manip.SRScript(position=(0,0), blocks=instructions))

    project.add_all_extensions_to_info_api(pmp_manip.info_api)
    print(project)
    project.validate(pmp_manip.info_api)
    return project


if __name__ == "__main__":
    configure("output/gen_opcode_info")
    code = '''
class X:
    5
    "5"
    global hi, opl
'''
    ast = Node.from_code(code)
    print(ast)
    project = convert_python_to_pm(ast)
    frproject = project.to_first(pmp_manip.info_api)
    frproject.to_file("output/generated.pmp")
