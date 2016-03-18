import requests
import sys
import unicodecsv as csv
import time


# eww globals
api_key = "46162c243979ee401c3e6942765f3d51"
start_year = 1990
end_year = 2016
page_max = 11
request_limit = 5


def get_movie_list():

    movie_list = []

    for year in range(start_year, end_year):
        for page in range(1, page_max):
            url = "https://api.themoviedb.org/3/discover/movie?primary_release_year=" \
                  + str(year) \
                  + "&page=" + str(page) + "&api_key=" + api_key
            request_count = 0
            r = requests.get(url=url)
            while request_count < request_limit and r.status_code != 200:
                r = requests.get(url=url)
                request_count += 1
                time.sleep(.25)

            if r.status_code == 200:
                movie_list += r.json()["results"]
            else:
                print(url)
    return movie_list


def detailed_movie_info(id):
    url = "https://api.themoviedb.org/3/movie/" + str(id) + "?api_key=" + api_key
    request_count = 0
    r = requests.get(url=url)
    while request_count < request_limit and r.status_code != 200:
        r = requests.get(url=url)
        request_count += 1

    return r.json()


def get_required_fields(obj):
    return [obj["id"], obj["title"], obj["adult"], obj["original_language"],
                "|".join(sorted([x["name"] for x in obj["genres"]])),
                "|".join(sorted([x["name"] for x in obj["production_companies"]])),
                obj["budget"], obj["release_date"], obj["runtime"], obj["overview"], obj["revenue"]]


def write_to_csv(file_name, data):
    file = open(file_name, 'wb')
    writer = csv.writer(file, delimiter=',')
    writer.writerows(data)
    file.close()


def read_from_csv(file_name):
    reader = csv.reader(open(file_name, "rb"), delimiter=',')
    return list(reader)


def main(args):
    #movies = get_movie_list()
    #movies_arr = [[x["id"], x["title"]] for x in movies]
    #write_to_csv("movie_list.csv", movies_arr)

    reader = csv.reader(open("new_movie_list.csv", "rb"), delimiter='\t')
    movies_arr = list(reader)
    detailed_list = []

    for mov in movies_arr:
        try:
            detailed_list.append(get_required_fields(detailed_movie_info(mov[0])))
        except KeyError:
            print("couldn't get " + str(mov))

    write_to_csv("detailed_new_list2.csv", detailed_list)

    #x = read_from_csv('detailed_list.csv')
    #num = len(list(filter(lambda row: row[-1] != '0', x)))


if __name__ == "__main__":
    main(sys.argv)
