#coding:utf-8
from functools import wraps
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from channels.handler import AsgiRequest
import jwt
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings
import logging

logger = logging.getLogger(__name__) #为logger定义name
User = get_user_model() #获取 User Class
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER

def token_authenticate(token,message):
    payload = check_payload(token=token,message=message)
    user = check_user(payload=payload,message=message)
    return user,token

#检查负载
def check_payload(token,message):
    payload = None
    try:
        payload = jwt_decode_handler(token)
    except jwt.ExpiredSignature:
        msg = _('Signature has expired.')
        logger.warn(msg)
        _close_reply_channel(message)
    except jwt.DecodeError:
        msg = _('Error decoding signature.')
        logger.warn(msg)
        _close_reply_channel(message)
    return payload

#检查用户
def check_user(payload,message):
    username = None
    try:
        username = payload.get('username')
    except Exception:
        msg = _('Invalid payload.')
        logger.warn(msg)
        _close_reply_channel(message)
        return

    try:
        user = User.objects.get_by_natural_key(username)
    except User.DoesNotExist:
        msg = _("User doesn't exist.")
        logger.warn(msg)
        raise exceptions.AuthenticationFailed(msg)

    if not user.is_active:
        msg = _('User account is disabled.')
        logger.warn(msg)
        raise exceptions.AuthenticationFailed(msg)
    return user

#关闭websokcet
def _close_reply_channel(message):
    message.reply_channel.send({"close":True})

#验证request中的token
def ws_auth_request_token(func):
    @wraps(func)
    def inner(message, *args, **kwargs):
        try:
            if "method" not in message.content:
                message.content['method'] = "FAKE"
            print("=================",message)
            request = AsgiRequest(message)
        except Exception as e:
            raise ValueError("Cannot parse HTTP message - are you sure this is a HTTP consumer? %s" % e)

        token = request.GET.get("token", None)
        print(request.path, request.GET)

        if token is None:
            _close_reply_channel(message)
            raise ValueError("Missing token request parameter. Closing channel.")

        # user, token = token_authenticate(token)
        user, token = token_authenticate(token, message)

        message.token = token
        message.user = user

        return func(message, *args, **kwargs)

    return inner



