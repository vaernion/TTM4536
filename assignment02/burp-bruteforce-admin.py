def queueRequests(target, wordlists):
    engine = RequestEngine(
        endpoint=target.endpoint,
        concurrentConnections=10,
        requestsPerConnection=100,
        pipeline=False,
    )

    for word in open("megalist_md5.txt"):
        engine.queue(target.req, word)


def handleResponse(req, interesting):
    if interesting or "flag" in req.response.lower():
        # if not "WrongAnswer" in req.response:
        table.add(req)
