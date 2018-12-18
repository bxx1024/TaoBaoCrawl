import os, re, random, time
import GetIPProxy
import urllib.request as request

product_id = re.compile(r"_(\d{2,20})_")
product_image = re.compile(r'Image:(.*)')

def get_ip_prroxy_list():
    proxy_ip_list = GetIPProxy.get_proxy_ip()
    proxy_ip_list= [term[0]+ ":" +  str(term[1]) for term in proxy_ip_list]
    return proxy_ip_list

def get_image(product_image, path, proxies):
    proxy_support = request.ProxyHandler({"http":random.choice(proxies)})
    opener = request.build_opener(proxy_support)
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
    try:
        request.install_opener(opener)
        request.urlretrieve(product_image, path)
    except:
        pass

def get_product_image(product_image_list, product_image_dir, proxies):

    #for product_num, product_image_part in enumerate(product_image_list):
    try:
        product_image_part = product_image_list[0]
        path = product_image_dir + str(0) + ".jpg"
        product_image = "https:" + product_image_part[2:-1:]
        get_image(product_image, path, proxies)
        time.sleep(1)
    except:
        pass


def save_infor(information_dir, image_dir):
    for big_class in range(0, 100):
        for small_class in range(0, 100):
            proxies = get_ip_prroxy_list()
            product_dir = information_dir + "/" + str(big_class) + "/" + str(small_class)
            if os.path.exists(product_dir):
                print(product_dir)
                for product_path in os.listdir(product_dir):
                    product_id_get = product_id.search(product_path).group(1)

                    product_path = product_dir  + "/" + product_path
                    with open(product_path, "rb") as file1:
                        for line in file1.readlines():
                            product_image_match = product_image.match(line.decode("utf-8"))
                            if product_image_match:
                                product_image_list = product_image_match.group(1)
                                product_image_list = product_image_list[0:-1].split(",")
                                product_image_dir = image_dir + str(big_class) + "/" + str(small_class) + "/" + str(big_class) + "_" + str(small_class) + "_" + product_id_get + "_" + "image/"
                                if not os.path.exists(product_image_dir):
                                    print(product_id_get)
                                    os.makedirs(product_image_dir)
                                    get_product_image(product_image_list, product_image_dir, proxies)


            else:
                break


if __name__ == "__main__":
    save_infor("./ProductInformationGet/ProductInformation", "F:/ProductImage/")