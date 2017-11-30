from django.shortcuts import render, HttpResponse

from app01 import models

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.authentication import BaseAuthentication

from rest_framework import serializers

from . import models

from xx.xx import caches

import json
# Create your views here.



class AmountView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            data = [{'course_id': 1, 'policy_id': 1}]   # 伪造数据

            # 检查数据合法
            user = models.Account.objects.get(id=1)
            for i in data:
                course = models.Course.objects.get(id=i['course_id'])
                price_set = user.couponrecord_set.all()
                if course.status != 0 or i['policy_id'] not in price_set:
                    raise



            buy_list = []
            for i in data:
                course = models.Course.objects.get(id=i['course_id'])
                price_policy = models.PricePolicy.objects.get(id=i['policy_id'])

                policy_tmp = {}
                policy_tmp['price'] = price_policy.price
                policy_tmp['valid_period'] = price_policy.valid_period
                policy_tmp['course']['id'] = course.id
                policy_tmp['course']['name'] = course.name
                policy_tmp['course']['img'] = course.course_img
                buy_list.append(policy_tmp)

            res = {user.id: buy_list}

            import json
            with open('trad_list.txt', 'w', encoding='utf8') as f:
                json.dump(res, f)

        except Exception as e:
            print(e)
            return HttpResponse('滚犊子')


class CustomAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """


        user_obj = models.Account.objects.filter(pk=1).first()

        if user_obj:
            # (UserInfo对象,Token对象)
            return (user_obj,user_obj)

class CoursSerializers(serializers.ModelSerializer):
    PricePolicy_list = serializers.SerializerMethodField()

    class Meta:
        model = models.Course
        fields = ['id','name','course_img','PricePolicy_list']
    def get_PricePolicy_list(self,obj):
        ret = []
        for price_policy_obj in obj.price_policy.all():
            ret.append({'id':price_policy_obj.id,'valid_priod':price_policy_obj.valid_period,'price':price_policy_obj.price})
        return ret


class ShoppingViews(APIView):
    '''
    购物车功能，实现增删改查功能
    '''
    authentication_classes = [CustomAuthentication, ]
    def get(self, request, *args, **kwargs):
        '''
        返回购物车页面数据：商品名称，商品有效期，商品价格
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        reponse = {'code':1000,'data':None,'msg':None}
        if request.user:
            try:
                data = caches.get('shopping_cart',request.user.id)
                if not data:
                    reponse['data'] = None
                    return Response(reponse)
                reponse['data'] = json.loads(data.decode('utf8'))
            except Exception as e:
                print(e)
                reponse['code'] = 1002
                reponse['msg'] = '购物车列表获取失败'


        else:
            reponse['code'] = 1001
            reponse['msg'] = '非登录用户不能访问'



        return Response(reponse)


    def post(self, request, *args, **kwargs):
        '''
        加入购物车
        :param request:
        :param args:
        :param kwargs:{courseId: "5", validPeriodId: "90"}
        :return: 购买用户id，被选中的商品套餐id，
        '''
        #获取当前登录用户
        reponse = {'code': 1000, 'msg': None}
        if request.user:
            try:
                courseId = request.POST.get('courseId')
                validPeriodId = request.POST.get('validPeriodId')
                course_obj = models.Course.objects.get(pk = courseId)
                models.PricePolicy.objects.get(pk =validPeriodId )
                ser = CoursSerializers(instance=course_obj,many=False)
                tag = False
                for item in ser.data.get('PricePolicy_list'):

                    if validPeriodId == str(item.get('id')):
                        tag = True
                        break

                if not tag:
                    raise
                print(222)
                data_dict = dict(ser.data)
                data_dict['selected_policty_id'] = validPeriodId
                ret = []
                data_list = caches.get('shopping_cart',request.user.id)
                if data_list:
                    ret = json.loads(data_list.decode('utf8'))
                    # [{"id": 2, "name": "python21天放弃", "course_img": "/static/image/course_img/1.png",
                    #   "PricePolicy_list": [{"id": 4, "valid_priod": 30, "price": 20.0},
                    #                        {"id": 5, "valid_priod": 180, "price": 100.0}], "selected_policty_id": "4"}]

                    for dict_obj in ret:
                        if data_dict.get('id') == dict_obj.get('id'):
                            dict_obj['selected_policty_id'] = validPeriodId
                            caches.set('shopping_cart', request.user.id, json.dumps(ret))
                            return Response(reponse)
                ret.append(data_dict)

                caches.set('shopping_cart',request.user.id,json.dumps(ret))

            except Exception as e:
                print(e)
                reponse['code'] = 1002
                reponse['msg'] = '没有这个课程或套餐'

        else:
            reponse['code'] = 1001
            reponse['msg'] = '非登录用户不能访问'

        return Response(reponse)

    def delete(self, request, *args, **kwargs):
        '''
        删除购物车中指定货物
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        reponse = {'code': 1003, 'msg': None}
        if request.user:
            try:
                if kwargs.get('kw') == 'all':
                    caches.delete('shopping_cart', request.user.id)
                    reponse['code'] = 1000
                courseId = request.POST.get('courseId')
                data = caches.get('shopping_cart', request.user.id)
                data_list = json.loads(data.decode('utf8'))
                # [{"id":2,"name":"python21天放弃","course_img":"/static/image/course_img/1.png","PricePolicy_list":[{"id":4,"valid_priod":30,"price":20.0},{"id":5,"valid_priod":180,"price":100.0}],"selected_policty_id":"4"},{"id":1,"name":"爬虫开发","course_img":"/static/image/course_img/1.png","PricePolicy_list":[{"id":1,"valid_priod":30,"price":9.9},{"id":2,"valid_priod":90,"price":49.0},{"id":3,"valid_priod":180,"price":99.0}],"selected_policty_id":"1"}]
                for data_dict in data_list:

                    if int(courseId) == data_dict.get('id'):
                        print(111)
                        data_list.remove(data_dict)
                        caches.set('shopping_cart', request.user.id, json.dumps(data_list))
                        reponse['code'] = 1000
                        return Response(reponse)

            except Exception as e:
                print(e)
                reponse['code'] = 1002
                reponse['msg'] = '删除失败'

        else:
            reponse['code'] = 1001
            reponse['msg'] = '非登录用户不能访问'

        return Response(reponse)

