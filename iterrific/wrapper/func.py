import re
from math import exp, cos, sin, tan, atan, log, log10, sqrt, acos, asin
from iterrific.wrapper import LbdWrapper
from iterrific.wrapper.lbd import PartialWrapper


Function = LbdWrapper()
Partial = PartialWrapper()

Exp = Function[exp]
Cos = Function[cos]
Sin = Function[sin]
Tan = Function[tan]
Ln = Function[log]
Log = Function[log10]
Sqrt = Function[sqrt]

ArcTan = Function[atan]
ArcCos = Function[acos]
ArcSin = Function[asin]

Match = Partial[re.match]
Search = Partial[re.search]
