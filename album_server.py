from bottle import route
from bottle import run
from bottle import request
from bottle import HTTPError

import album


@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Никаких альбомов {} в базе данных не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        album_count = len(album_names)
        result = "Суммарное количество альбомов {} -- {} шт. Вот их список: <br> - ".format(artist, album_count)
        result += "<br> - ".join(album_names)
    return result


@route("/albums", method="POST")
def create_album():
    year = request.forms.get("year")
    artist = request.forms.get("artist")
    genre = request.forms.get("genre")
    album_name = request.forms.get("album")
    
    try:
        year = int(year)
    except ValueError:
        return HTTPError(400, "Год альбома указан некорректно")

    try:
        new_album = album.save(year, artist, genre, album_name)
    except AssertionError as err:
        result = HTTPError(400, str(err))
    except album.AlreadyExists as err:
        result = HTTPError(409, str(err))
    else:    
        print("Новый альбом {} сохранён в базу данных".format(new_album.album))
        result = "Новый альбом {} сохранён в базу данных".format(new_album.album)
    return result


if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)