# from channels import Group
# from .ws_authentication import ws_auth_request_token
# from common.utils import get_redis_instance
# from channels.generic.websockets import WebsocketConsumer
# import json
#
# queue = get_redis_instance()
# channel = queue.pubsub()
# # Connected to websocket.connect
# @ws_auth_request_token
# def ws_add(message):
#     # Accept the connection
#     queue.publish(message.reply_channel.name, json.dumps(['hello']))
#     message.reply_channel.send({"accept": True})
#     # Add to the chat group
#     Group("chat").add(message.reply_channel)
#
# # Connected to websocket.receive
# def ws_message(message):
#     Group("chat").send({
#         "text": "[user] %s" % message.content['text'],
#     })
#
# # Connected to websocket.disconnect
# def ws_disconnect(message):
#     Group("chat").discard(message.reply_channel)
import time
import json
from django.views.decorators import cache
from channels.generic.websockets import WebsocketConsumer
from channels.handler import AsgiRequest
from .ws_authentication import token_authenticate

class MyConsumer(WebsocketConsumer):
    # Set to True if you want it, else leave it out
    strict_ordering = False

    http_user = True
    # 由于使用的是token方式，需要使用session将user传递到receive中
    channel_session_user = True

    def connection_groups(self, **kwargs):
        """
        Called to return the list of groups to automatically add/remove
        this connection to/from.
        """
        return ['test']

    def connect(self, message, **kwargs):
        try:
            request = AsgiRequest(message)
        except Exception as e:
            self.close()
            return
        token = request.GET.get("token", None)
        if token is None:
            self.close()
            return
        user, token = token_authenticate(token, message)
        message.token = token
        message.user = user
        message.channel_session['user']=user
        self.message.reply_channel.send({"accept": True})
        print('连接状态', message.user)

    def receive(self, text=None, bytes=None, **kwargs):
        print('接收到消息', text, self.message.channel_session['user'])
        """
        Called when a message is received with decoded JSON content
        """
        # Simple echo
        value = cache.get('test')
        print(value)
        while True:
            if cache.get('test') is not None and cache.get('test') != value:
                value = cache.get('test')
                break
            time.sleep(1)
        self.send(json.dumps({
            "text": cache.get('test')
        }))

    def disconnect(self, message, **kwargs):
        """
        Perform things on connection close
        """
        pass