import ast
import inspect
from typing import Dict, List

def get_ast_node_types():
    """Return all AST node classes in the ast module."""
    types = []
    for name, obj in inspect.getmembers(ast):
        if inspect.isclass(obj) and issubclass(obj, ast.AST):
            doc = getattr(obj, "__doc__", None)
            if doc and ("deprecated" in doc.lower()):
                print(obj, obj.__doc__)
            else:
                types.append(obj)
    return types


def classify_fields(node_cls):
    """Classify each field of a node as primitive or AST-node."""
    primitive_fields: List[str] = []
    node_fields: List[str] = []

    # Instantiate a dummy node only if possible
    # (Some nodes require arguments; use fallback for those)
    try:
        node = node_cls()
    except Exception:
        # Fallback: use field names only
        fields = getattr(node_cls, "_fields", ())
        # Without instance values we cannot distinguish primitives reliably
        # So we assume every field *might* be a node — fix using AST docs
        try:
            node = node_cls(**{f: None for f in fields})
        except Exception:
            return {"primitive_fields": [], "node_fields": list(fields)}

    for field_name in getattr(node_cls, "_fields", []):
        value = getattr(node, field_name, None)

        if isinstance(value, ast.AST):
            node_fields.append(field_name)
        elif isinstance(value, list):
            # list may contain nodes or primitives
            # we classify list as "node field" only if it *can* contain nodes
            if any(isinstance(x, ast.AST) for x in value):
                node_fields.append(field_name)
            else:
                primitive_fields.append(field_name)
        else:
            primitive_fields.append(field_name)

    return {
        "primitive_fields": primitive_fields,
        "node_fields": node_fields,
    }


def build_node_field_map() -> Dict[str, Dict[str, List[str]]]:
    """Create a mapping: node_name → {primitive_fields, node_fields}"""
    mapping = {}
    for cls in get_ast_node_types():
        mapping[cls.__name__] = classify_fields(cls)
    return mapping


if __name__ == "__main__":
    from pprint import pprint
    field_map = build_node_field_map()
    pprint(field_map)