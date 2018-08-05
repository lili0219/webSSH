import errno
import os


class WebsocketAuth(object):
    @property
    def authenticate(self):
        if self.message.user.is_authenticated:
            return True
        else:
            return False
    def haspermission(self,perm):
        if self.message.user.has_perm(perm):
            return True
        else:
            return False

def get_redis_instance():
    """
    _connection_list
    :return:
    """
    from webterminal.asgi import channel_layer
    return channel_layer._connection_list[0]

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise