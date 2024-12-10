# -*- coding: utf-8 -*-

WEBSITE = 'CDN'

import re
import os
import sys
import json
# try:
#     from resources.lib.autotranslate import AutoTranslate
#     portuguese = AutoTranslate.language('Portuguese')
#     english = AutoTranslate.language('English')
#     select_option_name = AutoTranslate.language('select_option')
# except ImportError:
#     portuguese = 'DUBLADO'
#     english = 'LEGENDADO'
#     select_option_name = 'SELECIONE UMA OPÇÃO ABAIXO:'
# try:
#     from resources.lib import resolveurl
#     from resources.lib.unblock import unblock as requests
# except ImportError:
#     local_path = os.path.dirname(os.path.realpath(__file__))
#     lib_path = local_path.replace('scrapers', '')
#     sys.path.append(lib_path)
#     from resolvers import resolveurl
#     from unblock import unblock as requests
import requests
from urllib.parse import urljoin as resolveurl
portuguese = 'DUBLADO'
english = 'LEGENDADO'
select_option_name = 'SELECIONE UMA OPÇÃO ABAIXO:'

class source:
    __headers__ = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0', 'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3'}

    @classmethod
    def warezcdn_servers(cls,imdb,season=False,episode=False):
        links = []
        host_url = 'https://embed.warezcdn.link/'
        referer = 'https://embed.warezcdn.com/'
        headers = cls.__headers__
        headers.update({'Referer': referer})        
        if season and episode:
            # get series page
            referer_url = 'https://embed.warezcdn.com/serie/%s'%(str(imdb))
            data = requests.get(referer_url).text

            # extract url to get seasons information
            season_url = re.compile(r"var cachedSeasons\s*=\s*(?P<url>'(?:[^\']+)'|\"([^\"]+)\")", re.MULTILINE | re.DOTALL | re.IGNORECASE).findall(data)[0][1]
            season_url = 'https://embed.warezcdn.link/' + season_url

            # get seasons information
            seasons_info = requests.get(season_url, headers={'Referer': referer_url}).json()['seasons']

            # search for specified season and episode
            episode_info = {}
            for key in seasons_info.keys():
                season_dict = seasons_info[key]
                if season_dict['name'] == str(season):
                    # search for specified episode
                    for key in season_dict['episodes'].keys():
                        episode_dict = season_dict['episodes'][key]
                        if episode_dict['name'] == str(episode):
                            episode_info = episode_dict
                            break
            
            # request audio data
            request_url = 'https://embed.warezcdn.link/core/ajax.php?audios=%s' % episode_dict['id']

            audio_ids = requests.get(
                request_url,
                headers={'Referer': referer_url}
                ).json()
            audio_ids = json.loads(audio_ids)
                        
            if audio_ids:
                for audio in audio_ids:
                    if int(audio['audio']) == 1:
                        lg = portuguese
                    elif int(audio['audio']) == 2:
                        lg = english

                    servers = ['warezcdn', 'mixdrop']
                    for server in servers:
                        if server in audio['servers']:
                            embed_referer_url = 'https://embed.warezcdn.link/getEmbed.php?id=%s&sv=%s&lang=%s' % (audio['id'], server, audio['audio'])
                            play_url = 'https://embed.warezcdn.link/getPlay.php?id=%s&sv=%s' % (audio['id'], server)

                            # get referer urls to avoid bot detection
                            requests.get(referer_url)
                            requests.get(
                                embed_referer_url,
                                headers={'Referer': referer_url}
                                )
                            
                            # get embed play html
                            play_response = requests.get(
                                play_url,
                                headers={'Referer': embed_referer_url}
                                ).text

                            # extract video url from play_response
                            video_url = re.compile(r"window.location.href = (?:\'|\")(.+)(?:\'|\")", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(play_response)[0]
                            
                            # save name and url to the list of links
                            name = server.upper() + ' - ' + lg
                            links.append((name,video_url))

        else:
            # movie page url
            referer_url = 'https://embed.warezcdn.link/filme/%s' % imdb

            # request html content of the movie page
            data = requests.get(referer_url).text

            # extract audio data from the html content
            audio_ids = re.compile(r"let data = (?:\'|\")(\[.+\])(?:\'|\")", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(data)
            audio_ids = json.loads(audio_ids[0])
            
            if audio_ids:
                for audio in audio_ids:
                    if int(audio['audio']) == 1:
                        lg = portuguese
                    elif int(audio['audio']) == 2:
                        lg = english

                    servers = ['warezcdn', 'mixdrop']
                    for server in servers:
                        if server in audio['servers']:
                            embed_referer_url = 'https://embed.warezcdn.link/getEmbed.php?id=%s&sv=%s&lang=%s' % (audio['id'], server, audio['audio'])
                            play_url = 'https://embed.warezcdn.link/getPlay.php?id=%s&sv=%s' % (audio['id'], server)

                            # get referer urls to avoid bot detection
                            requests.get(referer_url)
                            requests.get(
                                embed_referer_url,
                                headers={'Referer': referer_url}
                                )
                            
                            # get embed play html
                            play_response = requests.get(
                                play_url,
                                headers={'Referer': embed_referer_url}
                                ).text

                            # extract video url from play_response
                            video_url = re.compile(r"window.location.href = (?:\'|\")(.+)(?:\'|\")", re.MULTILINE|re.DOTALL|re.IGNORECASE).findall(play_response)[0]
                            
                            # save name and url to the list of links
                            name = server.upper() + ' - ' + lg
                            links.append((name,video_url))

        return links
    
    @classmethod
    def search_movies(cls,imdb,year):
        try:
            return cls.warezcdn_servers(imdb,False,False)
        except:
            return []      
    
    @classmethod
    def resolve_movies(cls,url):
        #referer_player = 'https://warezcdn.com/'
        referer_player = ''
        streams = []
        if 'embed.warezcdn' in url:
            referer = 'https://embed.warezcdn.com/'
            headers = cls.__headers__
            headers.update({'Referer': referer})            
            try:
                r = requests.get(url,headers=headers)
                src = r.text
                try:
                    src = re.compile('window.location.href="(.*?)"').findall(src)[0]
                except:
                    src = ''
                if src:
                    try:
                        sub = src.split('http')[2]
                        sub = 'http%s'%sub
                        try:
                            sub = sub.split('&')[0]
                        except:
                            pass
                        if not '.srt' in sub:
                            sub = ''                                            
                    except:
                        sub = ''
                    try:
                        src = src.split('?')[0]
                    except:
                        pass
                    try:
                        src = src.split('#')[0]
                    except:
                        pass
                    stream, sub2 = resolveurl(src,referer_player)
                    if sub:
                        subfinal = sub
                    else:
                        subfinal = sub2
                    streams.append((stream,subfinal))
            except:
                pass          
        return streams
    
    @classmethod
    def search_tvshows(cls,imdb,year,season,episode):
        try:
            return cls.warezcdn_servers(imdb,season,episode)
        except:
            return []    

    @classmethod
    def resolve_tvshows(cls,url):
        #referer_player = 'https://warezcdn.com/'
        referer_player = ''
        streams = []
        if 'embed.warezcdn' in url:
            referer = 'https://embed.warezcdn.com/'
            headers = cls.__headers__
            headers.update({'Referer': referer})            
            try:
                r = requests.get(url,headers=headers)
                src = r.text
                try:
                    src = re.compile('window.location.href="(.*?)"').findall(src)[0]
                except:
                    src = ''
                if src:
                    try:
                        sub = src.split('http')[2]
                        sub = 'http%s'%sub
                        try:
                            sub = sub.split('&')[0]
                        except:
                            pass
                        if not '.srt' in sub:
                            sub = ''                                            
                    except:
                        sub = ''
                    try:
                        src = src.split('?')[0]
                    except:
                        pass
                    try:
                        src = src.split('#')[0]
                    except:
                        pass
                    stream, sub2 = resolveurl(src,referer_player)
                    if sub:
                        subfinal = sub
                    else:
                        subfinal = sub2
                    streams.append((stream,subfinal))
            except:
                pass          
        return streams                    

