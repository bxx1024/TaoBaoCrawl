# -*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
import GetIPProxy as GetIPProxy
import os, time, random


def get_ip_prroxy_list():
    proxy_ip_list = GetIPProxy.get_proxy_ip()
    proxy_ip_list= [term[0]+ ":" +  str(term[1]) for term in proxy_ip_list]
    return proxy_ip_list

def get_comment(product_url, comment_path):
    try:
        proxies = get_ip_prroxy_list()
        proxy = Proxy({'proxyType': ProxyType.MANUAL, 'httpProxy': random.choice(proxies)})
        # option = webdriver.FirefoxOptions()
        # option.set_headless() firefox_options = option,
        driver = webdriver.Firefox(proxy = proxy, executable_path='geckodriver')
        driver.set_page_load_timeout(60)
        driver.get(product_url)
        WebDriverWait(driver, 100, 5).until(lambda driver: driver.find_element_by_xpath("//div[@class = 'tb-tabbar-inner-wrap']/ul[@class = 'tb-tabbar tb-clear']/li/a[@class = 'tb-tab-anchor']"))
    except Exception as e:
        print(e)
    else:
        try:
            driver.find_elements_by_xpath("//div[@class = 'tb-tabbar-inner-wrap']/ul[@class = 'tb-tabbar tb-clear']/li/a[@class = 'tb-tab-anchor']")[1].click()
            WebDriverWait(driver, 10, 5).until(lambda driver: driver.find_elements_by_xpath("//div[@class = 'kg-rate-detail']"))

            num = 0
            with open(comment_path, "wb") as file2:
                while True:
                    try:
                        for term in driver.find_elements_by_xpath("//div[@class = 'review-details']"):
                            try:
                                term.find_elements_by_xpath("li[@class = 'photo-item']/img")
                            except:
                                pass
                            file2.write(("ProductComment:" + str(num) + "\n").encode("utf-8"))
                            file2.write((term.text + "\n").encode("utf-8"))
                            num += 1
                        driver.find_element_by_xpath( "//li[@class = 'pg-next']").click()
                        time.sleep(2)
                    except Exception as e:
                        print("e1:", e)
                        break
        except Exception as e:
            print("e2:", e)
    try:
        driver.quit()
    except Exception as e:
        print("e3:", e)

def get_product_comment(initional_url, id_dir, information_dir):
    for big_class in range(0, 100):
        for small_class in range(0, 100):
            id_path = id_dir + "/" + str(big_class) + "/" + str(small_class) + "/" + str(big_class) + "_" + str(small_class) + "_id.txt"
            print(id_path)
            if os.path.exists(id_path):
                if not os.path.exists(information_dir + "/" + str(big_class) + "/" + str(small_class) + "/"):
                    os.makedirs(information_dir + "/" + str(big_class) + "/" + str(small_class) + "/")
                with open(id_path, "rb") as file1:
                    for product_id in file1.readlines():
                        product_id = product_id.decode('utf-8').strip()
                        comment_path = information_dir + "/" + str(big_class) + "/" + str(small_class) + "/" + str(big_class) + "_" + str(small_class) + "_" + product_id + "_comment.txt"
                        if not os.path.exists(comment_path):
                            product_id_url = initional_url.format(product_id=product_id)
                            print(product_id_url)
                            get_comment(product_id_url, comment_path)
            else:
                break

if __name__ == "__main__":
    initional_url = "https://item.taobao.com/item.htm?id={product_id}"
    get_product_comment(initional_url, "./ProductIdGet/ProductClassUrl", "D:/ProductCommentGet/ProductComment")
