# LyricsGenius
# Copyright 2018 John W. Miller
# See LICENSE for details.

import json
import os


class Song(object):
    """A song from the Genius.com database."""

    def __init__(self, json_dict, lyrics=''):
        """ Song Constructor

        Properties:
            title:  (str) Title of the song.
            artist: (str) Primary artist on the song.
            lyrcis: (str) Full set of song lyrics.
            album:  (str) Name of the album the song is on.
            year:   (int) Year the song was released.

        Methods:
            save_lyrics: Save the song lyrics to a JSON or TXT file.
        """
        try:
            self._body = json_dict['song']
        except Exception as e:
            self._body = json_dict
        self._body['lyrics'] = lyrics
        self._url = self._body['url']
        self._api_path = self._body['api_path']
        self._id = self._body['id']

    @property
    def title(self):
        return self._body['title']

    @property
    def artist(self):
        return self._body['primary_artist']['name']

    @property
    def lyrics(self):
        return self._body['lyrics']

    @property
    def album(self):
        try:
            return self._body['album']['name']
        except Exception as e:
            return None

    @property
    def year(self):
        try:
            return self._body['release_date']
        except Exception as e:
            return None

    @property
    def url(self):
        try:
            return self._body['url']
        except Exception as e:
            return None

    @property
    def album_url(self):
        try:
            return self._body['album']['url']
        except Exception as e:
            return None

    @property
    def featured_artists(self):
        try:
            return self._body['featured_artists']
        except Exception as e:
            return None

    @property
    def media(self):
        m = {}
        if 'media' in self._body:
            [m.__setitem__(p['provider'], p['url']) for p in self._body['media']]
        return m

    @property
    def writer_artists(self):
        """List of artists credited as writers"""
        writers = []
        [writers.append((writer['name'], writer['id'], writer['url'])) for writer in self._body['writer_artists']]
        return writers

    @property
    def song_art_image_url(self):
        try:
            return self._body['song_art_image_url']
        except Exception as e:
            return None

    def save_lyrics(self, filename=None, format='txt', overwrite=False, verbose=True, binary=False):
        # TODO: way too much repeated code between this and the Artist.save_lyrics method
        """Allows user to save song lyrics from Song obejct to a .json or .txt file."""
        if format[0] == '.':
            format = format[1:]
        assert (format == 'json') or (format == 'txt'), "Format must be json or txt"

        # Determine the filename
        if filename is None:
            filename = "Lyrics_{}.{}".format(self.artist.replace(" ",""), format)
        else:
            filename = filename.split('.')[0] + '.' + format

        # Check if file already exists
        write_file = False
        if not os.path.isfile(filename):
            write_file = True
        elif overwrite:
            write_file = True
        else:
            if input("{} already exists. Overwrite?\n(y/n): ".format(filename)).lower() == 'y':
                write_file = True

        # Format lyrics in either .txt or .json format
        if format == 'json':
            lyrics_to_write = {'songs': [], 'artist': self.artist}
            lyrics_to_write['songs'].append({})
            lyrics_to_write['songs'][-1]['title']  = self.title
            lyrics_to_write['songs'][-1]['album']  = self.album
            lyrics_to_write['songs'][-1]['year']   = self.year
            lyrics_to_write['songs'][-1]['lyrics'] = self.lyrics
            lyrics_to_write['songs'][-1]['image']  = self.song_art_image_url
            lyrics_to_write['songs'][-1]['artist'] = self.artist
            lyrics_to_write['songs'][-1]['json']   = self._body
        else:
            lyrics_to_write = self.lyrics

        if binary:
            lyrics_to_write = lyrics_to_write.encode('utf8')

        # Write the lyrics to either a .json or .txt file
        if write_file:
            with open(filename, 'wb' if binary else 'w') as lyrics_file:
                if format == 'json':
                    json.dump(lyrics_to_write, lyrics_file)
                else:
                    lyrics_file.write(lyrics_to_write)
            if verbose:
                print('Wrote {} to {}.'.format(self.title, filename))
        else:
            if verbose:
                print('Skipping file save.\n')
        return lyrics_to_write

    def __str__(self):
        """Return a string representation of the Song object."""
        if len(self.lyrics) > 100:
            lyr = self.lyrics[:100] + "..."
        else:
            lyr = self.lyrics[:100]
        return '"{title}" by {artist}:\n    {lyrics}'.format(
                 title=self.title, artist=self.artist, lyrics=lyr.replace('\n', '\n    '))

    def __repr__(self):
        return repr((self.title, self.artist))

    def __cmp__(self, other):
        return cmp(self.title, other.title) and cmp(self.artist, other.artist) and cmp(self.lyrics, other.lyrics)
