from django.shortcuts import render, HttpResponse
from app01 import models
from rest_framework.views import APIView
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
