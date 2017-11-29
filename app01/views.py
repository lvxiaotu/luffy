
from django.shortcuts import render, HttpResponse
from app01 import models

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.authentication import BaseAuthentication

from rest_framework import serializers

from . import models
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

shopping_cart ={}
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
        fields = ['name','course_img','PricePolicy_list']
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
                reponse['data'] = shopping_cart
            except Exception as e:
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


                shopping_cart[courseId] = ser.data
                shopping_cart[courseId]['selected_policty_id'] = validPeriodId

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
        reponse = {'code': 1000, 'msg': None}
        if request.user:
            try:
                courseId = request.POST.get('courseId')
                if courseId in shopping_cart:
                    shopping_cart.pop(courseId)

            except Exception as e:
                print(e)
                reponse['code'] = 1002
                reponse['msg'] = '删除失败'

        else:
            reponse['code'] = 1001
            reponse['msg'] = '非登录用户不能访问'

        return Response(reponse)

