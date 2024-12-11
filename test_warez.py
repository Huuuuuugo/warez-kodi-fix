from warez import *


# filme
print("MOVIE SOURCES:")
links = source.warezcdn_servers('tt1187064')
for link in links:
    print(source.resolve_movies(link[1]))
    input()

# serie
print("SERIES SOURCES:")
links = source.warezcdn_servers('tt0436992', 1, 1)
for link in links:
    print(source.resolve_tvshows(link[1]))
    input()

# search movies
print(source.search_movies('tt1187064', 0))

# search tvshows
print(source.search_tvshows('tt0436992', 0, 1, 1))
