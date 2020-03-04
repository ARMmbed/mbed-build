
class Op:

    def __init__(self):
        self.includes = []
        self.defines = []
        self.flags = []
        self.output_file = None

    def decode_common_args(self, args):
        if arg.startswith("-D"):
            try:
                define_name, define_value = arg[2:].split('=')
            except ValueError:
                define_name = arg[2:]
                define_value = None

            print(f"Define: {define_name} = {define_value}")
            self.defines.append({define_name: define_value})
            return True

        if arg == '-o':
            self.output_file = next(args)
            print(f"Output file: {self.output_file}")
            return True

        return False


class CompileOp(Op):
    def decode_args(self, arg_list):
        args = iter(arg_list)

        while True:
            try:
                arg = next(args)

                if self.decode_common_args(args):
                    continue

                if arg.startswith("-I"):
                    include_file = arg[2:]
                    self.includes.append(include_file)
                    print(f"Include: {include_file}")
                    continue

                if arg == '-c':
                    arg = next(args)
                    print(f"Compile file: {arg}")
                    continue

                if arg == '-include':
                    arg = next(args)
                    print(f"Extra include file: {arg}")
                    continue

                if arg.startswith("-"):
                    flag_value = arg[1:]
                    self.flags.append(flag_value)
                    print(f"Flag: {flag_value}")
                    continue

                print(f"Something else: {arg}")
                continue

            except StopIteration:
                break

class LinkOp(Op):
    def decode_args(self, arg_list):
        args = iter(arg_list)

        while True:
            try:
                arg = next(args)

                if self.decode_common_args(args):
                    continue

                if arg.startswith("-"):
                    flag_value = arg[1:]
                    self.flags.append(flag_value)
                    print(f"Flag: {flag_value}")
                    continue

                print(f"Something else: {arg}")
                continue

            except StopIteration:
                break


op = None

with open("full-trial/build-dir/make-out.txt", "r") as f:
    for line in f:
        parsed_args = []
        for arg in line.split():
            if arg == '/usr/local/gcc-arm-none-eabi-7-2018-q2-update/bin/arm-none-eabi-g++':
                op = CompileOp()
                print("=== Compile ===")
                continue

            if arg == 'arm-none-eabi-cpp':
                op = LinkOp()
                print("=== Link ===")
                continue

            if op:
                parsed_args.append(arg)
            else:
                print(f"Unrecognised '{arg}'")

        if op:
            op.decode_args(parsed_args)

        op = None

