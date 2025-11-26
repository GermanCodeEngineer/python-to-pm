from __future__ import annotations
import pmp_manip
from pmp_manip.utility import grepr_dataclass, AbstractTreePath
import dataclasses
import ast

@grepr_dataclass(grepr_fields=["type", "children", "fields"])
class Node:
    type: type[ast.AST]
    path: AbstractTreePath # Path from origin
    parent_nodes: list[Node]
    fields: dataclasses.field(default_factory=dict)
    
    @property
    def primitive_fields(self) -> dict[str, Any]: # TODO: define primitives typevar
        return {field: self.fields[field] for field in NodeTypes[self.type].primitive}

    @property
    def node_fields(self) -> dict[str, Any]: # TODO: add narrow typing
        return {field: self.fields[field] for field in NodeTypes[self.type].node}
    
    
    @staticmethod
    def from_simple(node: ast.AST, path: AbstractTreePath, parent_nodes: list["Node"]):
        return Node(
            type=type(node),
            path=path,
            parent_nodes=parent_nodes,
            fields=ast.iter_fields(...!)
        )

@grepr_dataclass(grepr_fields=["primitive", "node"])
class ASTTypeInfo:
    primitive: list[str]
    node: list[str]

NodeTypes = {
    ast.Add: ASTTypeInfo(primitive=[], node=[]),
    ast.And: ASTTypeInfo(primitive=[], node=[]),
    ast.AnnAssign: ASTTypeInfo(primitive=["simple"], node=["target", "annotation", "value"]),
    ast.Assert: ASTTypeInfo(primitive=[], node=["test", "msg"]),
    ast.Assign: ASTTypeInfo(primitive=["type_comment"], node=["targets", "value"]),
    ast.AsyncFor: ASTTypeInfo(primitive=["type_comment"], node=["target", "iter", "body", "orelse"]),
    ast.AsyncFunctionDef: ASTTypeInfo(primitive=["name", "type_comment"], node=["args", "body", "decorator_list", "returns", "type_params"]),
    ast.AsyncWith: ASTTypeInfo(primitive=["type_comment"], node=["items", "body"]),
    ast.Attribute: ASTTypeInfo(primitive=["attr"], node=["value", "ctx"]),
    ast.AugAssign: ASTTypeInfo(primitive=[], node=["target", "op", "value"]),
    ast.Await: ASTTypeInfo(primitive=[], node=["value"]),
    ast.BinOp: ASTTypeInfo(primitive=[], node=["left", "op", "right"]),
    ast.BitAnd: ASTTypeInfo(primitive=[], node=[]),
    ast.BitOr: ASTTypeInfo(primitive=[], node=[]),
    ast.BitXor: ASTTypeInfo(primitive=[], node=[]),
    ast.BoolOp: ASTTypeInfo(primitive=[], node=["op", "values"]),
    ast.Break: ASTTypeInfo(primitive=[], node=[]),
    ast.Call: ASTTypeInfo(primitive=[], node=["func", "args", "keywords"]),
    ast.ClassDef: ASTTypeInfo(primitive=["name"], node=["bases", "keywords", "body", "decorator_list", "type_params"]),
    ast.Compare: ASTTypeInfo(primitive=[], node=["left", "ops", "comparators"]),
    ast.Constant: ASTTypeInfo(primitive=["value", "kind"], node=[]),
    ast.Continue: ASTTypeInfo(primitive=[], node=[]),
    ast.Del: ASTTypeInfo(primitive=[], node=[]),
    ast.Delete: ASTTypeInfo(primitive=[], node=["targets"]),                                                                     ast.Dict: ASTTypeInfo(primitive=[], node=["keys", "values"]),
    ast.DictComp: ASTTypeInfo(primitive=[], node=["key", "value", "generators"]),
    ast.Div: ASTTypeInfo(primitive=[], node=[]),
    ast.Eq: ASTTypeInfo(primitive=[], node=[]),
    ast.ExceptHandler: ASTTypeInfo(primitive=["name"], node=["type", "body"]),
    ast.Expr: ASTTypeInfo(primitive=[], node=["value"]),
    ast.Expression: ASTTypeInfo(primitive=[], node=["body"]),
    ast.FloorDiv: ASTTypeInfo(primitive=[], node=[]),
    ast.For: ASTTypeInfo(primitive=["type_comment"], node=["target", "iter", "body", "orelse"]),
    ast.FormattedValue: ASTTypeInfo(primitive=["conversion"], node=["value", "format_spec"]),
    ast.FunctionDef: ASTTypeInfo(primitive=["name", "type_comment"], node=["args", "body", "decorator_list", "returns", "type_params"]),
    ast.FunctionType: ASTTypeInfo(primitive=[], node=["argtypes", "returns"]),
    ast.GeneratorExp: ASTTypeInfo(primitive=[], node=["elt", "generators"]),
    ast.Global: ASTTypeInfo(primitive=["names"], node=[]),
    ast.Gt: ASTTypeInfo(primitive=[], node=[]),
    ast.GtE: ASTTypeInfo(primitive=[], node=[]),
    ast.If: ASTTypeInfo(primitive=[], node=["test", "body", "orelse"]),
    ast.IfExp: ASTTypeInfo(primitive=[], node=["test", "body", "orelse"]),
    ast.Import: ASTTypeInfo(primitive=[], node=["names"]),
    ast.ImportFrom: ASTTypeInfo(primitive=["module", "level"], node=["names"]),
    ast.In: ASTTypeInfo(primitive=[], node=[]),
    ast.Interactive: ASTTypeInfo(primitive=[], node=["body"]),
    ast.Invert: ASTTypeInfo(primitive=[], node=[]),
    ast.Is: ASTTypeInfo(primitive=[], node=[]),
    ast.IsNot: ASTTypeInfo(primitive=[], node=[]),
    ast.JoinedStr: ASTTypeInfo(primitive=[], node=["values"]),
    ast.LShift: ASTTypeInfo(primitive=[], node=[]),
    ast.Lambda: ASTTypeInfo(primitive=[], node=["args", "body"]),
    ast.List: ASTTypeInfo(primitive=[], node=["elts", "ctx"]),
    ast.ListComp: ASTTypeInfo(primitive=[], node=["elt", "generators"]),
    ast.Load: ASTTypeInfo(primitive=[], node=[]),
    ast.Lt: ASTTypeInfo(primitive=[], node=[]),
    ast.LtE: ASTTypeInfo(primitive=[], node=[]),
    ast.MatMult: ASTTypeInfo(primitive=[], node=[]),
    ast.Match: ASTTypeInfo(primitive=[], node=["subject", "cases"]),
    ast.MatchAs: ASTTypeInfo(primitive=["name"], node=["pattern"]),
    ast.MatchClass: ASTTypeInfo(primitive=["kwd_attrs"], node=["cls", "patterns", "kwd_patterns"]),
    ast.MatchMapping: ASTTypeInfo(primitive=["rest"], node=["keys", "patterns"]),
    ast.MatchOr: ASTTypeInfo(primitive=[], node=["patterns"]),
    ast.MatchSequence: ASTTypeInfo(primitive=[], node=["patterns"]),
    ast.MatchSingleton: ASTTypeInfo(primitive=["value"], node=[]),
    ast.MatchStar: ASTTypeInfo(primitive=["name"], node=[]),
    ast.MatchValue: ASTTypeInfo(primitive=[], node=["value"]),
    ast.Mod: ASTTypeInfo(primitive=[], node=[]),
    ast.Module: ASTTypeInfo(primitive=[], node=["body", "type_ignores"]),
    ast.Mult: ASTTypeInfo(primitive=[], node=[]),
    ast.Name: ASTTypeInfo(primitive=["id"], node=["ctx"]),
    ast.NamedExpr: ASTTypeInfo(primitive=[], node=["target", "value"]),
    ast.Nonlocal: ASTTypeInfo(primitive=["names"], node=[]),
    ast.Not: ASTTypeInfo(primitive=[], node=[]),
    ast.NotEq: ASTTypeInfo(primitive=[], node=[]),
    ast.NotIn: ASTTypeInfo(primitive=[], node=[]),
    ast.Or: ASTTypeInfo(primitive=[], node=[]),
    ast.ParamSpec: ASTTypeInfo(primitive=["name"], node=[]),
    ast.Pass: ASTTypeInfo(primitive=[], node=[]),
    ast.Pow: ASTTypeInfo(primitive=[], node=[]),
    ast.RShift: ASTTypeInfo(primitive=[], node=[]),
    ast.Raise: ASTTypeInfo(primitive=[], node=["exc", "cause"]),
    ast.Return: ASTTypeInfo(primitive=[], node=["value"]),
    ast.Set: ASTTypeInfo(primitive=[], node=["elts"]),
    ast.SetComp: ASTTypeInfo(primitive=[], node=["elt", "generators"]),
    ast.Slice: ASTTypeInfo(primitive=[], node=["lower", "upper", "step"]),
    ast.Starred: ASTTypeInfo(primitive=[], node=["value", "ctx"]),
    ast.Store: ASTTypeInfo(primitive=[], node=[]),
    ast.Sub: ASTTypeInfo(primitive=[], node=[]),
    ast.Subscript: ASTTypeInfo(primitive=[], node=["value", "slice", "ctx"]),
    ast.Try: ASTTypeInfo(primitive=[], node=["body", "handlers", "orelse", "finalbody"]),
    ast.TryStar: ASTTypeInfo(primitive=[], node=["body", "handlers", "orelse", "finalbody"]),
    ast.Tuple: ASTTypeInfo(primitive=[], node=["elts", "ctx"]),
    ast.TypeAlias: ASTTypeInfo(primitive=["name"], node=["type_params", "value"]),
    ast.TypeIgnore: ASTTypeInfo(primitive=["lineno", "tag"], node=[]),
    ast.TypeVar: ASTTypeInfo(primitive=["name"], node=["bound"]),
    ast.TypeVarTuple: ASTTypeInfo(primitive=["name"], node=[]),
    ast.UAdd: ASTTypeInfo(primitive=[], node=[]),
    ast.USub: ASTTypeInfo(primitive=[], node=[]),
    ast.UnaryOp: ASTTypeInfo(primitive=[], node=["op", "operand"]),
    ast.While: ASTTypeInfo(primitive=[], node=["test", "body", "orelse"]),
    ast.With: ASTTypeInfo(primitive=["type_comment"], node=["items", "body"]),
    ast.Yield: ASTTypeInfo(primitive=[], node=["value"]),
    ast.YieldFrom: ASTTypeInfo(primitive=[], node=["value"]),
    ast.alias: ASTTypeInfo(primitive=["name", "asname"], node=[]),
    ast.arg: ASTTypeInfo(primitive=["arg", "type_comment"], node=["annotation"]),
    ast.arguments: ASTTypeInfo(primitive=[], node=["posonlyargs", "args", "vararg", "kwonlyargs", "kw_defaults", "kwarg", "defaults"]),
    ast.comprehension: ASTTypeInfo(primitive=["is_async"], node=["target", "iter", "ifs"]),
    ast.keyword: ASTTypeInfo(primitive=["arg"], node=["value"]),
    ast.match_case: ASTTypeInfo(primitive=[], node=["pattern", "guard", "body"]),
    ast.withitem: ASTTypeInfo(primitive=[], node=["context_expr", "optional_vars"]),
}

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
    code = "x = a + b"
    module = ast.parse(code)
    print(ast.dump(module, indent=4))
    #walk_node(module)
    
    converted = convert(module)
    print(converted)
