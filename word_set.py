import sys
import numpy as np
import string
import unicodecsv as csv
import Retrievanator

# Here is the data that LDA spat out
LDA = [{"school", "high", "college", "student", "girl", "students", "teacher", "time", "girls", "professor", "friends",
         "year-old", "begins", "parents", "decides", "friendship", "finds", "end", "year", "learns"},
        {"war", "american", "story", "army", "world", "young", "men", "arts", "british", "forced", "martial", "french",
         "set",
         "america", "forces", "south", "soldiers", "based", "soldier", "france"},
        {"film", "story", "based", "movie", "comedy", "director", "set", "series", "tells", "drama", "book", "stories",
         "tale",
         "life", "american", "sequel", "stars", "directed", "short", "hollywood"},
        {"life", "man", "past", "woman", "death", "story", "events", "lives", "years", "mysterious", "family", "tells",
         "world",
         "young", "accident", "discovers", "face", "fate", "secrets", "boy"},
        {"police", "murder", "killer", "drug", "cop", "detective", "crime", "case", "angeles", "los", "john", "find",
         "serial",
         "fbi", "undercover", "murdered", "partner", "criminal", "city", "investigation"},
        {"father", "family", "mother", "daughter", "son", "life", "home", "wife", "parents", "young", "house",
         "children",
         "boy", "girl", "brother", "year-old", "living", "discovers", "husband", "returns"},
        {"find", "island", "journey", "world", "young", "search", "crew", "ship", "adventure", "back", "friends", "sea",
         "takes", "quest", "deep", "make", "return", "mysterious", "leads", "captain"},
        {"family", "back", "christmas", "time", "home", "it's", "owner", "he's", "good", "summer", "city", "real",
         "put", "day",
         "decides", "live", "big", "can't", "friends", "cat"},
        {"years", "man", "prison", "time", "life", "joe", "ago", "max", "back", "sam", "free", "finally", "attempt",
         "eye",
         "makes", "son", "finds", "order", "bill", "chance"},
        {"world", "earth", "human", "planet", "stop", "alien", "save", "space", "race", "group", "future", "people",
         "find",
         "control", "machine", "time", "years", "it's", "humans", "deadly"},
        {"life", "job", "york", "finds", "lives", "work", "personal", "living", "business", "hotel", "room", "decides",
         "starts", "people", "san", "news", "martin", "begins", "career", "sex"},
        {"night", "make", "friends", "love", "friend", "find", "things", "girl", "day", "good", "party", "decide",
         "it's",
         "turn", "she's", "he's", "guy", "apartment", "couple", "girlfriend"},
        {"man", "wife", "takes", "finds", "young", "named", "he's", "doctor", "george", "work", "child", "hospital",
         "nick",
         "real", "begins", "successful", "turns", "receives", "company", "mental"},
        {"town", "group", "find", "discover", "house", "small", "lives", "home", "young", "forced", "city", "road",
         "dead",
         "escape", "night", "people", "they're", "trip", "friends", "remote"},
        {"game", "team", "world", "star", "show", "rock", "career", "video", "play", "big", "tom", "jim", "win", "band",
         "perfect", "competition", "singer", "ultimate", "determined", "coach"},
        {"forces", "battle", "revenge", "evil", "death", "man", "alex", "blood", "group", "ancient", "vampire", "son",
         "dark",
         "kill", "mysterious", "end", "powers", "great", "joins", "powerful"},
        {"agent", "team", "mission", "government", "secret", "cia", "president", "u.s", "time", "american", "capture",
         "rescue", "black", "international", "leader", "security", "agents", "world's", "assassin", "plot"},
        {"evil", "king", "world", "save", "named", "love", "set", "queen", "peter", "prince", "beautiful", "white",
         "true",
         "princess", "time", "stop", "magic", "land", "magical", "power"},
        {"love", "young", "woman", "life", "man", "women", "falls", "jack", "beautiful", "story", "relationship",
         "affair",
         "marriage", "husband", "married", "finds", "sexual", "meets", "wife", "couple"},
        {"money", "gang", "boss", "run", "plan", "job", "he's", "local", "bank", "friend", "brother", "mob", "heist",
         "thief",
         "vegas", "driver", "business", "crew", "kill", "deal"}]


def edit_description(instance):

    # twenty different categories
    scores = [0] * 20

    # Strip out all the punctuation
    unstripped = instance[9].lower()
    for c in string.punctuation:
        unstripped = unstripped.replace(c,"")

    description = unstripped.split()

    # add to the score if a word matches a category
    # 10 is the description
    for word in description:
        for i, category in enumerate(LDA):
            if word in category:
                scores[i] += 1

    # save the target
    target = instance[-1]

    # get rid of the description and target columns
    instance = np.delete(instance, 10, 0) # 10 is which column, 1 means column, 0 means row
    instance = np.delete(instance, -1, 0)

    # add the scores
    instance = np.append(instance, scores)

    # add the target back on the end
    return np.append(instance, target)

def whichCategory(instance):
    return np.argmax(instance[9:-2])

def totalUpCategories(movies):

    grabCol = lambda x: x[9:-2]

    catCols = map(grabCol, movies)

    def addToTotal(total, items):
        return map(lambda t, x: int(t) + int(x), total, items)

    return reduce(addToTotal, catCols)

def countLDAgroups(arr):
    groups = {};

    for i in range(len(LDA)):
        groups[i] = 0

    for category in arr:
        groups[category[0]] += 1

    return groups

def main(argv):
    instance = np.array(["769","Goodfellas","False","en","Crime|Drama","Warner Bros.","25000000","1990-09-12","146","Henry Hill is a small time gangster, who takes part in a robbery with Jimmy \
        Conway and Tommy De Vito, two other gangsters who have set their sights a bit higher. His two partners kill off everyone else involved in the robbery,\
        and slowly start to climb up through the hierarchy of the Mob. Henry, however, is badly affected by his partners success, but will he stoop low enough to bring about the downfall of Jimmy and Tommy?"
        ,"46836394"])

    #instance = edit_description(instance)
    #print(instance)
    #print(whichCategory(instance))

    reader = csv.reader(open("detailed_new_list2.csv", "rb"), delimiter=',')
    movies_arr = list(reader)

    movie_arr_desc = map(edit_description, movies_arr)
    movie_cats = map(lambda x: [x], map(whichCategory, movie_arr_desc))

    category_totals = totalUpCategories(movie_arr_desc)

    # Retrievanator.write_to_csv("detailed_new_list2_LDA_cols.csv", movie_arr_desc);
    # Retrievanator.write_to_csv("detailed_new_list2_cats.csv", movie_cats);
    Retrievanator.write_to_csv("detailed_new_list2_cat_TOTAL.csv", [category_totals]);

# This is here to ensure main is only called when
#   this file is run, not just loaded
if __name__ == "__main__":
    main(sys.argv)
