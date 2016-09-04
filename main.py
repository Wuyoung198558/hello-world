#qpy:webapp:Hello Qpython
#qpy://127.0.0.1:8080/
"""
This is a sample for qpython webapp
"""
import os, sys
from bottle import Bottle, ServerAdapter
from bottle import run, debug, route, error, static_file, template


7######### QPYTHON WEB SERVER ###############

class MyWSGIRefServer(ServerAdapter):
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        #sys.stderr.close()
        import threading 
        threading.Thread(target=self.server.shutdown).start() 
        #self.server.shutdown()
        self.server.server_close() #<--- alternative but causes bad fd exception
        print("# qpyhttpd stop")


######### BUILT-IN ROUTERS ###############
#获取本脚本所在的路径
pro_path = os.path.split(os.path.realpath(__file__))[0]
sys.path.append(pro_path)
#定义assets路径，即静态资源路径，如css,js,及样式中用到的图片等
assets_path = '/'.join((pro_path,'assets'))
os.chdir(os.path.dirname(__file__))
@route('/assets/<filename:re:.*\.css|.*\.js|.*\.png|.*\.jpg|.*\.tpl>')
def server_static(filename):
    #print assets_path
    """定义/assets/下的静态(css,js,图片)资源路径"""
    return static_file(filename, root=assets_path)
@route('/assets/<filename:re:.*\.ttf|.*\.otf|.*\.eot|.*\.woff|.*\.svg|.*\.map>')
def server_static(filename):
    """定义/assets/字体资源路径"""
    return static_file(filename, root=assets_path)

@route('/__exit', method=['GET','HEAD'])
def __exit():
    global server
    server.stop()

@route('/__ping')
def __ping():
    return "ok"


#@route('/assets/<filepath:path>')
route('./static/<filename>')
def server_static(filename):
    filename += ".tpl"
    return static_file(filename, root='/')


######### WEBAPP ROUTERS ###############
@route('/')
def home():
    
    return template('test',name='QPython')


######### WEBAPP ROUTERS ###############

app = Bottle()
app.route('/', method='GET')(home)
app.route('/__exit', method=['GET','HEAD'])(__exit)
app.route('/__ping', method=['GET','HEAD'])(__ping)
#app.route('/assets/<filepath:path>', method='GET')(server_static)
app.route('./static/<filename>', method='GET')(server_static)


try:
    #print os.path
    server = MyWSGIRefServer(host="127.0.0.1", port="8080")
    app.run(server=server,reloader=False)
except (Exception) as ex:
    print("Exception: %s" % repr(ex))
