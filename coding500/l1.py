import re

keywords = {
    "V": "r",
    "B": "b",
    "N": "",
}


def eval_exp(stack: list[str]) -> str | int | None:
    ar_ops = ["MUL", "ADD", "DIV", "SUB"]
    bin_ops = ["QE", "EN", "EL", "EG", "TG", "TL"]
    if stack:
        exp = stack.pop()
    else:
        return None
    # print(f"EXP: {exp}")

    if exp == "P":
        # print(f"PRINT: {str(eval_exp(stack))}")
        print(str(eval_exp(stack)), end="")

    elif exp == "BOH" or exp == "OH":
        sep = ""
        conds: list[str] = []
        rhs: list[str | int | None] = []
        lhs: list[str | int | None] = []
        joins: list[str] = []
        while sep != "|":
            conds.insert(0, stack.pop())
            rhs.insert(0, eval_exp(stack))
            lhs.insert(0, eval_exp(stack))
            sep = stack.pop()
            if sep != "|":
                joins.insert(0, sep)

        truth = False
        for i, cond in enumerate(reversed(conds)):
            lh = lhs.pop()
            rh = rhs.pop()
            join = joins.pop() if joins and i > 0 else None
            ltruth = False
            if cond == "QE":
                ltruth = lh == rh
            elif cond == "EN":
                ltruth = lh != rh
            elif isinstance(lh, int) and isinstance(rh, int):
                if cond == "EL":
                    ltruth = lh <= rh
                elif cond == "EG":
                    ltruth = lh >= rh
                elif cond == "TG":
                    ltruth = lh > rh
                elif cond == "TL":
                    ltruth = lh < rh
            if join:
                if join == "OR":
                    truth = truth or ltruth
                elif join == "AND":
                    truth = truth and ltruth
            else:
                truth = ltruth

        inst_stack: list[str] = []
        alt_stack: list[str] = []

        inst = ""
        counter = 0
        # print(f"STACk: {stack}")
        while True:
            inst = stack.pop()
            if inst == "BOH":
                counter += 1
            if counter > 0:
                inst_stack.insert(0, inst)
                if inst == "HOB":
                    counter -= 1
            elif counter == 0:
                if inst == "HOB" or inst == "HO":
                    break
                if inst == "OH":
                    alt_counter = 0
                    alt_stack.insert(0, inst)
                    alt_inst = ""
                    while True:
                        alt_inst = stack.pop()
                        alt_stack.insert(0, alt_inst)
                        if alt_inst == "HO" and alt_counter == 0:
                            break
                        if alt_inst == "OH":
                            alt_counter += 1
                        elif alt_inst == "HO":
                            alt_counter -= 1
                else:
                    inst_stack.insert(0, inst)
        # print(f"INST_STACk: {inst_stack}")
        # print(f"ALT_STACk: {alt_stack}")
        if truth:
            while inst_stack:
                eval_exp(inst_stack)
        else:
            while alt_stack:
                eval_exp(alt_stack)

    elif exp == "LOOP":
        cond_stack: list[str] = []
        inst = stack.pop()
        inst_stack = []
        while inst != "|":
            cond_stack.insert(0, inst)
            inst = stack.pop()
        inst = stack.pop()
        count = 0
        while True:
            if count == 0 and inst == "POOL":
                break
            if inst == "LOOP":
                count += 1
            elif inst == "POOL":
                count -= 1
            inst_stack.insert(0, inst)
            inst = stack.pop()

        # print(f"COND_STACK: {cond_stack}")
        # print(f"INST_STACK: {inst_stack}")

        while True:
            truth = bool(eval_exp(cond_stack.copy()))
            if not truth:
                break
            inst_stack_copy = inst_stack.copy()
            while inst_stack_copy:
                eval_exp(inst_stack_copy)

    elif exp in bin_ops:
        rh = eval_exp(stack)
        lh = eval_exp(stack)

        tvalue = None

        if exp == "QE":
            tvalue = lh == rh
        elif exp == "EN":
            tvalue = lh != rh
        if isinstance(lh, int) and isinstance(rh, int):
            if exp == "LE":
                tvalue = lh <= rh
            elif exp == "EG":
                tvalue = lh >= rh
            elif exp == "TG":
                tvalue = lh > rh
            elif exp == "TL":
                tvalue = lh < rh

        return tvalue

    elif exp.startswith("B"):
        return exp[-2::-2]

    elif exp.startswith("V"):
        name = exp[1:-1:2]
        if exp.endswith("="):
            value = eval_exp(stack)
            if value is not None:
                variables[name] = value
        else:
            return variables[name]

    elif exp.startswith("N"):
        split = re.split(r"(?<=[0-9])(?=[a-zZ])|(?<=[a-zZ])(?=[0-9])", exp[1:])
        values = split[::2]
        ops = split[1::2]

        value = int(values[0])
        for op, val in zip(ops, values[1:]):
            if op == "a":
                value += int(val)
            elif op == "s":
                value -= int(val)
            elif op == "m":
                value *= int(val)
            elif op == "d":
                value //= int(val)
        return value

    elif exp in ar_ops:
        b = eval_exp(stack)
        a = eval_exp(stack)
        a_type = type(a)
        b_type = type(b)

        if a_type != b_type:
            return None

        if isinstance(a, int) and isinstance(b, int):
            if exp == "MUL":
                return a * b
            elif exp == "ADD":
                return a + b
            elif exp == "DIV":
                return a // b
            elif exp == "SUB":
                return a - b
        elif isinstance(a, str) and isinstance(b, str):
            return "".join([a, b])
        else:
            return None
    else:
        raise Exception(f"Invalid expression: {exp}")

    return None


variables: dict[str, str | int] = {}
stack: list[str] = []

file = "./coding500/Level4.txt"
with open(file, "r") as f:
    for i, line in enumerate(f):
        if line.startswith(("//", "\n")):
            continue

        # split where changes from lowercase to uppercase or at spaces, or at any of the ops, whituout removing the op
        split = re.split(r"(?<=[a-z]|[0-9])(?=[A-Z])| |(MUL|ADD|DIV|SUB)", line[:-1])
        # remove none elements or empty string
        split = list(filter(lambda x: x is not None and x != "", split))
        for j, e in enumerate(reversed(split)):
            stack.insert(0, e)

# for inst in stack:
#     print(inst)

while len(stack) > 0:
    eval_exp(stack)

# print(variables)

# l2: 1936anok33ga16wu143102843phlqkkkmwcsw31821_31443137ps9ko3318ut93744299vsb571124022vbboc
# l3:921433450ltnl2324034338jbn621604j179046404987m2tb1840k2116-1346rkcc18oi28znb22av_yz122839om_6x41
