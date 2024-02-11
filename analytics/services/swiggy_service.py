import requests
import uuid
import json
from user_agent import generate_user_agent
from analytics.models import SwiggySessionData, SwiggyOrderTotal



class SwiggyService:

    def send_otp(phone_number):

       url = 'https://www.swiggy.com/dapi/auth/sms-otp'
  

       headers = {
            'cookie': f"_device_id={uuid.uuid4()}; _guest_tid={uuid.uuid4()}; _sid={uuid.uuid4()};",
            'User-Agent': generate_user_agent(),
            'Origin': 'https://www.swiggy.com',
            'Content-Type': 'application/json'
            }
       try:
         print("sending otp..")
         payload = json.dumps({
            "mobile": phone_number
            })  
         response = requests.request('POST', url=url, headers=headers, data=payload)

         resp_json = response.json()

         if resp_json["statusCode"] == 0 and resp_json["statusMessage"]=="done successfully":
             print("otp successfully sent")
             print("otp response: ", resp_json)
             SwiggySessionData(mobile = phone_number, t_id = resp_json['tid'], s_id = resp_json['sid'], device_id = resp_json['deviceId']).save()

       except Exception as e:

         print("otp sending error:", e)


    def verify_otp(mobile ,otp):
      
       swiggy_session_data = SwiggySessionData.objects.filter(mobile = mobile, state = 'ACTIVE').first()

       if swiggy_session_data is None:
          print("No swiggy session found for otp verification")
          return

       url='https://www.swiggy.com/dapi/auth/otp-verify'

       headers = {
            'cookie': f"_device_id={swiggy_session_data.device_id}; _guest_tid={swiggy_session_data.t_id}; _sid={swiggy_session_data.s_id};",
            'User-Agent': generate_user_agent(),
            'Origin': 'https://www.swiggy.com',
            'Content-Type': 'application/json'
            }

       try:
          payload = json.dumps({"otp": otp})

          response = requests.request('POST' ,url=url, headers=headers, data=payload)

          print(response.json())
       
          resp_json = response.json()

          if resp_json['statusCode'] == 0 and resp_json["statusMessage"]=="done successfully":
             print("otp successfully verified")
             print("otp verification response: ", resp_json)
             print("otp verification response headers: ", response.headers)

             for item in response.headers['set-cookie'].split(' '):
               if item.startswith('_session_tid'):
                 swiggy_session_data.session_id = item.split('=')[1]
                 swiggy_session_data.save()
                 break
             
             print('No session found')    

       except Exception as e:

          print("otp verification error: ", e)

    def third_party_call_for_order_listing(self, order_id, session_id, device_id, s_id, t_id, order_total, count, order_count):

       if order_id is None:
          url = "https://www.swiggy.com/dapi/order/all"
       else: 
          url = f"https://www.swiggy.com/dapi/order/all?order_id={order_id}"

       headers = {
            'cookie': f"_device_id={device_id}; _sid={s_id}; _session_tid={session_id};",
            'User-Agent': generate_user_agent(),
            'Origin': 'https://www.swiggy.com',
            'Content-Type': 'application/json'
            }   
      
       response =  requests.request('GET', url=url, headers=headers)
       

       if response.json()['statusCode'] == 0:
         next_page_order_id = None
         print("api call count: ", count)
         

         print(response)
         print(response.json())

         if len(response.json()['data']['orders']) == 0:
            print('******')
            mobile = SwiggySessionData.objects.filter(session_id = session_id, state = 'ACTIVE').first().mobile  
            SwiggyOrderTotal(mobile = mobile, order_total = order_total, num_of_orders=order_count).save()
            return
         
         
         for order in response.json()['data']['orders']:
            print(order)
            order_total += order['order_total']
            order_count+=1
            print("order count: ", order_count)
            print("order value incremented to ", order_total)
            next_page_order_id = order['order_id']
            
         
         SwiggyService().third_party_call_for_order_listing(order_id=next_page_order_id, 
                                                          session_id=session_id, 
                                                          device_id=device_id,
                                                          t_id=t_id, 
                                                          s_id=s_id, 
                                                          order_total=order_total, count= count+1, order_count=order_count)  

     
         
       return
        


    def third_party_order_dump(self, mobile):
       
       swiggy_session_data = SwiggySessionData.objects.filter(mobile=mobile, state = 'ACTIVE').first()

       if swiggy_session_data is None:
          print("No session found")
          return 
       

       try:
           self.third_party_call_for_order_listing(order_id=None, 
                                                  session_id =swiggy_session_data.session_id, 
                                                  device_id=swiggy_session_data.device_id, 
                                                  s_id = swiggy_session_data.s_id, 
                                                  t_id = swiggy_session_data.t_id,
                                                  order_total=0,
                                                  count=1,order_count=0)
       except Exception as e:
          print(e)


  