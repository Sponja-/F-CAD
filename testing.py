from elements import *
from arithmetic import *
from algebra import *
from logic import *
from set_theory import *
from constants import *
from flow_control import *
from iterable import *
from special_functions import *
from statements import *
from objects import *

ClassDefinition("complex", None, {
	"constructor": Function(["real", "imag"], StatementList([
			AbsoluteAssignment(AccessMember(Variable("this"), "real"), Variable("real")),
			AbsoluteAssignment(AccessMember(Variable("this"), "imag"), Variable("imag"))
		])),
	"get_imag": Function([], StatementList([
			Return(AccessMember(Variable("this"), "imag"))
		]))
	}).eval()
AbsoluteAssignment(Variable("a"), CreateInstance("complex", Number(10), Number(20))).eval()
print(AccessMember(Variable("a"), "imag").eval())
AbsoluteAssignment(Variable("b"), CreateInstance("complex", Number(10), Number(10))).eval()
print(AccessMember(Variable("b"), "imag").eval())
print(Addition(AccessMember(Variable("b"), "imag"), AccessMember(Variable("a"), "imag")).eval())
AbsoluteAssignment(AccessMember(Variable("a"), "real"), Number(20)).eval()
print(AccessMember(Variable("a"), "real").eval(), AccessMember(Variable("b"), "real").eval())
print(MethodCall(Variable("a"), AccessMember(Variable("a"), "get_imag")).eval())