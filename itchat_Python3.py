import itchat,requests,re
from pandas import DataFrame
from urllib.request import quote

url_headers = {
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
    'Connection': "keep-alive",
    'Content-Type': "application/x-www-form-urlendatad",
    'Cookie': "PHPSESSID=cvfk3e39sdadadasdor3td2; tkdg_user_info=think%3A%7B%22id%22%3A%kdhakdhalskdhlasdasdhasldhjalkdhlak32dd7a%22%7D",
    'Host': "www.taokouling.com",
    'Origin': "http://www.taokouling.com",
    'Referer': "http://www.taokouling.com/index/taobao_tkljm/",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest"
}

def save(UserName, NickName, CreateTime, fanli_rmb, quan_info, price, suo_url, content_title):
    df = DataFrame({
        '发送者昵称': [NickName],
        '发送者标识': [UserName],
        '消息时间': [CreateTime],
        '返利金额': [fanli_rmb],
        '优惠券信息': [quan_info],
        '付费价': [price],
        '跳转链接': [suo_url],
        '商品标题': [content_title]
    })
    df.to_csv(
        './1.0.0淘宝客用户使用统计.csv', mode='a', encoding='utf-8-sig', header=False
    )

#此处为pid，即淘宝联盟获取的pid；
pid = 'mm_128460193_324588930_89729003452'
#此处为uid，即高佣授权ID；
uid = '901545344'
#此处为pid值第二段，也就是中间的段，例如上面的324588930
siteid = '324588930'
##此处为pid值第二段，也就是中间的段，例如上面的89729003452
adzoneid = '89729003452'



