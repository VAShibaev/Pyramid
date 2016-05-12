import os
import sys

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.wsgi import wsgiapp

@wsgiapp
def index(environ, start_response):
    status = '200 OK'
    response_headers = [("Content-Type", "text/html")]
    result = []
    file = open('/Users/stiv/GitHub/Pyramid/index.html', 'rb')        
    for line in file:
        result.append(line)
    file.close()
    start_response(status, response_headers)
    return result

@wsgiapp
def aboutme(environ, start_response):
    status = '200 OK'
    response_headers = [("Content-Type", "text/html")]
    result = []
    file = open('/Users/stiv/GitHub/Pyramid/about/aboutme.html', 'rb')
    for line in file:
        result.append(line)
    file.close()

    start_response(status, response_headers)
    return result    




class my_middleware(object):
    def __init__(self, my_application):
        self.app = my_application

    def __call__(self, environ, start_response):
        top_position = -1
        top_str = "\t\t<div class='top'>Middleware TOP</div>\n".encode()
        
        bottom_position = -1
        bottom_str = "\t\t<div class='botton'>Middleware BOTTOM</div>\n".encode()
        
        response = self.app(environ, start_response)
        for line in response:
            string = line.decode()
            if "<body>" in string :
                top_position = response.index(line)
            if "</body>" in string :
                bottom_position = response.index(line)

        response = response[:top_position+1] + [top_str] + \
                   response[top_position+1: bottom_position] + [bottom_str] +\
                   response[bottom_position:]
        
        return response



if __name__ == '__main__':
    config = Configurator()
    
    config.add_route('index1', '/index.html')
    config.add_route('index2', '/')
    config.add_route('aboutme', '/about/aboutme.html')

    config.add_view(index, route_name='index1')
    config.add_view(index, route_name='index2')
    config.add_view(aboutme, route_name='aboutme')

    pyramid_app = config.make_wsgi_app()

    my_application = my_middleware(pyramid_app)

    server = make_server('localhost', 8000, my_application)
    server.serve_forever()

    
    
        
