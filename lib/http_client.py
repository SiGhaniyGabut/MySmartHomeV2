import requests, gc

class Response:
    def __init__(self, response, save_to: str=''):
        self.response = response
        self.save_to = save_to

        if save_to: DataStream(response.raw, save_to).write()

class DataStream:
    def __init__(self, data, save_to: str):
        self.data = data
        self.save_to = save_to

    def write(self, chunk_size: int = 512):
        with open(self.save_to, 'wb') as file:
            while chunk := self.data.read(chunk_size):
                file.write(chunk)
            file.close()

class HttpClient:
    def __init__(self):
        gc.collect()

    def get(self, url: str, params: dict={}, headers: dict={}, **kwargs):
        return self.request('GET', url, params, headers, **kwargs)
    
    def post(self, url: str, data: dict = {}, headers: dict = {}, **kwargs):
        return self.request('POST', url, data, headers, **kwargs)
    
    def put(self, url: str, data: dict = {}, headers: dict = {}, **kwargs):
        return self.request('PUT', url, data, headers, **kwargs)
    
    def patch(self, url: str, data: dict = {}, headers: dict = {}, **kwargs):
        return self.request('PATCH', url, data, headers, **kwargs)
    
    def delete(self, url: str, headers: dict = {}, **kwargs):
        return self.request('DELETE', url, headers, **kwargs)
    
    def request(self, method: str, url: str, params: dict={}, data: dict={}, headers: dict={}, stream=False, save_to: str='', **kwargs):
        return Response(
            requests.request(
                method, url + self.__params(params), data=data, stream=stream, headers=self.__headers(headers), **kwargs
                ), save_to
            ).response

    def __headers(self, headers: dict = {}):
        default = { 'content-type': 'application/json', 'user-agent': 'MySmartHomeV2 with MicroPython on ESP' }
        default.update(headers)

        return default

    def __params(self, params: dict = {}):
        return '?' + '&'.join([f'{k}={v}' for k, v in params.items() if v]) if params else ''
