import pmp_manip
import ast

CLASS_BEING_CREATED = pmp_manip.SREmbeddedBlockInputValue(
    block=pmp_manip.SRBlock(opcode="&gceClassesOOP::class being created"),
)

def configure(gen_opcode_info_dir: str) -> None:
    cfg = pmp_manip.get_default_config()
    cfg.ext_info_gen.gen_opcode_info_dir = gen_opcode_info_dir
    cfg.ext_info_gen.is_trusted_extension_origin_handler = lambda source: source.startswith(
        "https://raw.githubusercontent.com/GermanCodeEngineer/PM-Extensions/")
    pmp_manip.init_config(cfg)

def convert_python_to_pm() -> pmp_manip.SRProject:
    project = pmp_manip.SRProject.create_empty()
    project.extensions.append(pmp_manip.SRCustomExtension(
        id="gceClassesOOP",  
        url="https://raw.githubusercontent.com/GermanCodeEngineer/PM-Extensions/refs/heads/main/extensions/classes.js",
    ))
    project.stage.scripts.append(pmp_manip.SRScript(
        position=(0, 0),
        blocks=[
            pmp_manip.SRBlock(
                opcode="&gceClassesOOP::create class at (NAME) {:SHADOW:} {SUBSTACK}",
                inputs={
                    "NAME": pmp_manip.SRBlockAndTextInputValue(block=None, immediate="cls"),
                    "SHADOW": CLASS_BEING_CREATED,
                    "SUBSTACK": pmp_manip.SRScriptInputValue(blocks=[]),
                },
            ),
        ],
    ))

    project.add_all_extensions_to_info_api(pmp_manip.info_api)
    print(project)
    project.validate(pmp_manip.info_api)
    return project


if __name__ == "__main__":
    configure("output/gen_opcode_info")
    #project = convert_python_to_pm()
    #frproject = project.to_first(pmp_manip.info_api)
    #frproject.to_file("output/generated.pmp")

    code = """# Program to check if a number is prime or not

num = 29

# To take input from the user
#num = int(input("Enter a number: "))

# define a flag variable
flag = False

if num == 0 or num == 1:
    print(num, "is not a prime number")
elif num > 1:
    # check for factors
    for i in range(2, num):
        if (num % i) == 0:
            # if factor is found, set flag to True
            flag = True
            # break out of loop
            break

    # check if flag is True
    if flag:
        print(num, "is not a prime number")
    else:
        print(num, "is a prime number")"""
    print(ast.dump(ast.parse(code), indent=4))
