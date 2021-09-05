def queueRequests(target, wordlists):
    engine = RequestEngine(
        endpoint=target.endpoint,
        # engine=Engine.BURP,
        concurrentConnections=10,
        requestsPerConnection=10,
        pipeline=False,
    )

    continue_from = 0

    for i, word in enumerate(open("S:/NTNU-large/TTM4536/megalist2.txt")):
        if i < continue_from - 1:
            continue
        word_stripped = word.rstrip()
        print(i, word_stripped)  # look in extension output when pausing
        engine.queue(target.req, word_stripped)


def handleResponse(req, interesting):
    print(req.response)
    # if interesting or not "WrongAnswer" in req.response or "flag" in req.response.lower():
    if (
        len(req.response) != 2742
        or not "WrongAnswer" in req.response
        or "flag" in req.response.lower()
    ):
        table.add(req)
