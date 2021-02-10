def count_votes(reactions):
    """
    takes in a string with reactions from discord
    parses it and return a tuple of the toal votes on each alternative
    """
    positive_vote = "👍"
    negative_vote = "👎"
    alternatives = [positive_vote, negative_vote]
    results={}

    for a in alternatives:
        position = reactions.find(a) + 17
        votes= reactions[position:position+2]
        if votes[-1] == ">": votes = votes[:-1]
        results[a] = votes

    return (results[positive_vote], results[negative_vote])

def net_score(results):
    """
    takes in a results tuple and returns net score after a substraction
    """
    if type(results) != tuple: raise TypeError
    return int(results[0]) - int(results[1])