@itchat.msg_register(itchat.content.TEXT)
def reply_self(msg):
    #获取发送者信息；
    NickName = msg['User']['NickName']  #发送者昵称
    UserName = msg['User']['UserName']  #发送者唯一标示
    CreateTime = msg['CreateTime']   #发送时间

    print(msg['Text'])

    if len(msg['Text']) > 11:   #判断用户发送的内容字符长度
        ShangPing_TKL = (msg['Text'][msg['Text'].index('￥') + 1:msg['Text'].index('￥') + 12]).strip('￥')  #获取商品淘口令

        # 开始获取商品ID及获取返利链接，简述为一键转单；
        try:
            payload = 'tkl=' + ShangPing_TKL + '&zdgy=true&pid=' + pid + '&tkltitle=%20&tklpic=%20&tkluserid=%20&tgdl=true&undefined='
            url = 'http://www.taokouling.com/index/tbtkltoitemid/'
            url_res = requests.post(url, headers=url_headers, data=payload)
            yijian_itemid = url_res.json()['data']['itemid']
            yijian_click_url = url_res.json()['data']['url']
            print('商品ID：' + yijian_itemid)
            print('返利链接：' + yijian_click_url)


            #开始获取返利金额及比例；
            try:
                url_FanLi_Price = 'http://www.taokouling.com/index/tbkitemget/'
                payload_url_FanLi_Price = 'itemid=' + yijian_itemid
                res_url_FanLi_Price = requests.post(url_FanLi_Price, headers=url_headers, data=payload_url_FanLi_Price)
                if 'quan_info' in res_url_FanLi_Price.json()['data']:
                    quan_info = re.findall('\d+', res_url_FanLi_Price.json()['data']['quan_info'])[1]  # 优惠券
                    price = round(float(res_url_FanLi_Price.json()['data']['price']) - float(quan_info), 2) # 付费价
                    #fanli_rmb = round((float(res_url_FanLi_Price.json()['data']['commission_rate']) * 0.01 * price), 2)  # 返利金额

                    # 通过高佣api获取返利比例；
                    try:
                        url_gaoyong_api = 'https://api.taokouling.com/tbk/TbkPrivilegeGet'
                        payload_gaoyong = {'itemid': yijian_itemid, 'siteid': siteid, 'adzoneid': adzoneid,
                                           'uid': uid}
                        res_gaoyong = requests.post(url_gaoyong_api, data=payload_gaoyong)
                        fanli_rmb = round((float(res_gaoyong.json()['result']['data']['max_commission_rate']) * 0.01 * price),
                                          2)  # 返利金额

                        print(quan_info)
                        print(price)
                        print(fanli_rmb)

                    except:
                        print('查询返利比例失败')
                        return '查询返利比例失败'

                    #正在解析淘口令；
                    try:
                        url = "http://www.taokouling.com/index/taobao_tkljm/"
                        payload_JieXi = 'text=' + str(ShangPing_TKL)
                        response_JieXi = requests.post(url, data=payload_JieXi, headers=url_headers)
                        content_title = response_JieXi.json()['data']['content']  # 标题
                        content_picUrl = response_JieXi.json()['data']['picUrl']  # 头图
                        print('内容标题：' + content_title)

                        #生成淘口令；
                        try:
                            url = "http://www.taokouling.com/index/tktaokouling/"
                            payload_TaoKouLing = 'url=' + yijian_click_url + '&tgdl=false&tkltitle=' + quote(
                                content_title.encode('utf-8')) + '&tklpic=' + content_picUrl + '&tkluserid=&undefined='
                            response_TaoKouLing = requests.post(url, data=payload_TaoKouLing, headers=url_headers)
                            TKL_num = response_TaoKouLing.json()['data'][0]['tkl']
                            print('返利金额：' + str(fanli_rmb) + ' 优惠券：' + str(quan_info) + ' 付费价格：' + str(price))
                            yang_url = 'https://yangshuhello01.gitee.io/yangshuf/YangShu.html?password=' + TKL_num.strip(
                                '￥') + '&url=' + yijian_click_url + '&MainPicture=' + content_picUrl

                            #长链接转换为短链接；
                            try:
                                url_Conversion = 'http://www.taokouling.com/index/tbshorturl/'
                                payload_Conversion = 'url=' + quote(yang_url.encode('utf-8')) + '&type=' + '1'
                                res_Conversion = requests.post(url_Conversion, headers=url_headers, data=payload_Conversion)
                                suo_url = res_Conversion.json()['data'][0]

                                # 运行保存函数；
                                save(UserName, NickName, CreateTime, fanli_rmb, quan_info, price, suo_url,
                                     content_title)
                                return '约返：' + str(fanli_rmb) + '元，优惠：' + str(quan_info) + '元，付费价：' + str(
                                    price) + '元；跳转链接：' + suo_url

                            except:
                                print('长链接转换失败')
                                return '长链接转换失败'

                        except:
                            print('生成淘口令运行异常')
                            return '生成淘口令运行异常'

                    except:
                        print('淘口令解析异常')
                        return '淘口令解析异常'

                else:
                    quan_info = 0
                    price = float(res_url_FanLi_Price.json()['data']['price'])  # 付费价

                    # 通过高佣api获取返利比例；
                    try:
                        url_gaoyong_api = 'https://api.taokouling.com/tbk/TbkPrivilegeGet'
                        payload_gaoyong = {'itemid': yijian_itemid, 'siteid': siteid, 'adzoneid': adzoneid,
                                           'uid': uid}
                        res_gaoyong = requests.post(url_gaoyong_api, data=payload_gaoyong)
                        fanli_rmb = round((float(res_gaoyong.json()['result']['data']['max_commission_rate']) * 0.01 * price),
                                          2)  # 返利金额

                        print(quan_info)
                        print(price)
                        print(fanli_rmb)

                    except:
                        print('查询返利比例失败')
                        return '查询返利比例失败'

                    # 正在解析淘口令；
                    try:
                        url = "http://www.taokouling.com/index/taobao_tkljm/"
                        payload_JieXi = 'text=' + str(ShangPing_TKL)
                        response_JieXi = requests.post(url, data=payload_JieXi, headers=url_headers)
                        content_title = response_JieXi.json()['data']['content']  # 标题
                        content_picUrl = response_JieXi.json()['data']['picUrl']  # 头图
                        print('内容标题：' + content_title)

                        # 生成淘口令；
                        try:
                            url = "http://www.taokouling.com/index/tktaokouling/"
                            payload_TaoKouLing = 'url=' + yijian_click_url + '&tgdl=false&tkltitle=' + quote(
                                content_title.encode('utf-8')) + '&tklpic=' + content_picUrl + '&tkluserid=&undefined='
                            response_TaoKouLing = requests.post(url, data=payload_TaoKouLing, headers=url_headers)
                            TKL_num = response_TaoKouLing.json()['data'][0]['tkl']
                            print('返利金额：' + str(fanli_rmb) + ' 优惠券：' + str(quan_info) + ' 付费价格：' + str(price))
                            yang_url = 'https://yangshuhello01.gitee.io/yangshuf/YangShu.html?password=' + TKL_num.strip(
                                '￥') + '&url=' + yijian_click_url + '&MainPicture=' + content_picUrl

                            # 长链接转换为短链接；
                            try:
                                url_Conversion = 'http://www.taokouling.com/index/tbshorturl/'
                                payload_Conversion = 'url=' + quote(yang_url.encode('utf-8')) + '&type=' + '1'
                                res_Conversion = requests.post(url_Conversion, headers=url_headers,
                                                               data=payload_Conversion)
                                suo_url = res_Conversion.json()['data'][0]

                                # 运行保存函数；
                                save(UserName, NickName, CreateTime, fanli_rmb, quan_info, price, suo_url,
                                     content_title)
                                return '约返：' + str(fanli_rmb) + '元，优惠：' + str(quan_info) + '元，付费价：' + str(
                                    price) + '元；跳转链接：' + suo_url
                            except:
                                print('长链接转换失败')
                                return '长链接转换失败'

                        except:
                            print('生成淘口令运行异常')
                            return '生成淘口令运行异常'

                    except:
                        print('淘口令解析异常')
                        return '淘口令解析异常'

            except:
                print('查询返利金额运行异常')
                return '查询返利金额运行异常'


        except:
            print('淘口令一键转单运行异常')
            return '''◇ ◇ ◇ 返 利 失 败 ◇ ◇ ◇

Sorry!该商品无返利通道
建议更换其他同款商品查询

————————————

千万不要用淘金币！
千万不要用淘金币！
千万不要用淘金币！
'''



    else:   #默认11的为不带￥的淘口令
        ShangPing_TKL = msg['Text'].strip('￥')

        # 开始获取商品ID及获取返利链接，简述为一键转单；
        try:
            payload = 'tkl=' + ShangPing_TKL + '&zdgy=true&pid=' + pid + '&tkltitle=%20&tklpic=%20&tkluserid=%20&tgdl=true&undefined='
            url = 'http://www.taokouling.com/index/tbtkltoitemid/'
            url_res = requests.post(url, headers=url_headers, data=payload)
            yijian_itemid = url_res.json()['data']['itemid']
            yijian_click_url = url_res.json()['data']['url']
            print('商品ID：' + yijian_itemid)
            print('返利链接：' + yijian_click_url)

            # 开始获取返利金额及比例；
            try:
                url_FanLi_Price = 'http://www.taokouling.com/index/tbkitemget/'
                payload_url_FanLi_Price = 'itemid=' + yijian_itemid
                res_url_FanLi_Price = requests.post(url_FanLi_Price, headers=url_headers, data=payload_url_FanLi_Price)
                if 'quan_info' in res_url_FanLi_Price.json()['data']:
                    quan_info = re.findall('\d+', res_url_FanLi_Price.json()['data']['quan_info'])[1]  # 优惠券
                    price = float(res_url_FanLi_Price.json()['data']['price']) - float(quan_info)  # 付费价
                    # fanli_rmb = round((float(res_url_FanLi_Price.json()['data']['commission_rate']) * 0.01 * price), 2)  # 返利金额

                    # 通过高佣api获取返利比例；
                    try:
                        url_gaoyong_api = 'https://api.taokouling.com/tbk/TbkPrivilegeGet'
                        payload_gaoyong = {'itemid': yijian_itemid, 'siteid': siteid, 'adzoneid': adzoneid,
                                           'uid': uid}
                        res_gaoyong = requests.post(url_gaoyong_api, data=payload_gaoyong)
                        fanli_rmb = round((float(res_gaoyong.json()['result']['data']['max_commission_rate']) * 0.01 * price),
                                          2)  # 返利金额

                        print(quan_info)
                        print(price)
                        print(fanli_rmb)

                    except:
                        print('查询返利比例失败')
                        return '查询返利比例失败'

                    # 正在解析淘口令；
                    try:
                        url = "http://www.taokouling.com/index/taobao_tkljm/"
                        payload_JieXi = 'text=' + str(ShangPing_TKL)
                        response_JieXi = requests.post(url, data=payload_JieXi, headers=url_headers)
                        content_title = response_JieXi.json()['data']['content']  # 标题
                        content_picUrl = response_JieXi.json()['data']['picUrl']  # 头图
                        print('内容标题：' + content_title)

                        # 生成淘口令；
                        try:
                            url = "http://www.taokouling.com/index/tktaokouling/"
                            payload_TaoKouLing = 'url=' + yijian_click_url + '&tgdl=false&tkltitle=' + quote(
                                content_title.encode('utf-8')) + '&tklpic=' + content_picUrl + '&tkluserid=&undefined='
                            response_TaoKouLing = requests.post(url, data=payload_TaoKouLing, headers=url_headers)
                            TKL_num = response_TaoKouLing.json()['data'][0]['tkl']
                            print('返利金额：' + str(fanli_rmb) + ' 优惠券：' + str(quan_info) + ' 付费价格：' + str(price))
                            yang_url = 'https://yangshuhello01.gitee.io/yangshuf/YangShu.html?password=' + TKL_num.strip(
                                '￥') + '&url=' + yijian_click_url + '&MainPicture=' + content_picUrl

                            # 长链接转换为短链接；
                            try:
                                url_Conversion = 'http://www.taokouling.com/index/tbshorturl/'
                                payload_Conversion = 'url=' + quote(yang_url.encode('utf-8')) + '&type=' + '1'
                                res_Conversion = requests.post(url_Conversion, headers=url_headers,
                                                               data=payload_Conversion)
                                suo_url = res_Conversion.json()['data'][0]

                                # 运行保存函数；
                                save(UserName, NickName, CreateTime, fanli_rmb, quan_info, price, suo_url, content_title)
                                return '约返：' + str(fanli_rmb) + '元，优惠：' + str(quan_info) + '元，付费价：' + str(
                                    price) + '元；跳转链接：' + suo_url
                            except:
                                print('长链接转换失败')
                                return '长链接转换失败'

                        except:
                            print('生成淘口令运行异常')
                            return '生成淘口令运行异常'

                    except:
                        print('淘口令解析异常')
                        return '淘口令解析异常'

                else:
                    quan_info = 0
                    price = float(res_url_FanLi_Price.json()['data']['price'])  # 付费价
                    #fanli_rmb = round((float(res_url_FanLi_Price.json()['data']['commission_rate']) * 0.01 * price), 2)  # 返利金额

                    # 通过高佣api获取返利比例；
                    try:
                        url_gaoyong_api = 'https://api.taokouling.com/tbk/TbkPrivilegeGet'
                        payload_gaoyong = {'itemid': yijian_itemid, 'siteid': siteid, 'adzoneid': adzoneid,
                                           'uid': uid}
                        res_gaoyong = requests.post(url_gaoyong_api, data=payload_gaoyong)
                        fanli_rmb = round((float(res_gaoyong.json()['result']['data']['max_commission_rate']) * 0.01 * price),
                                          2)  # 返利金额

                        print(quan_info)
                        print(price)
                        print(fanli_rmb)

                    except:
                        print('查询返利比例失败')
                        return '查询返利比例失败'

                    # 正在解析淘口令；
                    try:
                        url = "http://www.taokouling.com/index/taobao_tkljm/"
                        payload_JieXi = 'text=' + str(ShangPing_TKL)
                        response_JieXi = requests.post(url, data=payload_JieXi, headers=url_headers)
                        content_title = response_JieXi.json()['data']['content']  # 标题
                        content_picUrl = response_JieXi.json()['data']['picUrl']  # 头图
                        print('内容标题：' + content_title)

                        # 生成淘口令；
                        try:
                            url = "http://www.taokouling.com/index/tktaokouling/"
                            payload_TaoKouLing = 'url=' + yijian_click_url + '&tgdl=false&tkltitle=' + quote(
                                content_title.encode('utf-8')) + '&tklpic=' + content_picUrl + '&tkluserid=&undefined='
                            response_TaoKouLing = requests.post(url, data=payload_TaoKouLing, headers=url_headers)
                            TKL_num = response_TaoKouLing.json()['data'][0]['tkl']
                            print('返利金额：' + str(fanli_rmb) + ' 优惠券：' + str(quan_info) + ' 付费价格：' + str(price))
                            yang_url = 'https://yangshuhello01.gitee.io/yangshuf/YangShu.html?password=' + TKL_num.strip(
                                '￥') + '&url=' + yijian_click_url + '&MainPicture=' + content_picUrl

                            # 长链接转换为短链接；
                            try:
                                url_Conversion = 'http://www.taokouling.com/index/tbshorturl/'
                                payload_Conversion = 'url=' + quote(yang_url.encode('utf-8')) + '&type=' + '1'
                                res_Conversion = requests.post(url_Conversion, headers=url_headers,
                                                               data=payload_Conversion)
                                suo_url = res_Conversion.json()['data'][0]

                                # 运行保存函数；
                                save(UserName, NickName, CreateTime, fanli_rmb, quan_info, price, suo_url,
                                     content_title)
                                return '约返：' + str(fanli_rmb) + '元，优惠：' + str(quan_info) + '元，付费价：' + str(
                                    price) + '元；跳转链接：' + suo_url

                            except:
                                print('长链接转换失败')
                                return '长链接转换失败'

                        except:
                            print('生成淘口令运行异常')
                            return '生成淘口令运行异常'

                    except:
                        print('淘口令解析异常')
                        return '淘口令解析异常'

            except:
                print('查询返利金额运行异常')
                return '查询返利金额运行异常'

        except:
            print('淘口令一键转单运行异常')
            return '''◇ ◇ ◇ 返 利 失 败 ◇ ◇ ◇

Sorry!该商品无返利通道
建议更换其他同款商品查询

————————————

千万不要用淘金币！
千万不要用淘金币！
千万不要用淘金币！
'''

    #itchat.send_msg('111')

    #return ret

itchat.auto_login(hotReload=True)
itchat.run()