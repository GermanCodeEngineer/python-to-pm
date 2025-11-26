from __future__ import annotations
import ast
import copy
import dataclasses
from pmp_manip.utility import grepr_dataclass, AbstractTreePath
from typing import Any

@grepr_dataclass(grepr_fields=["type", "children", "primitive_fields", "node_fields"])
class Node:
    type: type[ast.AST]
    path: AbstractTreePath # Path from origin
    parent_nodes: list[Node]
    fields: dict[str, Any] = dataclasses.field(default_factory=dict)
    
    @property
    def primitive_fields(self) -> dict[str, Any]: # TODO: define primitives typevar
        return {field: self.fields[field] for field in NODE_TYPES[self.type].primitive}

    @property
    def node_fields(self) -> dict[str, Any]: # TODO: add narrow typing
        return {field: self.fields[field] for field in NODE_TYPES[self.type].node}
    
    
    @staticmethod
    def from_simple(simple_node: ast.AST, path: AbstractTreePath, parent_nodes: list["Node"]) -> Node:
        node = Node(
            type=type(simple_node),
            path=path,
            parent_nodes=parent_nodes,
            fields={},
        )
        extended_parent_nodes = copy.copy(parent_nodes)
        extended_parent_nodes.append(node)
        fields_path = path.add_attribute("fields")

        for field_name in NODE_TYPES[node.type].primitive:
            node.fields[field_name] = getattr(simple_node, field_name)
        for field_name in NODE_TYPES[node.type].node:
            value = getattr(simple_node, field_name)
            field_path = fields_path.add_index_or_key(field_name)
            if value is None:
                pass  # Keep None as-is
            elif isinstance(value, ast.AST):
                value = Node.from_simple(value, field_path, extended_parent_nodes)
            elif isinstance(value, list):
                value = [
                    Node.from_simple(item, field_path.add_index_or_key(index), extended_parent_nodes)
                    for index, item in enumerate(value)
                ]
            else:
                raise Exception("Unexpected value", value)
            node.fields[field_name] = value
        return node

    @staticmethod
    def from_code(code: str) -> Node:
        module = ast.parse(code)
        return Node.from_simple(module, AbstractTreePath(), [])

@grepr_dataclass(grepr_fields=["primitive", "node"])
class ASTTypeInfo:
    primitive: list[str]
    node: list[str]

NODE_TYPES = {
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


__all__ = ["Node"]
