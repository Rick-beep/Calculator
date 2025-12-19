import ast
import operator as op

# mencatung mana operasi yang hanya bisa di gunakan
ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

# Tree walker untuk navigasi node
def safe_eval(operasi):
    tree = ast.parse(operasi , mode="eval").body
    
    def node_eval(node):
        # ast.Sum di hapus di py 3.14, saya gunakan ast.constants sebagai pengganti
        if isinstance(node, ast.Constant): 
            return node.value
        
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in ALLOWED_OPS:
                raise TypeError("Operasi tidak valid")
        
            left = node_eval(node.left)
            right = node_eval(node.right)
            
            if isinstance(node.op, ast.Pow) and abs(right > 100):
                raise ValueError("Exponent terlalu besar")
            
            return ALLOWED_OPS[type(node.op)](left, right)
        
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in ALLOWED_OPS:
                raise TypeError("Operasi tidak valid")
            
            return ALLOWED_OPS[type(node.op)](node_eval(node.operand))
        else:
            raise TypeError("Expression berisi kode illegal")

    if "/ 0" in operasi:
        raise ZeroDivisionError
    
    print(ast.dump(tree, indent=4))
    return node_eval(tree)
        
        
if __name__ == "__main__":
    k = safe_eval("20+(-20**20)")
    print(k)
