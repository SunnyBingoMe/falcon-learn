import json, falcon

class ObjRequestClass:
    __json_content = {}


    def __validate_json_input(self, req):
        try:
            self.__json_content = json.loads(req.stream.read().decode('utf-8'))
            print('json input is valid')
            return(True)
        except ValueError as e: # differs from py2
            self.__json_content = {}
            print('ERR: json input is NOT valid.')
            return(False)


    def on_get(self, req, resp):
        output = {}
        resp.status = falcon.HTTP_200
        
        input_data = req.stream.read()
        print(input_data)
        input_data = json.loads(input_data.decode('utf-8'))
        print(input_data)
        
        content = {
                'name': 'pppSunny',
                'age': '30',
                'country': 'Sweden'
                }
        
        if('method' not in input_data):
            resp.status = falcon.HTTP_501
            output['value'] = 'ERR: none method found.'
        else:
            if(input_data['method'] == 'get-name'):
                output['value'] = content['name']
                output['msg'] = 'Hello, {0}'.format(input_data['name'])
            else:
                resp.status = falcon.HTTP_404
                output['value'] = None

        resp.body = json.dumps(output)
        print('eggs.')


    def on_post(self, req, resp):
        output = {}
        resp.status = falcon.HTTP_200
        
        input_data = req.stream.read()
        input_data = json.loads(input_data.decode('utf-8'))
        print(input_data)
        
        result = int(input_data['x']) + int(input_data['y'])
        output['msg'] = 'Hello, x:{0}, y:{1}, result:{2}.'.format(input_data['x'], input_data['y'], result)
        
        resp.body = json.dumps(output)
        print('eggs.')


    def on_put(self, req, resp):
        output = {'status': 301} # just a msg to client, will not influence the `resp.status` in HTTP
        resp.status = falcon.HTTP_200
        
        if(self.__validate_json_input(req)):
            input_data = self.__json_content
            #input_data = json.loads(req.stream.read().decode('utf-8')) # will not work, see: is.gd/zMeBoZ
            print(input_data)
            result = int(input_data['x1']) + int(input_data['y1'])
            output['msg'] = 'Hello, x:{x}, y:{y}, result:{z}.'.format(x=input_data['x1'], y=input_data['y1'], z=result)
        else:
            output = {'status': 302}
        
        resp.body = json.dumps(output)
        print('eggs.')


    def on_delete(self, req, resp):
        output = {}
        resp.status = falcon.HTTP_200
        param_is_valid = True
        if('x' not in req.params or 'y' not in req.params):
            param_is_valid = False
        
        if(param_is_valid):
            output = {
                    'x': req.params['x'],
                    'y': req.params['y']
                    }
        else:
            output['msg'] = 'ERR: param NOT valid.'
        
        resp.body = json.dumps(output)

api = falcon.API()
api.add_route('/test', ObjRequestClass())

