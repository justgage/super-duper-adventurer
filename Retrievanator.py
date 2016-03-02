import requests
import sys
import unicodecsv as csv

# eww globals
api_key = "46162c243979ee401c3e6942765f3d51"
start_year = 2010
end_year = 2011
page_max = 2
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
                obj["budget"], obj["release_date"], obj["runtime"], obj["revenue"]]


def write_to_csv(file_name, data):
    file = open(file_name, 'wb')
    writer = csv.writer(file, delimiter=',')
    writer.writerows(data)
    file.close()


def main(args):
    movies = get_movie_list()
    movies_arr = [[x["id"], x["title"]] for x in movies]

    detailed_list = []

    for mov in movies_arr:
        detailed_list.append(get_required_fields(detailed_movie_info(mov[0])))

    write_to_csv("detailed_list.csv", detailed_list)


if __name__ == "__main__":
    main(sys.argv)
