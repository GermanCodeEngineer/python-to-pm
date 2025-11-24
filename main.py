import pmp_manip
from pmp_manip.utility.decorators import grepr_dataclass
import dataclasses
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

@grepr_dataclass(grepr_fields=["type", "children", "fields"])
class Node:
    type: str
    children: dataclasses.field(default_factory=dict) # dict: field_name -> Node or list of Nodes
    fields: dataclasses.field(default_factory=dict) # simple values (strings, numbers, None)


def convert(node):
    """Convert Python AST nodes into custom Node objects."""
    if isinstance(node, ast.AST):
        children = {}
        fields = {}

        for field_name, value in ast.iter_fields(node):

            # Case 1: list of child AST nodes
            if isinstance(value, list):
                child_list = []
                for item in value:
                    if isinstance(item, ast.AST):
                        child_list.append(convert(item))
                    else:
                        # Non-AST primitives inside lists
                        child_list.append(Node("Literal", fields={"value": item}))
                children[field_name] = child_list

            # Case 2: single child AST node
            elif isinstance(value, ast.AST):
                children[field_name] = convert(value)

            # Case 3: primitive field (id, name, number, None...)
            else:
                fields[field_name] = value

        return Node(type(node).__name__, children=children, fields=fields)

    else:
        # Literal fallback (numbers, strings, None)
        return Node(type="Literal", fields={"value": node})

class Visitor(ast.NodeVisitor):
    ...
    ###def visit_AST(self, node):
    #def visit_Add(self, node):
    #def visit_And(self, node):
    #def visit_AnnAssign(self, node):
    #def visit_Assert(self, node):
    #def visit_Assign(self, node):
    #def visit_AsyncFor(self, node):
    #def visit_AsyncFunctionDef(self, node):
    #def visit_AsyncWith(self, node):
    #def visit_Attribute(self, node):
    #def visit_AugAssign(self, node):
    #def visit_Await(self, node):
    #def visit_BinOp(self, node):
    #def visit_BitAnd(self, node):
    #def visit_BitOr(self, node):
    #def visit_BitXor(self, node):
    #def visit_BoolOp(self, node):
    #def visit_Break(self, node):
    #def visit_Call(self, node):
    #def visit_ClassDef(self, node):
    #def visit_Compare(self, node):
    #def visit_Constant(self, node):
    #def visit_Continue(self, node):
    #def visit_Del(self, node):
    #def visit_Delete(self, node):
    #def visit_Dict(self, node):
    #def visit_DictComp(self, node):
    #def visit_Div(self, node):
    #def visit_Eq(self, node):
    #def visit_ExceptHandler(self, node):
    #def visit_Expr(self, node):
    #def visit_Expression(self, node):
    #def visit_FloorDiv(self, node):
    #def visit_For(self, node):
    #def visit_FormattedValue(self, node):
    #def visit_FunctionDef(self, node):
    #def visit_FunctionType(self, node):
    #def visit_GeneratorExp(self, node):
    #def visit_Global(self, node):
    #def visit_Gt(self, node):
    #def visit_GtE(self, node):
    #def visit_If(self, node):
    #def visit_IfExp(self, node):
    #def visit_Import(self, node):
    #def visit_ImportFrom(self, node):
    #def visit_In(self, node):
    #def visit_Interactive(self, node):
    #def visit_Invert(self, node):
    #def visit_Is(self, node):
    #def visit_IsNot(self, node):
    #def visit_JoinedStr(self, node):
    #def visit_LShift(self, node):
    #def visit_Lambda(self, node):
    #def visit_List(self, node):
    #def visit_ListComp(self, node):
    #def visit_Load(self, node):
    #def visit_Lt(self, node):
    #def visit_LtE(self, node):
    #def visit_MatMult(self, node):
    #def visit_Match(self, node):
    #def visit_MatchAs(self, node):
    #def visit_MatchClass(self, node):
    #def visit_MatchMapping(self, node):
    #def visit_MatchOr(self, node):
    #def visit_MatchSequence(self, node):
    #def visit_MatchSingleton(self, node):
    #def visit_MatchStar(self, node):
    #def visit_MatchValue(self, node):
    #def visit_Mod(self, node):
    #def visit_Module(self, node):
    #def visit_Mult(self, node):
    #def visit_Name(self, node):
    #def visit_NamedExpr(self, node):
    #def visit_Nonlocal(self, node):
    #def visit_Not(self, node):
    #def visit_NotEq(self, node):
    #def visit_NotIn(self, node):
    #def visit_Or(self, node):
    #def visit_ParamSpec(self, node):
    #def visit_Pass(self, node):
    #def visit_Pow(self, node):
    #def visit_RShift(self, node):
    #def visit_Raise(self, node):
    #def visit_Return(self, node):
    #def visit_Set(self, node):
    #def visit_SetComp(self, node):
    #def visit_Slice(self, node):
    #def visit_Starred(self, node):
    #def visit_Store(self, node):
    #def visit_Sub(self, node):
    #def visit_Subscript(self, node):
    #def visit_Try(self, node):
    #def visit_TryStar(self, node):
    #def visit_Tuple(self, node):
    #def visit_TypeAlias(self, node):
    #def visit_TypeIgnore(self, node):
    #def visit_TypeVar(self, node):
    #def visit_TypeVarTuple(self, node):
    #def visit_UAdd(self, node):
    #def visit_USub(self, node):
    #def visit_UnaryOp(self, node):
    #def visit_While(self, node):
    #def visit_With(self, node):
    #def visit_Yield(self, node):
    #def visit_YieldFrom(self, node):
    #def visit__ast_Ellipsis(self, node):
    #def visit_alias(self, node):
    #def visit_arg(self, node):
    #def visit_arguments(self, node):
    #def visit_boolop(self, node):
    #def visit_cmpop(self, node):
    #def visit_comprehension(self, node):
    #def visit_excepthandler(self, node):
    ###def visit_expr(self, node):
    #def visit_expr_context(self, node):
    #def visit_keyword(self, node):
    #def visit_match_case(self, node):
    ###def visit_mod(self, node):
    #def visit_operator(self, node):
    ###def visit_pattern(self, node):
    ###def visit_stmt(self, node):
    #def visit_type_ignore(self, node):
    #def visit_type_param(self, node):
    #def visit_unaryop(self, node):
    #def visit_withitem(self, node):

def walk_node(node: ast.AST) -> None:
    def _walk_nodes(nodes: list[ast.AST]):
        [walk_node(node) for node in nodes]
    
    for field in node._fields:
        value = getattr(node, field)
        match field:
            case "body": _walk_nodes(value)
            case "targets": _walk_nodes(value)
            case "id" | "ctx": pass
            case "value":
                if not isinstance(node, ast.Constant):
                    walk_node(value)
            case _: raise Exception(f"Unknown node field: {field} on {type(node)}")    

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
    code = "x = a + b"
    module = ast.parse(code)
    print(ast.dump(module, indent=4))
    #walk_node(module)
    
    converted = convert(module)
    print(converted)
