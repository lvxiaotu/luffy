#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Q1mi"
# Date: 2017/11/17


class MiddlewareMixin(object):
    def __init__(self, get_response=None):
        self.get_response = get_response
        super(MiddlewareMixin, self).__init__()

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

class M1(MiddlewareMixin):


    def process_response(self,request,response):
        # print('*****',response,type(response))

        if request.method == 'OPTIONS':
            response['Access-Control-Allow-Headers'] = 'content-type'
            response['Access-Control-Allow-Origin'] = '*'


        else:
            response['Access-Control-Allow-Origin'] = '*'
        # print(response._headers)

        return response


