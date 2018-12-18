import os, random, json, time,  socket
import urllib.request as request
import GetIPProxy
import urllib.error
import http.client

socket.setdefaulttimeout(20)
def get_ip_prroxy_list():
    proxy_ip_list = GetIPProxy.get_proxy_ip()
    proxy_ip_list= [term[0]+ ":" +  str(term[1]) for term in proxy_ip_list]
    return proxy_ip_list

def getHtml(url, proxies):
    proxy_support = request.ProxyHandler({"http":random.choice(proxies)})
    opener = request.build_opener(proxy_support)
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
    request.install_opener(opener)
    return request.urlopen(url).read()


def get_information(product_id_url, proxies):
    for i in range(0, 100):
        try:
            html = getHtml(product_id_url, proxies)
            dict_data = json.loads(html.decode("utf-8")[20: -1:])["data"]
            title = dict_data["item"]["title"]
            image = dict_data["item"]["images"]
            categoryId = dict_data["item"]["categoryId"]
            price = json.loads(dict_data["mockData"])["price"]["price"]["priceText"]
            base_infor = dict_data["props"]["groupProps"][0]
            shop_infor = dict_data["seller"]
            return title, image, categoryId, price, base_infor, shop_infor
        except KeyError as e:
            time.sleep(5)
        except json.decoder.JSONDecodeError as e:
            time.sleep(5)
        except UnicodeDecodeError as e:
            time.sleep(5)
        except urllib.error.URLError as e:
            time.sleep(5)
        except http.client.RemoteDisconnected as e:
            time.sleep(5)
        except socket.timeout as e:
            time.sleep(5)

def get_product_information(initional_url, id_dir, information_dir):
    for big_class in range(0, 100):
        if os.path.exists(id_dir + "/" + str(big_class)):
            proxies = get_ip_prroxy_list()
            for small_class in range(0, 100):
                if os.path.exists(id_dir + "/" + str(big_class) + "/"  + str(small_class) + "/" + str(big_class) + "_" + str(
                        small_class) + "_id.txt"):
                    if not os.path.exists(information_dir + "/" + str(big_class) + "/"  + str(small_class) + "/"):
                        os.makedirs(information_dir + "/"  + str(big_class) + "/"  + str(small_class) + "/")
                    with open(id_dir + "/" + str(big_class) + "/"+ str(small_class) + "/"  + str(big_class) + "_"  + str(
                        small_class) + "_id.txt", "rb") as file1:
                        for product_id in file1.readlines():
                            product_id = product_id.decode('utf-8').strip()
                            if not os.path.exists(information_dir + "/" + str(
                                    big_class) + "/" + str(small_class) + "/" + str(big_class) + "_" + str(
                                    small_class) + "_" + product_id + "_infor.txt"):
                                print(product_id)
                                product_id_url = initional_url.format(time = int(time.time() * 1000), product_id = product_id)

                                with open(information_dir + "/" + str(big_class) + "/"  + str(small_class) + "/" + str(big_class) + "_" + str(
                            small_class) + "_" + product_id + "_infor.txt", "wb") as file2:
                                    try:
                                        title, image, categoryId, price, base_infor, shop_infor = get_information(product_id_url, proxies)
                                        file2.write(("Title:" + title + "\n").encode("utf-8"))
                                        file2.write(("Image:" + str(image) + "\n").encode("utf-8"))
                                        file2.write(("CategoryId:" + categoryId + "\n").encode("utf-8"))
                                        file2.write(("Price:" + str(price) + "\n").encode("utf-8"))
                                        file2.write(("Information:" + str(base_infor) + "\n").encode("utf-8"))
                                        file2.write(("ShopInformation:" + str(shop_infor) + "\n").encode("utf-8"))
                                        time.sleep(3)
                                    except TypeError as e:
                                        continue
                else:
                    break
        else:
            break


if __name__ == "__main__":
    initional_url ="https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?" \
                   "type=jsonp&" \
                   "api=mtop.taobao.detail.getdetail&" \
                   "v=6.0&" \
                   "ttid=324%40taobao_iphone_6.0.0&" \
                   "appKey=12574478&" \
                   "data=%7B%22itemNumId%22%3A%22{product_id}%22%7D&" \
                   "t={time}&" \
                   "sign=&" \
                   "callback=mn1cb1{time}"
    get_product_information(initional_url, "./ProductIdGet/ProductClassUrl", "./ProductInformationGet/ProductInformation/")
