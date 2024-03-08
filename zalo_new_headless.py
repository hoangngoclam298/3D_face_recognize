from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import base64
import eventlet
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from PIL import Image
import time
from io import BytesIO
import base64
import os
import traceback
from selenium.webdriver.common.action_chains import ActionChains
import random
import zipfile
import regex as re
from bs4 import BeautifulSoup
import shutil
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QMimeData, QUrl
from selenium.common.exceptions import NoSuchElementException
import unicodedata
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

autoit_semaphore = eventlet.semaphore.Semaphore()

dict_proxy = {"103.82.133.213:13501:sp08-13501:PBTQX":True, "103.82.133.213:13519:sp08-13519:IDRMW":True}
dict_driver = {}
dict_status_zalo = {}
dict_status_update_data_chat = {}
dict_status_update_list_chat = {}
dict_id_zalo = {}
dict_zalo_online = {}
folder_data_zalo = r'C:\Zalo_server\data'
dict_folder_zalo = {}

dict_tag_label = {
        'color: rgb(217, 27, 27);':0,
        'color: rgb(243, 27, 200);':1,
        'color: rgb(255, 105, 5);':2,
        'color: rgb(250, 192, 0);':3,
        'color: rgb(75, 195, 119);':4,
        'color: rgb(42, 197, 187);':5,
        'color: rgb(0, 104, 255);':6,
        'color: rgb(111, 63, 207);':7
}

list_icon_s = [':)', ':~', ':b', ":')", '8-)', ':-((', ':$', ':3', ':z', ':((', '&-(', ':-h', ':p', ':d', ':o', ':(', ';-)', '--b', ':))', ':-*', ';p', ';-d', '/-showlove', ';d', ';o', ';g', '|-)', ':!', ':l', ':>', ':;', ';f', ':v', ':wipe', ':-dig', ':handclap', 'b-)', ':-r', ':-<', ':-o', ';-s', ';?', ';-x', ':-f', '8*)', ';!', ';-!', ';xx', ':-bye', '>-|', 'p-(', ':--|', ':q', 'x-)', ':*', ';-a', '8*', ':|', ':x', ':t', ';-/', ':-l', '$-)', '/-beer', '/-coffee', '/-rose', '/-fade', '/-bd', '/-bome', '/-cake', '/-heart', '/-break', ':-bye', '>-|', 'p-(', ':--|', ':q', 'x-)', ':*', ';-a', '8*', ':|', ':x', ':t', ';-/', ':-l', '$-)', '/-beer', '/-coffee', '/-rose', '/-fade', '/-bome', '/-cake', '/-heart', '/-break', '/-li', '/-flag', '/-strong', '/-weak', '/-ok', '/-v', '/-thanks', '/-punch', '/-share', '_()_', '/-no', '/-bad', '/-loveu']
list_icon_s = [':)', ':~', ':b', ":')", '8-)', ':-((', ':$', ':3', ':z', ':((', '&-(', ':-h', ':p', ':d', ':o', ':(', ';-)', '--b', ':))', ':-*', ';p', ';-d', ';d', ';o', ';g', '|-)', ':!', ':l', ':>', ':;', ';f', ':v', 'b-)', ':-r', ':-<', ':-o', ';-s', ';?', ';-x', ':-f', '8*)', ';!', ';-!', ';xx', ':-bye', '>-|', 'p-(', ':--|', ':q', 'x-)', ':*', ';-a', '8*', ':|', ':x', ':t', ';-/', ':-l', '$-)', '>-|', 'p-(', ':--|', ':q', 'x-)', ':*', ';-a', '8*', ':|', ':x', ':t', ';-/', ':-l', '$-)']

def filter_bmp(input_string):
    bmp_string = ''
    for char in input_string:
        if ord(char) <= 0xFFFF:
            bmp_string += char
    return bmp_string

def click_element(driver, key, value, times = 5, sleep_time = 0.5):
    for timet in range(times):
        try:
            element_to_click = driver.find_element(key, value)
            element_to_click.click()
            return True
        except:
            print("k click element")
        eventlet.sleep(sleep_time)
    print(key, value)
    return False

def get_element(driver, key, value, times = 5, sleep_time = 0.5):
    for timet in range(times):
        try:
            element = driver.find_element(key, value)
            return element
        except:
            print("k get element")
        eventlet.sleep(sleep_time)
    print(key, value)
    return None

def get_elements(driver, key, value, times = 5, sleep_time = 0.5):
    for timet in range(times):
        try:
            element = driver.find_elements(key, value)
            return element
        except:
            print("k get elements")
        eventlet.sleep(sleep_time)
    print(key, value)
    return None

def latest_download_file(num_file, path):
    while True:
        # Lấy danh sách các tệp trong thư mục
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        # Đợi cho tệp được tải xuống
        if len(files) <= num_file:
            eventlet.sleep(0.2)
            print('Waiting for download to be initiated...')
        else:
            # Sắp xếp các tệp dựa trên thời gian sửa đổi
            newest = sorted(files, key=lambda x: os.path.getmtime(os.path.join(path, x)))[-1]
            if ".crdownload" in newest or ".tmp" in newest:
                eventlet.sleep(0.5)
                print('Waiting for download to complete...')
            else:
                # Tạo đường dẫn tuyệt đối và trả về
                absolute_path = os.path.join(path, newest)
                print('Absolute path:', absolute_path)
                return absolute_path

def copy_file_to_clipboard(file_path):
    mime_data = QMimeData()
    url = QUrl.fromLocalFile(file_path)
    mime_data.setUrls([url])
    app = QApplication([])
    app.clipboard().setMimeData(mime_data)

def base64_to_image(base64_string, output_path):
    try:
        imgstr = base64_string.split(';base64,')[-1]
        image_data = BytesIO(base64.b64decode(imgstr))
        img = Image.open(image_data)
        img.save(output_path)
        print(f"Đã lưu hình ảnh vào {output_path}")
    except Exception as e:
        traceback.print_exc()

def get_file_content_chrome(driver, uri):
    result = driver.execute_async_script("""
        var uri = arguments[0];
        var callback = arguments[1];
        var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
        var xhr = new XMLHttpRequest();
        xhr.responseType = 'arraybuffer';
        xhr.onload = function(){ callback(toBase64(xhr.response)) };
        xhr.onerror = function(){ callback(xhr.status) };
        xhr.open('GET', uri);
        xhr.send();
        """, uri)
    if type(result) == int :
        raise Exception("Request failed with status %s" % result)
    return result

# lay thong tin trong chat
def get_data_chat_boxes(div_child, id_driver, new_id = False):
    data_chat_boxes = []
    boxes = div_child.find_all('div', {'data-node-type': 'bubble-message'})
    # print(len(boxes))
    for box in boxes:
        # print('box: ')
        chat_box = {"id": box.get('id')}
        if new_id:
            if chat_box['id'] not in new_id:
                continue
        data_chat_box = []
        # tim cac the text, sticker, image, file
        items = box.find_all(lambda tag: tag.name == 'div' and 
        (tag.get('class') and 
        ('chatImageMessage' in ' '.join(tag.get('class')) 
        or 'file-message card--file' in ' '.join(tag.get('class'))
        or 'card card-with-reaction-v2' in ' '.join(tag.get('class')))))
        try:
            time_line = box.find(lambda tag: tag.name == 'span-13' and 
            (tag.get('class') and 
            ('card-send-time__sendTime' in ' '.join(tag.get('class'))))).text
        except:
            time_line = ''
        # print(time_line)
        for item in items:
            # print("item: ")
            try:
                text_item = item.find('span-15').text
                # print("text item:", text_item)
                if text_item.endswith(time_line) and time_line != "":
                    if text_item == time_line:
                        text_item = ''
                    else:
                        text_item = text_item[:-len(time_line)].rstrip()
            except:
                text_item = ''
            if text_item and text_item != "":
                try:
                    reply_div = item.find('div', class_='rel quote-banner')
                    if reply_div:
                        name_reply = reply_div.find('div', class_="truncate quote-name").text 
                        text_reply = reply_div.find('div', class_="quote-text truncate").text
                        thumbnail = reply_div.find('img', class_='quote-banner-thumb')
                        if thumbnail:
                            data_chat_box.append({"time":time_line,"type":"text", "data":[text_item], "reply":{"name":name_reply, 'type':'sticker', 'thumbnail': thumbnail.get('src'), "data":text_reply}})
                        else:
                            data_chat_box.append({"time":time_line,"type":"text", "data":[text_item], "reply":{"name":name_reply, 'type':'text', 'thumbnail':'', "data":text_reply}})
                    else:
                        reply_image = item.find('div', class_='rel quote-banner quote-banner__photo')
                        if reply_image:
                            name_reply = reply_image.find('div', class_="truncate quote-name").text 
                            text_reply = reply_image.find('div', class_="quote-text truncate").text
                            thumbnail_blob = reply_image.find('img', {'data-z-element-type': 'image'}).get('data-drag-src')
                            thumbnail = get_file_content_chrome(dict_driver[id_driver], thumbnail_blob)
                            data_chat_box.append({"time":time_line,"type":"text", "data":[text_item], "reply":{"name":name_reply, 'type':'image', 'thumbnail': thumbnail, "data":text_reply}})
                        else:
                            reply_file = item.find('div', class_='quote-base quote-base--scroll-on quote-file rel')
                            if reply_file:
                                name_reply = reply_file.find('div', class_="truncate quote-name").text 
                                text_reply = reply_file.find('div', class_="quote-text truncate").text
                                style_value = reply_file.find('div', class_='svg-icon svg-icon--size-medium file-icon file-icon--size-medium').get('style')
                                thumbnail = r'https://chat.zalo.me/' + re.search(r"url\((.*?)\)", style_value).group(1).strip('"')
                                data_chat_box.append({"time":time_line,"type":"text", "data":[text_item], "reply":{"name":name_reply, 'type':'file', 'thumbnail': thumbnail, "data":text_reply}})
                            else:
                                image_tag = item.find('img', {'data-z-element-type': 'image'})
                                if image_tag:
                                    url_blob = image_tag.get("src")
                                    path_id_folder = dict_folder_zalo[id_driver]
                                    download_folder = os.path.join(path_id_folder, 'download')
                                    path_save_image = os.path.join(download_folder, f'image_{time.time()}.png')
                                    base64_to_image(get_file_content_chrome(dict_driver[id_driver], url_blob), path_save_image)
                                    data_chat_box.append({"time":time_line,"type":"text","data":[text_item], 'isTagImage': True, "link_image":path_save_image})
                                else:
                                    data_chat_box.append({"time":time_line,"type":"text","data":[text_item]})
                except:
                    # print(item)
                    # traceback.print_exc()
                    pass
            else:
                try:
                    if not item.get("data-id"):
                        stickers_ele = item.find_all('div', class_='sticker sticker-message')
                        url_pattern = r'url\("([^"]+)"\)'
                        stickers = [re.findall(url_pattern, sticker_ele.get("style"))[0] for sticker_ele in stickers_ele]
                        if(len(stickers) != 0):
                            data_chat_box.append({"time":time_line,"type":"sticker","data":stickers})
                except:
                    pass
                try:
                    images = item.find_all('img', {'data-z-element-type': 'image'})
                    src_image = [image.get("src") for image in images]
                    if(len(src_image) != 0):
                        list_link_local = []
                        for url_blob in src_image:
                            try:
                                path_id_folder = dict_folder_zalo[id_driver]
                                download_folder = os.path.join(path_id_folder, 'download')
                                path_save_image = os.path.join(download_folder, f'image_{time.time()}.png')
                                base64_to_image(get_file_content_chrome(dict_driver[id_driver], url_blob), path_save_image)
                                list_link_local.append(path_save_image)
                            except:
                                traceback.print_exc()
                        data_chat_box.append({"time":time_line,"type":"image","data":list_link_local})
                except:
                    # print('bat duoc trong try')
                    traceback.print_exc()
                    pass
                try:
                    chat_files = item.find_all('div-b14', class_ = 'file-message__content-title')
                    if(len(chat_files) != 0):
                        name_files = [chat_file.get("title") for chat_file in chat_files]
                        data_chat_box.append({"time":time_line, "type":"file", 'name_files': name_files, "file_path":['']})
                except:
                    traceback.print_exc()
                    pass
                try:
                    if item.find('span', attrs={'data-translate-inner': ["STR_UNDO_MSG", "STR_RECALLED"]}):
                        data_chat_box.append({"time":time_line,"type":"text","data":["Tin nhắn đã được thu hồi"],"IsRecall":True})
                except:
                    pass
        chat_box["data_chat_box"] = data_chat_box
        # print(data_chat_box)
        data_chat_boxes.append(chat_box)
    return data_chat_boxes

def get_data_chat_all_block_date(soup, id_driver, new_id = False):
    block_dates = soup.find_all('div', class_='block-date')
    data_all_block_date = []
    for div_block_date in block_dates:
        data_chat_block_date = {}
        data_mess_chat = []
        data_block_date = [child for child in div_block_date.children if child.name == 'div']
        for div_child in data_block_date:
            if div_child.get('class'):
                class_name = ' '.join(div_child.get('class'))
                if  class_name == 'chat-date --time island':
                    time_block_date = div_child.text
                    data_chat_block_date["time_block_date"] = time_block_date.rstrip()
                elif class_name == 'chat-item flx me':
                    chat_boxes = {"actor": {}}
                    chat_boxes["data"] = get_data_chat_boxes(div_child, id_driver, new_id)
                    data_mess_chat.append(chat_boxes)
                elif class_name == 'chat-item flx':
                    chat_boxes = {"actor": {"name": '', "ava": ''}}
                    ava_sender = div_child.find("div", class_="rel zavatar-container avatar--overlay").find('img', class_='a-child')
                    if ava_sender:
                        chat_boxes['actor']['ava'] = ava_sender.get('src')
                    name_sender = div_child.find("div-13", class_="card-sender-name")
                    if name_sender:
                        chat_boxes['actor']['name'] = name_sender.text
                    chat_boxes["data"] = get_data_chat_boxes(div_child, id_driver, new_id)
                    data_mess_chat.append(chat_boxes)
            else:
                event_message_div = div_child.find(class_=lambda x: x and ("event-message" in x.split() or "message-info" in x.split()))
                if event_message_div:
                    event_message_div = event_message_div.text.rstrip()
                    # print(event_message_div)
        data_chat_block_date['data_chat_block_date'] = data_mess_chat
        data_all_block_date.append(data_chat_block_date)
        # print(data_all_block_date)
    return data_all_block_date

def get_id_chat_boxes(div_child):
    id_chat_boxes = []
    boxes = div_child.find_all('div', {'data-node-type': 'bubble-message'})
    for box in boxes:
        id_chat_boxes.append(box.get('id'))
    return id_chat_boxes

def get_id_chat_all_block_date(soup):
    block_dates = soup.find_all('div', class_='block-date')
    id_all_block_date = []
    for div_block_date in block_dates:
        data_block_date = [child for child in div_block_date.children if child.name == 'div']
        for div_child in data_block_date:
            if div_child.get('class'):
                class_name = ' '.join(div_child.get('class'))
                if class_name == 'chat-item flx me':
                    id_all_block_date += get_id_chat_boxes(div_child)
                elif class_name == 'chat-item flx':
                    id_all_block_date += get_id_chat_boxes(div_child)
    return id_all_block_date

def get_list_friend_by_bs4(id_driver):
    check_f5 = True
    while check_f5:
        ts1 = time.time()
        click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[1]", times=3, sleep_time=0.2)
        click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[2]", times=3, sleep_time=0.2)
        click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[2]/div[3]/div/div[1]", times=3, sleep_time=0.2)
        set_data = set()
        sorted_list = []
        dict_driver[id_driver].execute_script("document.body.style.zoom='0.1%'")
        eventlet.sleep(2)
        print("click + zoom", time.time() - ts1)
        ts = time.time()
        try:
            html_content = get_element(dict_driver[id_driver], "xpath", '//*[@id="container"]/div[3]/div[2]/div/div[1]/div', times=10, sleep_time=0.5).get_attribute('outerHTML')
            break
        except:
            dict_driver[id_driver].get("https://chat.zalo.me/")
            continue
    print("get html", time.time() - ts)
    ts = time.time()
    soup = BeautifulSoup(html_content, 'html.parser').find('div', class_='contact-tab-v2__scrollbar-custom')
    print("tim the tong", time.time() - ts)
    ts = time.time()
    friend_info_divs = soup.find_all('div', class_='friend-info')
    print(len(friend_info_divs))
    print("tim the con", time.time() - ts)
    ts = time.time()
    for div in friend_info_divs:
        img_src = ''
        friend_name = ''
        img_tag = div.find('img', class_='a-child')
        if img_tag:
            img_src = img_tag['src'] 
        span_tag = div.find('span', class_='name')
        if span_tag:
            friend_name = span_tag.text
        # set_data.add((friend_name, img_src))
        sorted_list.append((friend_name, img_src))
    print("lấy data the con", time.time() - ts)
    ts = time.time()
    dict_driver[id_driver].execute_script("document.body.style.zoom='100%'")
    # sorted_list = sorted(set_data, key=lambda x: x[0])
    print("sort list friend", time.time() - ts)
    print("all time list friend", time.time() - ts1)
    return sorted_list
    
def get_list_group_by_bs4(id_driver):
    click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[1]")
    click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[2]")
    click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[2]/div[3]/div/div[2]")
    eventlet.sleep(2)
    dict_driver[id_driver].execute_script("document.body.style.zoom='0.1%'")
    eventlet.sleep(1)
    
    html_text = dict_driver[id_driver].find_element("xpath",'//*[@id="container"]/div[3]/div[2]/div/div[1]/div').get_attribute('outerHTML')
    soup = BeautifulSoup(html_text, 'html.parser')
    friend_info_divs = soup.find_all('div', class_='friend-info')
    list_group = []
    for div in friend_info_divs:
        img_src = ''
        target_div = div.find('div', class_=lambda x: x and x.startswith('zavatar zavatar-l zavatar-single'))
        if target_div:
            img_tag = target_div.find('img', class_='a-child')
            if img_tag:
                img_src = img_tag['src'] 
        
        name = div.find('span', class_='name').text.strip()
        members = div.find('a', class_='description left members').text.strip()
        list_group.append({'name':name, 'members':members, 'img_src':img_src})
    return list_group

def forward_list_zalo(id_driver, id_message, list_zalo):
    try:
        len_sub_list = 99
        sub_lists = [list_zalo[i:i + len_sub_list] for i in range(0, len(list_zalo), len_sub_list)]
        for sub_list_zalo in sub_lists:
            element = get_element(dict_driver[id_driver], 'xpath', f'//*[@id="{id_message}"]')
            actions = ActionChains(dict_driver[id_driver])
            actions.move_to_element(element).perform()
            click_element(dict_driver[id_driver], 'xpath','//*[@id="messageViewContainer"]/div[1]/div[1]/div[@data-translate-title="STR_FORWARD_MSG"]/i')
            for zalo_forward in sub_list_zalo:
                name, ava = zalo_forward['name'], zalo_forward['ava']
                name_check_see = unicodedata.normalize('NFKD', name).encode('utf-8', 'ignore').decode('utf-8')
                tim_kiem = get_element(dict_driver[id_driver], 'xpath','//*[@id="group-creator"]/div[1]/span/input')
                tim_kiem.send_keys(Keys.CONTROL, 'a')
                tim_kiem.send_keys(filter_bmp(name))
                eventlet.sleep(0.5)
                check_see = True
                last_div = None
                while check_see:
                    elements = dict_driver[id_driver].find_elements("xpath", "//div[@data-id='div_FWD_CTItem']")
                    for contact_div in elements:
                        try:
                            soup = BeautifulSoup(contact_div.get_attribute('outerHTML'), "html.parser")
                            div_element = soup.find("div", class_="create-group__item")
                            try:
                                img_src = div_element.find("img")["src"]
                            except:
                                img_src = ''
                            try:
                                name = div_element.find(class_="create-group__item__name").text
                            except:
                                name = ''
                            if img_src == ava:
                                if unicodedata.normalize('NFKD', name).encode('utf-8', 'ignore').decode('utf-8') == name_check_see:
                                    print("đã thấy")
                                    contact_div.click()
                                    check_see = False
                                    break
                        except:
                            traceback.print_exc()
                            continue
                    if len(elements) == 0:
                        check_see = False
                    if check_see:
                        if last_div == elements[-1]:
                            check_see = False
                        else:
                            last_div = elements[-1]
                            print("Vẫn chưa tới cuối")
                            actions = ActionChains(dict_driver[id_driver])
                            actions.move_to_element(last_div).perform()
                            eventlet.sleep(0.1)
            click_element(dict_driver[id_driver], 'xpath', '//div[@data-translate-inner="STR_FORWARD"]')
    except:
        traceback.print_exc()
    try:
        click_element(dict_driver[id_driver], 'xpath', '//div[@data-translate-inner="STR_CANCEL"]', times = 1)
    except:
        pass
    return None

@app.route('/')
def index():
    return "Server ok!"

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('join')
def handle_join(data):
    room = data['id_chat']
    # global folder_data_zalo
    # folder_data_zalo = data['folder_data_zalo']
    # os.makedirs(os.path.join(folder_data_zalo, 'data'), exist_ok=True)
    join_room(room)
    print(f"Client {request.sid} joined room {room}")

@socketio.on('leave')
def handle_leave(data):
    room = data['id_chat']
    leave_room(room)
    print(f"Client {request.sid} left room {room}")

@socketio.on('logout_zalo')
def handle_logout_zalo(data):
    room = data['id_chat']
    id_driver = data['id_zalo']
    if id_driver in dict_driver and room in dict_zalo_online:
        if id_driver in dict_zalo_online[room]:
            dict_driver[id_driver].quit()
            del dict_zalo_online[room][id_driver]
        if id_driver in dict_driver:
            del dict_driver[id_driver]
        if id_driver in dict_status_zalo:
            del dict_status_zalo[id_driver] 

@socketio.on('download_file')
def handle_download_file(data):
    room = data['id_chat']
    id_driver = data['id_zalo']
    id_message_file = data['id_mess_file']
    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        if(dict_status_zalo[id_driver] != ''):
            print("bận rồi !!!", dict_status_zalo[id_driver])
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            path_id_folder = dict_folder_zalo[id_driver]
            download_folder = os.path.join(path_id_folder, 'download')
            before_download_num_file = len(os.listdir(download_folder))
            file_path_download = ''
            dict_status_zalo[id_driver] = "download_file"
            if click_element(dict_driver[id_driver], 'xpath', f'//*[@id="{id_message_file}"]/div/div[2]/div[1]/div-13/div[2]/div-13/div[2]/a/i', times=10, sleep_time=0.5):
                dict_status_zalo[id_driver] = ""
                file_path_download = latest_download_file(before_download_num_file, download_folder)
                emit('result_download', {"result":'success', 'id_zalo':id_driver, 'id_mess_file':id_message_file, 'link_file':file_path_download},room=room)
            else:
                emit('result_download', {"result":'fail', 'id_zalo':id_driver, 'id_mess_file':id_message_file, 'link_file':file_path_download},room=room)
            dict_status_zalo[id_driver] = ""

@socketio.on('get_list_zalo')
def handle_get_list_zalo(data):
    room = data['id_chat']
    # print("dict_zalo_online luc day :", dict_zalo_online)
    eventlet.sleep(0)
    if room in dict_zalo_online:
        result = []
        for id_zalo in dict_zalo_online[room]:
            tmp = {}
            tmp['id_zalo'] = id_zalo
            tmp['name'] = dict_zalo_online[room][id_zalo]['name']
            tmp['ava'] = dict_zalo_online[room][id_zalo]['ava']
            tmp['num_phone_zalo'] = dict_zalo_online[room][id_zalo]['num_phone_zalo']
            tmp['list_friend'] = dict_zalo_online[room][id_zalo]['list_friend']
            result.append(tmp)
        emit("list_zalo", {"list_zalo": result}, room=room)
        print(room, 'emit xong list_zalo')
    else:
        emit("list_zalo", {"list_zalo": []}, room=room)
        print(room, 'chua dang nhap')

@socketio.on('get_list_friend')
def handle_get_list_friend(data):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        if(dict_status_zalo[id_driver] != ''):
            print("bận rồi !!!", dict_status_zalo[id_driver])
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            dict_status_zalo[id_driver] = "get_list_friend"        
            sorted_list = get_list_friend_by_bs4(id_driver)
            result = []
            for index, (name, ava) in enumerate(sorted_list):
                tmp = {}
                tmp['id'] = str(index).zfill(6)
                tmp['name'] = name
                tmp['ava'] = ava
                result.append(tmp)
            dict_zalo_online[room][id_driver]["list_friend"] = result
            emit("list_friend", {"id_zalo": id_driver, "list_friend":result}, room=room)
            dict_driver[id_driver].get("https://chat.zalo.me/")
            dict_status_zalo[id_driver] = ""

@socketio.on('get_list_group')
def handle_get_list_group(data):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        if(dict_status_zalo[id_driver] != ''):
            print("bận rồi !!!", dict_status_zalo[id_driver])
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            dict_status_zalo[id_driver] = "get_list_group"        
            list_group = get_list_group_by_bs4(id_driver)
            emit("list_friend", {"id_zalo": id_driver, "list_group":list_group}, room=room)
            dict_driver[id_driver].get("https://chat.zalo.me/")
            dict_status_zalo[id_driver] = ""

@socketio.on('auto_send_mess')
def handle_auto_send_mess(data):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    list_zalo_send = data["list_zalo_send"]
    text_auto_send = data['text']

    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        folder_id_zalo = dict_folder_zalo[id_driver]
        if(dict_status_zalo[id_driver] != ''):
            print("bận rồi !!!", dict_status_zalo[id_driver])
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            dict_status_zalo[id_driver] = "auto_send_mess"
            try:
                first_zalo = list_zalo_send[0]
                del list_zalo_send[0]
                name_tmp, ava_tmp = first_zalo['name'], first_zalo['ava']
                click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[1]")
                click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[2]")
                click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[2]/div[3]/div/div[1]")
                input_name = get_element(dict_driver[id_driver], "xpath", '//*[@id="container"]/div[3]/div[2]/div/div[1]/div/div[1]/div/div/div[2]/div/div/span/input')
                input_name.click()
                input_name.send_keys(filter_bmp(name_tmp))
                input_name.send_keys(Keys.ENTER)
                eventlet.sleep(0.5)
                check_see = True
                name_tmp_check = unicodedata.normalize('NFKD', name_tmp).encode('utf-8', 'ignore').decode('utf-8')
                while check_see:
                    eventlet.sleep(0)
                    elements = dict_driver[id_driver].find_elements("xpath", '//div[contains(@class, "contact-item-v2-wrapper has--border") or contains(@class, "contact-item-v2-wrapper") or contains(@class, "contact-item-v2-wrapper last")]')
                    for contact_div in elements:
                        try:
                            img_src = ''
                            span_text = ''
                            try:
                                img_element = contact_div.find_element(By.CSS_SELECTOR, 'img.a-child')
                                img_src = img_element.get_attribute('src')
                            except:
                                pass
                            try:
                                span_element = contact_div.find_element(By.CSS_SELECTOR, 'span.name')
                                span_text = span_element.text
                            except:
                                pass
                            if img_src == ava_tmp:
                                if name_tmp_check == unicodedata.normalize('NFKD', span_text).encode('utf-8', 'ignore').decode('utf-8'):
                                    check_see = False
                                    if(span_text != "Zalo"):
                                        contact_div.click()
                                        break
                        except:
                            traceback.print_exc()
                            continue
                    if len(elements) == 0:
                        check_see = False
                    if check_see:
                        try:
                            element = dict_driver[id_driver].find_element("xpath", '//div[contains(@class, "contact-item-v2-wrapper last")]')
                            if element:
                                check_see = False
                        except:
                            print("Vẫn chưa tới cuối")
                            actions = ActionChains(dict_driver[id_driver])
                            actions.move_to_element(contact_div[-1]).perform()
                            eventlet.sleep(0.1)

                input_element = dict_driver[id_driver].find_element("xpath", '//*[@id="input_line_0"]')
                input_element.click()
                input_element.send_keys(text_auto_send)
                try:
                    input_element.send_keys(Keys.ENTER)
                except:
                    click_element(dict_driver[id_driver], "xpath", '//*[@id="chatInputv2"]/div/div/div[2]/div[5]/div')
                eventlet.sleep(1)
                div_message = get_element(dict_driver[id_driver], 'xpath', '//*[@id="messageViewScroll"]')
                soup = BeautifulSoup(div_message.get_attribute('outerHTML'), "html.parser")
                id_message = None
                div_elements = soup.find_all('div', attrs={'data-node-type': 'bubble-message'})
                for div_element in div_elements[::-1]:
                    span_element = div_element.find('span', text=text_auto_send)
                    if span_element:
                        id_message = div_element.get('id')
                        break
                if id_message:
                    forward_list_zalo(id_driver, id_message, list_zalo_send)
            except:
                traceback.print_exc()
            dict_status_zalo[id_driver] = ""

@socketio.on('auto_send_file')
def handle_auto_send_file(data):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    list_zalo_send = data["list_zalo_send"]
    result_api = data["result"]
    num_phone_server_api = data["num_phone_server"]
    id_message_api = data["id_mess_success"]

    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        if(dict_status_zalo[id_driver] != ''):
            print("bận rồi !!!", dict_status_zalo[id_driver])
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            dict_status_zalo[id_driver] = "auto_send_image"
            try:
                if (result_api == 'success'):
                    click_element(dict_driver[id_driver], 'xpath', '//*[@id="main-tab"]/div[1]/div[2]/div[1]')
                    click_element(dict_driver[id_driver], 'xpath', '//*[@id="contact-search-input"]')
                    input_ele = get_element(dict_driver[id_driver], 'xpath', '//*[@id="contact-search-input"]')
                    input_ele.send_keys(num_phone_server_api) 
                    eventlet.sleep(0.5)
                    input_ele.send_keys(Keys.ENTER)
                    eventlet.sleep(0.5)
                    forward_list_zalo(id_driver, id_message_api, list_zalo_send)
            except:
                traceback.print_exc()
            dict_status_zalo[id_driver] = ""

@socketio.on('get_list_invite_friend')
def handle_get_list_invite_friend(data):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        if(dict_status_zalo[id_driver] != ''):
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            dict_status_zalo[id_driver] = "get_list_invite_friend"
            click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[2]")
            click_element(dict_driver[id_driver], "xpath", "//*[@id='ContactTabV2']/div/div[3]")
            eventlet.sleep(1)
            card_receiveds = dict_driver[id_driver].find_elements(By.XPATH, "//div[contains(@class, 'card-wrapper received--friend')]")
            list_invite_friend = []
            for card_received in card_receiveds:
                info_dict = {}
                image_element = None
                try:
                    image_element = card_received.find_element(By.TAG_NAME, "img")
                except NoSuchElementException:
                    pass
                if image_element:
                # Nếu tồn tại, lấy URL của hình ảnh từ thuộc tính src
                    image_url = image_element.get_attribute("src")
                    print(image_url)
                else:
                    image_url = ""
                name = card_received.find_element(By.XPATH, ".//span[@class='name truncate']")
                text_name = name.text
                
                message = card_received.find_element(By.XPATH, ".//div[contains(@class, 'card-message')]")
                text_message = message.text
                
                info_dict["name"] = text_name
                info_dict["avatar"] = image_url
                info_dict["message"] = text_message
                list_invite_friend.append(info_dict)
            
            emit("list_invite_friend", {"id_zalo": id_driver, "list_invite_friend":list_invite_friend}, room=room)
            click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[1]")
            dict_status_zalo[id_driver] = ''

@socketio.on('accept_or_Refuse')
def handle_accept_or_refuse(data, list_invite):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    total = len(list_invite)
    check_total = 0 
    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        if(dict_status_zalo[id_driver] != ''):
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            dict_status_zalo[id_driver] = "accept_or_Refuse"
            click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[2]")
            click_element(dict_driver[id_driver], "xpath", "//*[@id='ContactTabV2']/div/div[3]")
            eventlet.sleep(3)
            card_receiveds = get_elements(dict_driver[id_driver], 'xpath', "//div[contains(@class, 'card-wrapper received--friend')]")
            print(len(card_receiveds))
            for card_received in card_receiveds:
                print('check tung card moi')
                image_element = None
                try:
                    image_element = card_received.find_element(By.TAG_NAME, "img")
                except NoSuchElementException:
                    pass
                if image_element:
                # Nếu tồn tại, lấy URL của hình ảnh từ thuộc tính src
                    image_url = image_element.get_attribute("src")
                else:
                    image_url = ""
                name = card_received.find_element(By.XPATH, ".//span[@class='name truncate']")
                text_name = name.text
                for dict_info_invite in list_invite:
                    if (dict_info_invite["name"] == text_name and dict_info_invite["avatar"] == image_url ):
                        print('tim thay ten')
                        if(dict_info_invite["accept_or"] == "accept"):
                            print("accept")
                            click_element(card_received,"xpath",".//div[contains(@class, 'z--btn--v2 btn-secondary large  --rounded')]")
                            click_element(dict_driver[id_driver],"xpath",".//div[contains(@class, 'z--btn--v2 btn-primary large wi --rounded wi')]")
                        else:
                            click_element(card_received,"xpath",".//div[contains(@class, 'z--btn--v2 btn-neutral large  --rounded')]")
                            click_element(dict_driver[id_driver],"xpath",".//div[contains(@class, 'z--btn--v2 btn-secondary large zl-modal__footer__button --rounded zl-modal__footer__button')]")
                        check_total += 1 
                        break
                if(check_total== total):
                    break
            click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[1]")
            dict_status_zalo[id_driver] = ''

@socketio.on('add_friend_all_members_group')
def handle_add_friend_all_members_group(data, list_group_to_add):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    total = len(list_group_to_add)
    check_total = 0
    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        if(dict_status_zalo[id_driver] != ''):
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            dict_status_zalo[id_driver] = "add_friend_all_members_group" 
            try:
                click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[1]")
                # time.sleep(1)
                click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[2]")
                # time.sleep(1)
                click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[2]/div[3]/div/div[2]")
                # time.sleep(1)
                list_group_card = dict_driver[id_driver].find_elements(By.XPATH, "//div[contains(@class, 'contact-item-v2-wrapper has--border')]")
                for group_card in list_group_card:
                    name_group = group_card.find_element(By.XPATH, ".//div[@class='name-wrapper']")
                    text_name_group = name_group.text 
                    # print(text_name_group)
                    quantity_members = group_card.find_element(By.XPATH, ".//a[@class='description left members']")
                    text_quantity_members = quantity_members.text 
                    # print(text_quantity_members)
                    for group in list_group_to_add: 
                        if (group["name"] == text_name_group and group["members"] == text_quantity_members ):
                            click_element(group_card, "xpath", ".//div[@class='friend-info']")
                            click_element(dict_driver[id_driver], "xpath", ".//div[@class='subtitle__groupmember__content flx flx-al-c clickable']")
                            eventlet.sleep(0.5)
                            members_card =  dict_driver[id_driver].find_elements(By.XPATH, ".//div[contains(@class, 'chat-box-member__info v2')]")
                            for member_card in members_card: 
                                add_frien_element = None
                                try:
                                    add_frien_element = member_card.find_element(By.XPATH, ".//div[@class='z--btn--v2 btn-secondary medium  --rounded']")
                                except NoSuchElementException:
                                    pass
                                if add_frien_element:
                                    click_element(member_card, "xpath", ".//div[@class='z--btn--v2 btn-secondary medium  --rounded']")
                                    click_element(dict_driver[id_driver], "xpath", ".//div[@class='z--btn--v2 btn-primary large  --rounded']")
                            check_total += 1
                            break 
                    if(check_total== total):
                        break
            except:
                print("null")
            dict_status_zalo[id_driver] = ''


@socketio.on('get_list_chat')
def handle_get_list_chat(data):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        if(dict_status_zalo[id_driver] != ''):
            print("bận rồi !!!", dict_status_zalo[id_driver])
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            dict_status_zalo[id_driver] = "get_list_chat"  
            click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[1]")
            div_list_chat = dict_driver[id_driver].find_element('xpath','//*[@id="conversationList"]/div')
            list_chat_result = []
            try:
                html_content = div_list_chat.get_attribute('outerHTML')
                soup = BeautifulSoup(html_content, 'html.parser')
                msg_items = soup.find_all('div', class_=lambda x: x and x.startswith('msg-item'))
                for msg_item in msg_items:
                    try:
                        if 'pinned' in msg_item.get('class'):
                            check_pined = True
                        else:
                            check_pined = False
                        ava_img = msg_item.find("img", class_='a-child')
                        if ava_img:
                            ava = ava_img.get('src')
                        else:
                            ava = ''
                        name = msg_item.find(class_="conv-item-title__name truncate grid-item").text.replace("\xa0", " ")
                        tag_label = msg_item.find('div', class_='conv__label')
                        if tag_label:
                            tag_label = tag_label.get('style')
                            tag_label = dict_tag_label[tag_label]
                        else:
                            tag_label = -1
                        last_mess = msg_item.find('div', class_=lambda x: x and x.startswith("conv-message truncate")).text.replace("\n", " ")
                        time_mess = msg_item.find('div', class_="conv-item-title__more rel grid-item")
                        if time_mess:
                            time_mess = time_mess.text
                        else:
                            time_mess = ''
                        num_unread = msg_item.find('div', class_='conv-action__unread-v2 flx flx-al-c')
                        if num_unread:
                            num_unread = num_unread.find('i').get('class')[6:-20]
                            check_unread = True
                        else:
                            num_unread = '0'
                            check_unread = False
                        tmp = {"name":name,"ava":ava, "check_pined":check_pined, "unread":check_unread, "last_mess":last_mess, "time_mess":time_mess, "num_unread": num_unread, 'tag_label': tag_label}
                        list_chat_result.append(tmp)
                    except:
                        traceback.print_exc()
            except:
                traceback.print_exc()
            dict_zalo_online[room][id_driver]["list_chat"] = list_chat_result
            emit("list_chat", {"id_zalo": id_driver, "list_chat":list_chat_result}, room=room)
            dict_status_zalo[id_driver] = ''

@socketio.on('update_list_chat')
def handle_get_list_chat(data):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        if(dict_status_zalo[id_driver] != '' or dict_status_update_list_chat[id_driver] == 'update_list_chat'):
            print("bận rồi !!!", dict_status_zalo[id_driver])
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            dict_status_update_list_chat[id_driver] = 'update_list_chat'
            current_status = []
            last_status = []
            while True:
                if(id_driver not in dict_driver):
                    break
                if(dict_status_zalo[id_driver].startswith('auto_')):
                    eventlet.sleep(2)
                    continue
                try:
                    div_list_chat = dict_driver[id_driver].find_element('xpath','//*[@id="conversationList"]/div')
                    if div_list_chat is None or div_list_chat == '':
                        eventlet.sleep(1)
                        continue     
                    current_status = []
                    list_chat_result = []
                    try:
                        html_content = div_list_chat.get_attribute('outerHTML')
                        soup = BeautifulSoup(html_content, 'html.parser')
                        msg_items = soup.find_all('div', class_=lambda x: x and x.startswith('msg-item'))
                        for msg_item in msg_items:
                            try:
                                if 'pinned' in msg_item.get('class'):
                                    check_pined = True
                                else:
                                    check_pined = False
                                ava_img = msg_item.find("img", class_='a-child')
                                if ava_img:
                                    ava = ava_img.get('src')
                                else:
                                    ava = ''
                                name = msg_item.find(class_="conv-item-title__name truncate grid-item").text.replace("\xa0", " ")
                                tag_label = msg_item.find('div', class_='conv__label')
                                if tag_label:
                                    tag_label = tag_label.get('style')
                                    tag_label = dict_tag_label[tag_label]
                                else:
                                    tag_label = -1
                                last_mess = msg_item.find('div', class_=lambda x: x and x.startswith("conv-message truncate")).text.replace("\n", " ")
                                time_mess = msg_item.find('div', class_="conv-item-title__more rel grid-item")
                                if time_mess:
                                    time_mess = time_mess.text
                                else:
                                    time_mess = ''
                                num_unread = msg_item.find('div', class_='conv-action__unread-v2 flx flx-al-c')
                                if num_unread:
                                    num_unread = num_unread.find('i').get('class')[6:-20]
                                    check_unread = True
                                else:
                                    num_unread = '0'
                                    check_unread = False
                                tmp = {"name":name,"ava":ava, "check_pined":check_pined, "unread":check_unread, "last_mess":last_mess, "time_mess":time_mess, "num_unread": num_unread, 'tag_label': tag_label}
                                list_chat_result.append(tmp)
                                current_status.append(name)
                                current_status.append(ava)
                                current_status.append(last_mess)
                                current_status.append(num_unread)
                            except:
                                pass
                                # traceback.print_exc()
                    except:
                        pass
                        # traceback.print_exc()
                    if(len(list_chat_result) == 0):
                        eventlet.sleep(1)
                        continue
                    if last_status != current_status:
                        list_last_num = []
                        list_last_status_check = []
                        for index_mess in range(int(len(last_status)/4)):
                            list_last_num.append(last_status[index_mess*4+3])
                            list_last_status_check.append(last_status[index_mess*4:index_mess*4+3])
                        for index_mess in range(int(len(current_status)/4)):
                            try:
                                index_check = list_last_status_check.index(current_status[index_mess*4:index_mess*4+3])
                                if list_last_num[index_check] !=0  and current_status[index_mess*4+3] == 0:
                                    continue
                            except:
                                index_check = -1
                                pass
                            if index_check < 0:
                                if not current_status[index_mess*4+2].startswith("Bạn:"):
                                    emit("new_message", {"id_zalo": id_driver, "list_new_message":[{'name': current_status[index_mess*4], 'ava': current_status[index_mess*4+1], 'last_mess': current_status[index_mess*4+2], 'num_unread': current_status[index_mess*4+3]}]}, room=room)
                        last_status = current_status.copy()
                        dict_zalo_online[room][id_driver]["list_chat"] = list_chat_result
                        emit("list_chat", {"id_zalo": id_driver, "list_chat":list_chat_result}, room=room)
                except:
                    # traceback.print_exc()
                    pass
                eventlet.sleep(1)
            dict_status_update_list_chat[id_driver] = ''

@socketio.on('chat_pvp')
def handle_chat_pvp(data):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    name_chat = data['name']
    ava_chat = data['ava']
    id_pvp = data['id_pvp']
    if (name_chat == 'Tin nhắn từ người lạ' and ava_chat.startswith('assets/stranger_avatar')):
        return
    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        if(dict_status_zalo[id_driver] != ''):
            print("bận rồi !!!", dict_status_zalo[id_driver])
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            dict_status_zalo[id_driver] = "chat_pvp"        
            if(id_pvp != ""):
                list_friend = dict_zalo_online[room][id_driver]["list_friend"]
                set_data = set()
                for tmp in list_friend:
                    if tmp["id"] == id_pvp:
                        set_data.add((tmp["name"], tmp["ava"]))
                try:
                    name_tmp, ava_tmp = set_data.pop()
                    click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[1]")
                    click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[2]")
                    click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[2]/div[3]/div/div[1]")
                    input_name = get_element(dict_driver[id_driver], "xpath", '//*[@id="container"]/div[3]/div[2]/div/div[1]/div/div[1]/div/div/div[2]/div/div/span/input')
                    input_name.click()
                    input_name.send_keys(filter_bmp(name_tmp))
                    input_name.send_keys(Keys.ENTER)
                    eventlet.sleep(0.5)
                    check_see = True
                    name_tmp_check = unicodedata.normalize('NFKD', name_tmp).encode('utf-8', 'ignore').decode('utf-8')
                    while check_see:
                        eventlet.sleep(0)
                        elements = dict_driver[id_driver].find_elements("xpath", '//div[contains(@class, "contact-item-v2-wrapper has--border") or contains(@class, "contact-item-v2-wrapper") or contains(@class, "contact-item-v2-wrapper last")]')
                        for contact_div in elements:
                            try:
                                img_src = ''
                                span_text = ''
                                try:
                                    img_element = contact_div.find_element(By.CSS_SELECTOR, 'img.a-child')
                                    img_src = img_element.get_attribute('src')
                                except:
                                    pass
                                try:
                                    span_element = contact_div.find_element(By.CSS_SELECTOR, 'span.name')
                                    span_text = span_element.text
                                except:
                                    pass
                                if img_src == ava_tmp:
                                    if name_tmp_check == unicodedata.normalize('NFKD', span_text).encode('utf-8', 'ignore').decode('utf-8'):
                                        check_see = False
                                        if(span_text != "Zalo"):
                                            contact_div.click()
                                            break
                            except:
                                continue
                        if len(contact_div) == 0:
                            check_see = False
                        if check_see:
                            try:
                                element = dict_driver[id_driver].find_element("xpath", '//div[contains(@class, "contact-item-v2-wrapper last")]')
                                if element:
                                    check_see = False
                            except:
                                print("Vẫn chưa tới cuối")
                                actions = ActionChains(dict_driver[id_driver])
                                actions.move_to_element(contact_div[-1]).perform()
                                eventlet.sleep(0.1)
                except:
                    traceback.print_exc()
            else:                    
                click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[1]")
                name_tmp_check = unicodedata.normalize('NFKD', name_chat).encode('utf-8', 'ignore').decode('utf-8')
                print("name_chat: ", name_chat)
                eventlet.sleep(0.2)
                index = 1
                times_fail = 2
                while times_fail > 0:
                    eventlet.sleep(0)
                    xpath_name = f'//*[@id="conversationList"]/div/div[{index}]/div/div-16/div'
                    xpath_nameb = f'//*[@id="conversationList"]/div/div[{index}]/div/div-b16/div'
                    xpath_img = f'//*[@id="conversationList"]/div/div[{index}]/div/div[1]/div/div/img'
                    try:
                        name_element = dict_driver[id_driver].find_element('xpath',xpath_name)
                        name = name_element.text
                    except:
                        try:
                            name_element = dict_driver[id_driver].find_element('xpath',xpath_nameb)
                            name = name_element.text
                        except:
                            name = ''
                    if name == '':
                        times_fail -= 1
                        continue
                    else:
                        try:
                            ava = dict_driver[id_driver].find_element('xpath',xpath_img).get_attribute("src")
                        except:
                            ava = ''
                        if ava == ava_chat and unicodedata.normalize('NFKD', name).encode('utf-8', 'ignore').decode('utf-8') == name_tmp_check:
                            print("tìm thấy")
                            times_fail = 0
                            name_element.click()
                        else:
                            index += 1
                            times_fail = 2
            
            print("out_chat_pvp")
            dict_status_zalo[id_driver] = ''
            eventlet.sleep(0.5)
            emit("finish_chat_pvp", {}, room=room)

@socketio.on('update_chat_pvp')
def handle_update_chat_pvp(data):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        if(dict_status_zalo[id_driver] != '' or dict_status_update_data_chat[id_driver] == 'update_chat_pvp'):
            print("bận rồi !!!", dict_status_zalo[id_driver])
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            dict_status_update_data_chat[id_driver] = 'update_chat_pvp'
            last_id = []
            last_name = ''
            last_ava = ''
            while True:
                if(id_driver not in dict_driver):
                    break
                if(dict_status_zalo[id_driver].startswith('auto_') or dict_status_zalo[id_driver] == "forward_message"):
                    eventlet.sleep(2)
                    continue
                try:
                    try:
                        name_chat = dict_driver[id_driver].find_element('xpath', '//*[@id="header"]/div[1]/div[2]/div[1]/div/div-b18').text
                        current_name = name_chat
                    except:
                        name_chat = ''
                    if name_chat != '':
                        try:
                            ava_chat = dict_driver[id_driver].find_element('xpath', '//*[@id="ava_chat_box_view"]/div[1]/div/img').get_attribute('src')
                        except:
                            ava_chat = ''
                        current_ava = ava_chat
                        if last_ava != current_ava or last_name != current_name:
                            last_name = current_name
                            last_ava = current_ava
                            last_id = []
                        html_text = dict_driver[id_driver].find_element("xpath",'//*[@id="messageViewScroll"]').get_attribute('outerHTML')
                        soup = BeautifulSoup(html_text, 'html.parser')
                        current_id = get_id_chat_all_block_date(soup)
                        if current_id != last_id:
                            new_id = []
                            for id_data_chat in current_id[::-1]:
                                if id_data_chat not in last_id:
                                    new_id.append(id_data_chat)
                                else:
                                    break
                            print(new_id)
                            data_all_block_date = get_data_chat_all_block_date(soup, id_driver, new_id)
                            last_id = current_id.copy()
                            emit("update_data_chat", {"id_zalo": id_driver, "name_chat":name_chat, "ava_chat":ava_chat, "data_chat":data_all_block_date}, room=room)
                    else:
                        eventlet.sleep(1)
                except:
                    traceback.print_exc()
                    break
                eventlet.sleep(1)
            dict_status_update_data_chat[id_driver] = ''

@socketio.on('send_chat_pvp')
def handle_send_chat_pvp(data,dict_text_mem):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    name_chat = data['name']
    ava_chat = data['ava']
    print('list tag', dict_text_mem)
    # text_send = data['text']
    list_a = dict_text_mem
    text_send = data["text"]
    if(text_send.startswith("@setpst@")):
        if(id_driver in dict_driver):
            x,y = int(text_send.split("@")[-2]), int(text_send.split("@")[-1])
            dict_driver[id_driver].set_window_size(1920, 1080)
            dict_driver[id_driver].set_window_position(x, y)
    else:
        if(id_driver in dict_driver and id_driver in dict_status_zalo):
            if(dict_status_zalo[id_driver] != ''):
                print("bận rồi !!!", dict_status_zalo[id_driver])
                emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
            else:
                dict_status_zalo[id_driver] = "send_chat_pvp"
                try:
                    ava_check = dict_driver[id_driver].find_element('xpath','//*[@id="ava_chat_box_view"]/div[1]/div/img').get_attribute('src')
                except:
                    ava_check = ''
                try:
                    name_check = dict_driver[id_driver].find_element('xpath','//*[@id="header"]/div[1]/div[2]/div[1]/div[1]/div-b18').text
                except:
                    name_check = ''
                if(ava_chat == ava_check and name_chat == name_check):
                    if(dict_text_mem == None or len(dict_text_mem) == 0):
                        input_element = dict_driver[id_driver].find_element("xpath", '//*[@id="input_line_0"]')
                        input_element.click()
                        input_element.send_keys(text_send)
                        try:
                            input_element.send_keys(Keys.ENTER)
                        except:
                            click_element(dict_driver[id_driver], "xpath", '//*[@id="chatInputv2"]/div/div/div[2]/div[5]/div')
                    else:
                        try:
                            check_mem = 1
                            for member_a in list_a:
                                if(check_mem != len(list_a)):
                                    if(member_a["name"] == "All"):
                                        print("log cho Nga vui")
                                        st_a = "@" + str(member_a["name"])
                                        splitted_text = text_send.split(st_a)
                                        txt_0 = splitted_text[0] 
                                        text_send = splitted_text[1]
                                        message_input = dict_driver[id_driver].find_element(By.XPATH,".//div[@id='richInput']")
                                        actions = ActionChains(dict_driver[id_driver])
                                        actions.move_to_element(message_input).perform()
                                        message_input.send_keys(txt_0)
                                        message_input.send_keys(st_a)
                                        eventlet.sleep(0.2)
                                        message_input.send_keys(Keys.ENTER)
                                        check_mem += 1
                                    else:    
                                        st_a = "@" + str(member_a["name"])
                                        splitted_text = text_send.split(st_a)
                                        txt_0 = splitted_text[0] 
                                        text_send = splitted_text[1]
                                        message_input = dict_driver[id_driver].find_element(By.XPATH,".//div[@id='richInput']")
                                        actions = ActionChains(dict_driver[id_driver])
                                        actions.move_to_element(message_input).perform()
                                        message_input.send_keys(txt_0)
                                        message_input.send_keys(st_a)
                                        eventlet.sleep(0.2)                                        
                                        a_mentions = dict_driver[id_driver].find_elements(By.XPATH,"//div[contains(@class, 'clickable flx flx-al-c mention-popover__item')]")
                                        for mention in a_mentions:
                                            title = mention.get_attribute('title') 
                                            avatar_element = None
                                            try:
                                                avatar_element = mention.find_element(By.XPATH, ".//div[@class='rel zavatar-container']/div[@class='zavatar zavatar-s zavatar-single flx flx-al-c flx-center rel clickable disableDrag']/img")
                                            except NoSuchElementException:
                                                pass
                                            if avatar_element:
                                                avatar_url = avatar_element.get_attribute("src")
                                            else:
                                                avatar_url = ""  
                                            if (title == member_a['name'] and avatar_url == member_a['avatar']):
                                                click_element(dict_driver[id_driver], "xpath", ".//div[contains(@class, 'clickable flx flx-al-c mention-popover__item')]")
                                                eventlet.sleep(0.2) 
                                                check_mem += 1 
                                                break 
                                else:
                                    if(member_a["name"] == "All"):
                                        print("Nga vui r nhé!")
                                        st_a = "@" + str(member_a["name"])
                                        splitted_text = text_send.split(st_a)
                                        txt_0 = splitted_text[0] 
                                        text_send = splitted_text[1]
                                        message_input = dict_driver[id_driver].find_element(By.XPATH,".//div[@id='richInput']")
                                        actions = ActionChains(dict_driver[id_driver])
                                        actions.move_to_element(message_input).perform()
                                        message_input.send_keys(txt_0)
                                        message_input.send_keys(st_a)
                                        eventlet.sleep(0.2)
                                        message_input.send_keys(Keys.ENTER)
                                        message_input = dict_driver[id_driver].find_element(By.XPATH,".//div[@id='richInput']")
                                        actions = ActionChains(dict_driver[id_driver])
                                        actions.move_to_element(message_input).perform()
                                        message_input.send_keys(text_send)
                                        message_input.send_keys(Keys.ENTER)
                                        check_mem += 1
                                    else:
                                        st_a = "@" + str(member_a["name"])
                                        splitted_text = text_send.split(st_a)
                                        txt_0 = splitted_text[0] 
                                        text_send = splitted_text[1]
                                        message_input = dict_driver[id_driver].find_element(By.XPATH,".//div[@id='richInput']")
                                        actions = ActionChains(dict_driver[id_driver])
                                        actions.move_to_element(message_input).perform()
                                        eventlet.sleep(0.2)
                                        message_input.send_keys(txt_0)
                                        message_input.send_keys(st_a)
                                        eventlet.sleep(0.1)                                        
                                        a_mentions = dict_driver[id_driver].find_elements(By.XPATH,"//div[contains(@class, 'clickable flx flx-al-c mention-popover__item')]")                                        
                                        for mention in  a_mentions:
                                            title = mention.get_attribute('title') 
                                            avatar_element = None
                                            try:
                                                avatar_element = mention.find_element(By.XPATH, ".//div[@class='rel zavatar-container']/div[@class='zavatar zavatar-s zavatar-single flx flx-al-c flx-center rel clickable disableDrag']/img")
                                            except NoSuchElementException:
                                                pass
                                            if avatar_element:
                                                avatar_url = avatar_element.get_attribute("src")
                                            else:
                                                avatar_url = ""  
                                            if (title == member_a['name'] and avatar_url == member_a['avatar']):
                                                try:
                                                    click_element(dict_driver[id_driver], "xpath", ".//div[contains(@class, 'clickable flx flx-al-c mention-popover__item')]")
                                                    message_input = dict_driver[id_driver].find_element(By.XPATH,".//div[@id='richInput']")
                                                    actions = ActionChains(dict_driver[id_driver])
                                                    actions.move_to_element(message_input).perform()
                                                    message_input.send_keys(text_send)
                                                    message_input.send_keys(Keys.ENTER)
                                                    eventlet.sleep(0.2) 
                                                    check_mem += 1 
                                                except Exception as e:
                                                    print("Lỗi:" ,e)
                                                break
                        except:
                            pass
                        
                else:
                    emit('fail',{"error":"name or avatar conflict"}, room = room)
                dict_status_zalo[id_driver] = ''

@socketio.on('get_list_a_cong')
def handle_get_list_a_cong(data):
    room = data['id_chat']
    id_driver = data['id_zalo']
    name_chat = data['name']
    ava_chat = data['ava']
    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        if(dict_status_zalo[id_driver] != ''):
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            dict_status_zalo[id_driver] = "get_list_a_cong"
            group_ = None
            try:
                if "group" in get_element(dict_driver[id_driver], 'xpath', "//*[@id='header']/div[1]", times=3, sleep_time=0.2).get_attribute("class"):
                    community__ = None
                    try:
                        community__ = dict_driver[id_driver].find_element(By.XPATH, ".//div[@class='community__chat-box-indicator']")
                    except NoSuchElementException:
                        pass
                    if community__:
                        # print("ok_1")
                        click_element(dict_driver[id_driver], "xpath", ".//span[@class='flx flx-al-c clickable community__chat-box-indicator__mem']")
                        time.sleep(1)
                    else:
                        # print("ok_2")
                        click_element(dict_driver[id_driver], "xpath", ".//div[@class='subtitle__groupmember__content flx flx-al-c clickable']")
                        time.sleep(1)

                    
                    # dict_driver[id_driver].execute_script("document.body.style.zoom='25%'")
                    # eventlet.sleep(5)
                    
                    members_card_ =  dict_driver[id_driver].find_element(By.XPATH, "//*[@id='member-group']")
                    html_text = members_card_.get_attribute('outerHTML')
                    soup = BeautifulSoup(html_text, 'html.parser')
                    members_card = soup.find_all('div', class_='chat-box-member__info v2')
                    # dict_driver[id_driver].execute_script("document.body.style.zoom='100%'")
                    list_a = []
                    for member_card in members_card:
                        mem_ = {}
                        # Extract title attribute
                        title = member_card['title']
                        mem_['name'] = title
                        
                        
                        # Find the avatar image
                        avatar_element = member_card.find('div', class_='zavatar-container').find('img')
                        avatar_url = avatar_element['src'] if avatar_element else ""
                        mem_['avatar'] = avatar_url
                        
                        list_a.append(mem_)
                    emit("list_a_cong", {"id_zalo": id_driver, "name": name_chat, "ava": ava_chat, "list_chat":list_a}, room=room)
            except:
                pass
            dict_status_zalo[id_driver] = ''

# @socketio.on('send_image_chat_pvp')
# def send_image_chat_pvp(data):
#     room = data["id_chat"]
#     id_driver = data['id_zalo']
#     name_chat = data['name']
#     ava_chat = data['ava']
#     file_path = data["file_path"]
#     print(file_path)

#     if(id_driver in dict_driver and id_driver in dict_status_zalo):
#         if(dict_status_zalo[id_driver] != ''):
#             print("bận rồi !!!", dict_status_zalo[id_driver])
#             emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
#         else:
#             dict_status_zalo[id_driver] = "send_image_chat_pvp"
#             try:
#                 ava_check = dict_driver[id_driver].find_element('xpath','//*[@id="ava_chat_box_view"]/div[1]/div/img').get_attribute('src')
#             except:
#                 ava_check = ''
#             try:
#                 name_check = dict_driver[id_driver].find_element('xpath','//*[@id="header"]/div[1]/div[2]/div[1]/div[1]/div-b18').text
#             except:
#                 name_check = ''
#             if(ava_chat == ava_check and name_chat == name_check):
#                 try:
#                     with open(file_path, 'rb') as file:
#                         file_content = file.read()
#                     base64_content = base64.b64encode(file_content)
#                     base64_string = base64_content.decode('utf-8')

#                     url = 'http://103.138.113.76:2001/send_file'

#                     data = {
#                         "num_phone":dict_zalo_online[room][id_driver]["num_phone_zalo"],
#                         "base64_file":base64_string,
#                         "name_file":os.path.basename(file_path)
#                     }

#                     response = requests.post(url, json=data)
#                     if response.status_code == 200:
#                         if (response.json()['result'] == 'success'):
#                             num_phone_server = response.json()['num_phone_server']
#                             id_message = response.json()['id_mess_success']
#                             click_element(dict_driver[id_driver], 'xpath', '//*[@id="main-tab"]/div[1]/div[2]/div[1]')
#                             click_element(dict_driver[id_driver], 'xpath', '//*[@id="contact-search-input"]')
#                             input_ele = get_element(dict_driver[id_driver], 'xpath', '//*[@id="contact-search-input"]')
#                             input_ele.send_keys(num_phone_server) 
#                             eventlet.sleep(0.5)
#                             input_ele.send_keys(Keys.ENTER)
#                             eventlet.sleep(0.5)
#                             element = get_element(dict_driver[id_driver], 'xpath', f'//div[@id="{id_message}" and @data-node-type="bubble-message"]', times=100, sleep_time=0.5)
#                             if element:
#                                 actions = ActionChains(dict_driver[id_driver])
#                                 actions.move_to_element(element).perform()
#                                 click_element(dict_driver[id_driver], 'xpath', '//*[@id="messageViewContainer"]/div[1]/div[1]/div[@data-translate-title="STR_FORWARD_MSG"]/i')
                                
#                                 tim_kiem = get_element(dict_driver[id_driver], 'xpath','//*[@id="group-creator"]/div[1]/span/input')
#                                 tim_kiem.send_keys(filter_bmp(name_chat))
#                                 eventlet.sleep(0.5)
#                                 last_div = None
#                                 check_see = True
#                                 try:
#                                     print("find share", name_chat, ava_chat)
#                                     name_check_see = unicodedata.normalize('NFKD', name_chat).encode('utf-8', 'ignore').decode('utf-8')
#                                     while check_see:
#                                         elements = dict_driver[id_driver].find_elements("xpath", "//div[@data-id='div_FWD_CTItem']")
#                                         for contact_div in elements:
#                                             try:
#                                                 soup = BeautifulSoup(contact_div.get_attribute('outerHTML'), "html.parser")
#                                                 div_element = soup.find("div", class_="create-group__item")
#                                                 try:
#                                                     img_src = div_element.find("img")["src"]
#                                                 except:
#                                                     img_src = ''
#                                                 try:
#                                                     name = div_element.find(class_="create-group__item__name").text
#                                                 except:
#                                                     name = ''
#                                                 if img_src == ava_chat:
#                                                     if unicodedata.normalize('NFKD', name).encode('utf-8', 'ignore').decode('utf-8') == name_check_see:
#                                                         print("đã thấy")
#                                                         contact_div.click()
#                                                         click_element(dict_driver[id_driver], 'xpath', '//div[@data-translate-inner="STR_FORWARD"]')
#                                                         check_see = False
#                                                         break
#                                             except:
#                                                 traceback.print_exc()
#                                                 continue
#                                         if len(elements) == 0:
#                                             check_see = False
#                                         if check_see:
#                                             if last_div == elements[-1]:
#                                                     check_see = False
#                                             else:
#                                                 last_div = elements[-1]
#                                                 print("Vẫn chưa tới cuối")
#                                                 actions = ActionChains(dict_driver[id_driver])
#                                                 actions.move_to_element(last_div).perform()
#                                                 eventlet.sleep(0.1)
#                                 except:
#                                     traceback.print_exc()
#                                 click_element(dict_driver[id_driver], 'xpath', '//div[@data-translate-inner="STR_CANCEL"]', times = 1)
#                                 try:
#                                     click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[1]")
#                                     name_tmp_check = unicodedata.normalize('NFKD', name_chat).encode('utf-8', 'ignore').decode('utf-8')
#                                     print("name_chat: ", name_chat)
#                                     eventlet.sleep(0.2)
#                                     index = 1
#                                     times_fail = 2
#                                     while times_fail > 0:
#                                         eventlet.sleep(0)
#                                         xpath_name = f'//*[@id="conversationList"]/div/div[{index}]/div/div-16/div'
#                                         xpath_nameb = f'//*[@id="conversationList"]/div/div[{index}]/div/div-b16/div'
#                                         xpath_img = f'//*[@id="conversationList"]/div/div[{index}]/div/div[1]/div/div/img'
#                                         try:
#                                             name_element = dict_driver[id_driver].find_element('xpath',xpath_name)
#                                             name = name_element.text
#                                         except:
#                                             try:
#                                                 name_element = dict_driver[id_driver].find_element('xpath',xpath_nameb)
#                                                 name = name_element.text
#                                             except:
#                                                 name = ''
#                                         if name == '':
#                                             times_fail -= 1
#                                             continue
#                                         else:
#                                             try:
#                                                 ava = dict_driver[id_driver].find_element('xpath',xpath_img).get_attribute("src")
#                                             except:
#                                                 ava = ''
#                                             if ava == ava_chat and unicodedata.normalize('NFKD', name).encode('utf-8', 'ignore').decode('utf-8') == name_tmp_check:
#                                                 print("tìm thấy")
#                                                 times_fail = 0
#                                                 name_element.click()
#                                             else:
#                                                 index += 1
#                                                 times_fail = 2
#                                 except:
#                                     traceback.print_exc()
#                             else:
#                                 emit('fail',{"error":"can't send file"}, room = room)
#                         else:
#                             emit('fail',{"error":"can't send file"}, room = room)
#                     else:
#                         emit('fail',{"error":"can't send file"}, room = room)
#                 except:
#                     traceback.print_exc()
#             else:
#                 emit('fail',{"error":"name or avatar conflict"}, room = room)
#             dict_status_zalo[id_driver] = ""

@socketio.on('send_file_chat_pvp')
def handle_send_file_chat_pvp(data):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    name_chat = data['name']
    ava_chat = data['ava']
    result_api = data["result"]
    num_phone_server_api = data["num_phone_server"]
    id_message_api = data["id_mess_success"]

    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        if(dict_status_zalo[id_driver] != ''):
            print("bận rồi !!!", dict_status_zalo[id_driver])
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            dict_status_zalo[id_driver] = "send_file_chat_pvp"
            try:
                ava_check = dict_driver[id_driver].find_element('xpath','//*[@id="ava_chat_box_view"]/div[1]/div/img').get_attribute('src')
            except:
                ava_check = ''
            try:
                name_check = dict_driver[id_driver].find_element('xpath','//*[@id="header"]/div[1]/div[2]/div[1]/div[1]/div-b18').text
            except:
                name_check = ''
            if(ava_chat == ava_check and name_chat == name_check):
                try:
                    if (result_api == 'success'):
                        click_element(dict_driver[id_driver], 'xpath', '//*[@id="main-tab"]/div[1]/div[2]/div[1]')
                        click_element(dict_driver[id_driver], 'xpath', '//*[@id="contact-search-input"]')
                        input_ele = get_element(dict_driver[id_driver], 'xpath', '//*[@id="contact-search-input"]')
                        input_ele.send_keys(num_phone_server_api) 
                        eventlet.sleep(0.5)
                        input_ele.send_keys(Keys.ENTER)
                        eventlet.sleep(0.5)
                        element = get_element(dict_driver[id_driver], 'xpath', f'//div[@id="{id_message_api}" and @data-node-type="bubble-message"]', times=100, sleep_time=0.5)
                        if element:
                            actions = ActionChains(dict_driver[id_driver])
                            actions.move_to_element(element).perform()
                            click_element(dict_driver[id_driver], 'xpath', '//*[@id="messageViewContainer"]/div[1]/div[1]/div[@data-translate-title="STR_FORWARD_MSG"]/i')
                            
                            tim_kiem = get_element(dict_driver[id_driver], 'xpath','//*[@id="group-creator"]/div[1]/span/input')
                            tim_kiem.send_keys(filter_bmp(name_chat))
                            eventlet.sleep(0.5)
                            last_div = None
                            check_see = True
                            try:
                                print("find share", name_chat, ava_chat)
                                name_check_see = unicodedata.normalize('NFKD', name_chat).encode('utf-8', 'ignore').decode('utf-8')
                                while check_see:
                                    elements = dict_driver[id_driver].find_elements("xpath", "//div[@data-id='div_FWD_CTItem']")
                                    for contact_div in elements:
                                        try:
                                            soup = BeautifulSoup(contact_div.get_attribute('outerHTML'), "html.parser")
                                            div_element = soup.find("div", class_="create-group__item")
                                            try:
                                                img_src = div_element.find("img")["src"]
                                            except:
                                                img_src = ''
                                            try:
                                                name = div_element.find(class_="create-group__item__name").text
                                            except:
                                                name = ''
                                            if img_src == ava_chat:
                                                if unicodedata.normalize('NFKD', name).encode('utf-8', 'ignore').decode('utf-8') == name_check_see:
                                                    print("đã thấy")
                                                    contact_div.click()
                                                    click_element(dict_driver[id_driver], 'xpath', '//div[@data-translate-inner="STR_FORWARD"]')
                                                    check_see = False
                                                    break
                                        except:
                                            traceback.print_exc()
                                            continue
                                    if len(elements) == 0:
                                        check_see = False
                                    if check_see:
                                        if last_div == elements[-1]:
                                                check_see = False
                                        else:
                                            last_div = elements[-1]
                                            print("Vẫn chưa tới cuối")
                                            actions = ActionChains(dict_driver[id_driver])
                                            actions.move_to_element(last_div).perform()
                                            eventlet.sleep(0.1)
                            except:
                                traceback.print_exc()
                            click_element(dict_driver[id_driver], 'xpath', '//div[@data-translate-inner="STR_CANCEL"]', times = 1)
                            try:
                                click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[1]")
                                name_tmp_check = unicodedata.normalize('NFKD', name_chat).encode('utf-8', 'ignore').decode('utf-8')
                                print("name_chat: ", name_chat)
                                eventlet.sleep(1)
                                index = 1
                                times_fail = 2
                                while times_fail > 0:
                                    eventlet.sleep(0)
                                    xpath_name = f'//*[@id="conversationList"]/div/div[{index}]/div/div-16/div'
                                    xpath_nameb = f'//*[@id="conversationList"]/div/div[{index}]/div/div-b16/div'
                                    xpath_img = f'//*[@id="conversationList"]/div/div[{index}]/div/div[1]/div/div/img'
                                    try:
                                        name_element = dict_driver[id_driver].find_element('xpath',xpath_name)
                                        name = name_element.text
                                    except:
                                        try:
                                            name_element = dict_driver[id_driver].find_element('xpath',xpath_nameb)
                                            name = name_element.text
                                        except:
                                            name = ''
                                    if name == '':
                                        times_fail -= 1
                                        continue
                                    else:
                                        try:
                                            ava = dict_driver[id_driver].find_element('xpath',xpath_img).get_attribute("src")
                                        except:
                                            ava = ''
                                        if ava == ava_chat and unicodedata.normalize('NFKD', name).encode('utf-8', 'ignore').decode('utf-8') == name_tmp_check:
                                            print("tìm thấy")
                                            times_fail = 0
                                            name_element.click()
                                        else:
                                            index += 1
                                            times_fail = 2
                            except:
                                traceback.print_exc()
                        else:
                            emit('fail',{"error":"can't send file"}, room = room)
                    else:
                        emit('fail',{"error":"can't send file"}, room = room)
                except:
                    traceback.print_exc()
            else:
                emit('fail',{"error":"name or avatar conflict"}, room = room)
            dict_status_zalo[id_driver] = ""

@socketio.on('add_list_friend')
def handle_add_list_friend(data):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    list_phone = data["list_phone"]
    text_add_friend = data['text']
    data_emit = {}
    data_emit["so ko hop le"] = []
    data_emit["da ket ban"] = []
    data_emit["ket ban thanh cong"]= []
    print ("data :" , data)
    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        if(dict_status_zalo[id_driver] != ''):
            print("bận rồi !!!", dict_status_zalo[id_driver])
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            dict_status_zalo[id_driver] = "add_list_friend"
            list_fail_add = []
            for num_phone in list_phone :
                click_element(dict_driver[id_driver], 'xpath', '//*[@id="contact-search"]/div[2]/i')
                
                input_element = get_element(dict_driver[id_driver], "xpath", '//*[@id="findFriend"]/div[1]/div/div/input', times=1)
                try:
                   input_element.send_keys(str(num_phone))
                except:
                    dict_driver[id_driver].get("https://chat.zalo.me/")
                click_element(dict_driver[id_driver], 'xpath', '//*[@id="zl-modal__dialog-body"]/div/div/div/div[2]/div[2]/div')
                try:
                    # add_button = dict_driver[id_driver].find_element("xpath", '//*[@id="zl-modal__dialog-body"]/div/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div')
                    # add_button.click()
                    click_element(dict_driver[id_driver],"xpath", '//*[@id="zl-modal__dialog-body"]/div/div/div/div/div[1]/div/div[2]/div[2]/div[1]/div', times=2)
                    # //*[@id="zl-modal__dialog-body"]/div/div/div/div/div[1]/div/div[2]/div[2]/div/div
                    text_area = get_element(dict_driver[id_driver], "xpath", '//*[@id="zl-modal__dialog-body"]/div/div/div/div[1]/div[1]/div/div[3]/div/div[1]/div/textarea', times=2)
                    if text_area is None:
                        if get_element(dict_driver[id_driver],"xpath", '//*[@id="zl-modal__dialog-body"]/div/div/div/div/div[1]/div/div[2]/div[2]/div/div', times=2) is None:
                            data_emit["so ko hop le"].append(num_phone)
                            # //*[@id="zl-modal-v2-1705049384961"]/div/div/div[1]/div/div[2]/i
                            click_element(dict_driver[id_driver],"xpath", '/html/body/div[2]/div/div/div[1]/div/div[2]/i', times=2)

                        else:
                            data_emit["da ket ban"].append(num_phone)
                            click_element(dict_driver[id_driver],"xpath", '/html/body/div[2]/div/div/div[1]/div/div[2]/i', times=2)
                        continue
                    text_area.send_keys(Keys.CONTROL + "a")  # Select all text
                    text_area.send_keys(Keys.DELETE)  # Delete the selected text
                    text_area.send_keys(text_add_friend)
                    click_element(dict_driver[id_driver], 'xpath', '//*[@id="zl-modal__dialog-body"]/div/div/div/div[2]/div[2]/div')
                    data_emit["ket ban thanh cong"].append(num_phone)
                    eventlet.sleep(3)
                    # eventlet.sleep(random.randint(100, 150)/10)
                except:
                    traceback.print_exc()
                    list_fail_add.append(num_phone)
                # eventlet.sleep(1)
            emit('list_fail_add', {'list_fail_add': list_fail_add , "list_data": data_emit } , room= room)
            dict_status_zalo[id_driver] = ""
            dict_driver[id_driver].get("https://chat.zalo.me/")

@socketio.on('set_nickname')
def handle_set_nickname(data):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    name_chat = data['name']
    ava_chat = data['ava']
    nickname = data['nickname']
    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        if(dict_status_zalo[id_driver] != ''):
            print("bận rồi !!!", dict_status_zalo[id_driver])
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            try:
                ava_check = dict_driver[id_driver].find_element('xpath','//*[@id="ava_chat_box_view"]/div[1]/div/img').get_attribute('src')
            except:
                ava_check = ''
            try:
                name_check = dict_driver[id_driver].find_element('xpath','//*[@id="header"]/div[1]/div[2]/div[1]/div[1]/div-b18').text
            except:
                name_check = ''
            if(ava_chat == ava_check and name_chat == name_check):
                dict_status_zalo[id_driver] = "set_nickname"
                click_element(dict_driver[id_driver], 'xpath', '//*[@id="header"]/div[1]/div[2]/div[1]/div[1]/div-b18')
                click_element(dict_driver[id_driver], 'xpath', '//*[@id="header"]/div[1]/div[2]/div[1]/div[2]/i')
                input_ele = get_element(dict_driver[id_driver], 'xpath', '//*[@id="zl-modal__dialog-body"]/div/div/div[3]/div/span/input')
                input_ele.send_keys(Keys.CONTROL + "a")
                input_ele.send_keys(Keys.DELETE)
                input_ele.send_keys(nickname)
                input_ele.send_keys(Keys.ENTER)

            dict_status_zalo[id_driver] = ''

@socketio.on('revoke_message')
def handle_revoke_message(data):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    name_chat = data['name']
    ava_chat = data['ava']
    id_message = data['id_message']
    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        if(dict_status_zalo[id_driver] != ''):
            print("bận rồi !!!", dict_status_zalo[id_driver])
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            dict_status_zalo[id_driver] = "revoke_message"
            try:
                ava_check = dict_driver[id_driver].find_element('xpath','//*[@id="ava_chat_box_view"]/div[1]/div/img').get_attribute('src')
            except:
                ava_check = ''
            try:
                name_check = dict_driver[id_driver].find_element('xpath','//*[@id="header"]/div[1]/div[2]/div[1]/div[1]/div-b18').text
            except:
                name_check = ''
            if(ava_chat == ava_check and name_chat == name_check):
                element = get_element(dict_driver[id_driver], 'xpath', f'//div[@id="{id_message}" and @data-node-type="bubble-message"]')
                actions = ActionChains(dict_driver[id_driver])
                actions.move_to_element(element).perform()
                click_element(dict_driver[id_driver], 'xpath', f'//div[@id="{id_message}" and @data-node-type="bubble-message"]')
                click_element(dict_driver[id_driver], 'xpath', '//*[@id="messageViewContainer"]/div[1]/div[1]/div[last()]/i')
                click_element(dict_driver[id_driver], 'xpath', '/html/body/div[2]/div[2]/div/div/div-14[position() = last() - 1]/i')
            dict_status_zalo[id_driver] = ''

@socketio.on('reply_message')
def handle_reply_message(data):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    name_chat = data['name']
    ava_chat = data['ava']
    id_message = data['id_message']
    message = data['message']
    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        if(dict_status_zalo[id_driver] != ''):
            print("bận rồi !!!", dict_status_zalo[id_driver])
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            dict_status_zalo[id_driver] = "reply_message"
            try:
                ava_check = dict_driver[id_driver].find_element('xpath','//*[@id="ava_chat_box_view"]/div[1]/div/img').get_attribute('src')
            except:
                ava_check = ''
            try:
                name_check = dict_driver[id_driver].find_element('xpath','//*[@id="header"]/div[1]/div[2]/div[1]/div[1]/div-b18').text
            except:
                name_check = ''
            try:
                if(ava_chat == ava_check and name_chat == name_check):
                    element = get_element(dict_driver[id_driver], 'xpath', f'//div[@id="{id_message}" and @data-node-type="bubble-message"]')
                    actions = ActionChains(dict_driver[id_driver])
                    actions.move_to_element(element).perform()
                    click_element(dict_driver[id_driver], 'xpath', '//*[@id="messageViewContainer"]/div[1]/div[1]/div[1]/i')
                    input_ele = get_element(dict_driver[id_driver], 'xpath', '//*[@id="input_line_0"]')
                    input_ele.click()
                    input_ele.send_keys(message)
                    input_ele.send_keys(Keys.ENTER)
            except:
                traceback.print_exc()
            dict_status_zalo[id_driver] = ''

@socketio.on('forward_message')
def handle_forward_message(data):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    name_chat = data['name']
    ava_chat = data['ava']
    id_message = data['id_mess']
    list_name = data['name_ava']

    if (id_driver in dict_driver and id_driver in dict_status_zalo):
        if (dict_status_zalo[id_driver] != '' and dict_status_zalo[id_driver] != 'abc_chuyen_tiep'):
            emit("busy", {"status": dict_status_zalo[id_driver]}, room=room)
        else:
            try:
                ava_check = dict_driver[id_driver].find_element('xpath','//*[@id="ava_chat_box_view"]/div[1]/div/img').get_attribute('src')
            except:
                ava_check = ''
            try:
                name_check = dict_driver[id_driver].find_element('xpath','//*[@id="header"]/div[1]/div[2]/div[1]/div[1]/div-b18').text
            except:
                name_check = ''
            if (ava_chat == ava_check and name_chat == name_check):
                dict_status_zalo[id_driver] = "forward_message"
                forward_list_zalo(id_driver, id_message, list_name)
                dict_status_zalo[id_driver] = ''

@socketio.on('send_message_phone')
def handle_send_message_phone(data):
    room = data["id_chat"]
    id_driver = data['id_zalo']
    num_phone = data['num_phone']
    message = data['message']
    if(id_driver in dict_driver and id_driver in dict_status_zalo):
        if(dict_status_zalo[id_driver] != ''):
            print("bận rồi !!!", dict_status_zalo[id_driver])
            emit("busy",{"status":dict_status_zalo[id_driver]},room=room)
        else:
            dict_status_zalo[id_driver] = "send_message_phone"
            try:
                click_element(dict_driver[id_driver], 'xpath', '//*[@id="main-tab"]/div[1]/div[2]/div[1]')
                click_element(dict_driver[id_driver], 'xpath', '//*[@id="contact-search-input"]')
                input_ele = get_element(dict_driver[id_driver], 'xpath', '//*[@id="contact-search-input"]')
                input_ele.send_keys(num_phone) 
                check_phone = get_element(dict_driver[id_driver], 'xpath', '/html/body/div/div/div[3]/nav/div[2]/div[3]/div/div[2]/div/div/div[1]/div/div[1]/div/div/div[2]/div/div[3]/div/div/span/span[2]', times=3, sleep_time=1)
                if check_phone:
                    check_phone = check_phone.text
                    if num_phone == check_phone:
                        input_ele.send_keys(Keys.ENTER)
                        input_ele = get_element(dict_driver[id_driver], 'xpath', '//*[@id="input_line_0"]')
                        input_ele.click()
                        input_ele.send_keys(message)
                        input_ele.send_keys(Keys.ENTER)
                else:
                    click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[1]", times=3, sleep_time=0.2)
            except:
                traceback.print_exc()
            dict_status_zalo[id_driver] = ''

# @socketio.on('add_list_friend_in_group')
# def handle_add_list_friend_in_group(data):
#     print(xong)
            

@socketio.on('check_num_login')
def handle_login(data):
    room = data['id_chat']
    emit('num_login', {'num_login': len(dict_driver)}, room=room)

@socketio.on('login')
def handle_login(data):
    room = data['id_chat']
    chrome_options = Options()
    proxy_tmp = ""
    for proxy_check in dict_proxy:
        if dict_proxy[proxy_check]:
            proxy_tmp = proxy_check
            break
    print("\nMy proxy:", proxy_tmp,"\n")
    proxy_tmp = "103.82.133.213:13501:sp08-13501:PBTQX"
    proxy_tmp = ''
    chrome_options = webdriver.ChromeOptions()
    # prefs={"profile.managed_default_content_settings.images": 2}
    # chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument("--headless=new")
    # chrome_options.add_argument("--window-position=-5000,-5000")
    # chrome_options.add_argument("--start-maximized")  # Tối đa hóa cửa sổ khi mở trình duyệt
    # chrome_options.add_experimental_option("profile.default_content_settings.popups", 0)
    if proxy_tmp != "":
        PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS = tuple(proxy_tmp.split(":"))
        # PROXY_HOST = '103.82.27.7'  # rotating proxy or host
        # PROXY_PORT = 13281 # port
        # PROXY_USER = 'sp08-13281' # username
        # PROXY_PASS = 'EUMNX' # password
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

        pluginfile = 'proxy_auth_plugin.zip'
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)

    id_driver_1 = 0
    while (str(room) + "_" + str(id_driver_1).zfill(6)) in dict_driver:
        id_driver_1 += 1
    id_driver = str(room) + "_" + str(id_driver_1).zfill(6)
    path_id_folder = os.path.join(folder_data_zalo, str(id_driver))
    if os.path.exists(path_id_folder):
        shutil.rmtree(path_id_folder)
    os.mkdir(path_id_folder)
    os.mkdir(os.path.join(path_id_folder, 'download'))

    prefs = {
    "download.prompt_for_download": False,
    "download.default_directory": os.path.join(path_id_folder, 'download')
    }
    chrome_options.add_experimental_option('prefs', prefs)

    # emit("init zalo",{"id_zalo":id_driver},room=room)
    dict_driver[id_driver] = webdriver.Chrome(options=chrome_options)
    with open(r'C:\Zalo_server\num_login.json', 'w') as json_file:
        json.dump(len(dict_driver), json_file, indent=4)

    dict_driver[id_driver].get("https://chat.zalo.me/")
    ##eventlet.sleep(0)
    base64_qr = ""
    time_login = 0
    with open(os.path.join(path_id_folder, 'logg.txt'), 'a') as f:
        f.writelines("tao file \n")
    while time_login < 60:
        print(room, time.time())
        eventlet.sleep(0)
        try:
            if dict_driver[id_driver].find_element(By.CSS_SELECTOR, '#main-tab'):
                break
            else:
                eventlet.sleep(2)
        except:
            eventlet.sleep(2)
        try:
            try:
                ##eventlet.sleep(0)
                element = dict_driver[id_driver].find_element(By.CSS_SELECTOR, "div.qrcode-expired > a")
                element.click()
                print("Đã làm mới QR code")
            except:
                pass
            # eventlet.sleep(0)
            element = dict_driver[id_driver].find_element(By.CSS_SELECTOR, "div.qr-container > img")
            src = element.get_attribute("src")
            if(base64_qr != src):
                base64_qr = src
                # eventlet.sleep(0)
                emit('qr_image', {'base64_qr': src}, room=room)
                print("da emit day nay")
                # base64_to_image(src, os.path.join(folder_data_zalo,"QR.png"))
        except:
            print("không thấy QR code")
        time_login += 2
        print("Quá thời gian chờ. QR không xuất hiện trong vòng 2 giây.")
    if time_login >= 60:
        dict_driver[id_driver].quit()
        del dict_driver[id_driver]
        emit("time_out_login", {"result":"time_out_login"}, room = room)
    else:
        if id_driver in dict_driver:
            dict_status_zalo[id_driver] = "login"
            with open(os.path.join(path_id_folder, 'logg.txt'), 'a') as f:
                f.writelines("da login\n")
            print("đã login")
            zalo_name = ""
            img_avatar = ""
            try:
                zalo_name = get_element(dict_driver[id_driver], By.CSS_SELECTOR, "div.nav__tabs__zalo.web").get_attribute("title")
                img_avatar = get_element(dict_driver[id_driver], By.CSS_SELECTOR, "div.nav__tabs__zalo.web > div > div > img", 1).get_attribute("src")
                ##eventlet.sleep(0)
            except:
                pass
            try:
                click_element(dict_driver[id_driver], 'xpath', '//*[@id="main-tab"]/div[2]/div[3]/i')
                click_element(dict_driver[id_driver], 'xpath', '/html/body/div[2]/div[2]/div/div/div-14[1]/i')
                eventlet.sleep(0.5)
                div_num_phone = get_element(dict_driver[id_driver], 'xpath', "//div[@class='pi-info-item__content' and span[@data-translate-inner='STR_PROFILE_PHONENUMBER']]")
                num_phone_zalo = get_element(div_num_phone, 'xpath', ".//span[@class='content-copiable']/p").text
                print(num_phone_zalo)
                num_phone_zalo = '0' + (''.join(char for char in num_phone_zalo if char.isdigit()))[2:]
            except:
                num_phone_zalo = ''
            click_element(dict_driver[id_driver], 'xpath', '/html/body/div[2]/div/div/div[1]/div/div[2]/i')
            print(num_phone_zalo)
            emit("success", {"name": zalo_name, "ava": img_avatar, "id_zalo": id_driver, 'num_phone_zalo': num_phone_zalo}, room=room)
            sorted_list = get_list_friend_by_bs4(id_driver)
            result = []
            for index, (name, ava) in enumerate(sorted_list):        
                tmp = {}
                tmp['id'] = str(index).zfill(6)
                tmp['name'] = name
                tmp['ava'] = ava
                result.append(tmp)
            if room in dict_zalo_online:
                dict_zalo_online[room][id_driver] = {"num_phone_zalo":num_phone_zalo, "name":zalo_name, "ava":img_avatar, "list_friend":result, "status":""}
            else:
                dict_zalo_online[room] = {}
                dict_zalo_online[room][id_driver] = {"num_phone_zalo":num_phone_zalo, "name":zalo_name, "ava":img_avatar, "list_friend":result, "status":""}
            print(dict_zalo_online[room][id_driver])
            emit("list_friend", {"id_zalo": id_driver, "list_friend":result}, room=room)
            print("emit ok")
            with open(os.path.join(path_id_folder, 'logg.txt'), 'a') as f:
                f.writelines("da emit\n")
            dict_driver[id_driver].get("https://chat.zalo.me/")
            dict_status_zalo[id_driver] = ""
            # click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[1]")
            dict_status_zalo[id_driver] = ""
            dict_status_update_data_chat[id_driver] = ''
            dict_status_update_list_chat[id_driver] = ''
            dict_folder_zalo[id_driver] = path_id_folder
            with open(r'C:\Zalo_server\login_status.json', 'w') as json_file:
                json.dump(dict_zalo_online, json_file, indent=4)
            for time_t in range(4):
                eventlet.sleep(15)
                while dict_status_zalo[id_driver] != '':
                    eventlet.sleep(2)
                dict_status_zalo[id_driver] = "get_list_friend"  
                sorted_list = get_list_friend_by_bs4(id_driver)
                result = []
                for index, (name, ava) in enumerate(sorted_list):
                    tmp = {}
                    tmp['id'] = str(index).zfill(6)
                    tmp['name'] = name
                    tmp['ava'] = ava
                    result.append(tmp)
                if result != dict_zalo_online[room][id_driver]["list_friend"]:
                    dict_zalo_online[room][id_driver]["list_friend"] = result
                    emit("list_friend", {"id_zalo": id_driver, "list_friend":result}, room=room)
                    print("Update_list_friend_ok!")
                    click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[1]", times=3, sleep_time=0.2)
                    dict_status_zalo[id_driver] = ""
                    break
                click_element(dict_driver[id_driver], "xpath", "/html/body/div/div/div[3]/nav/div[1]/div[1]/div[2]/div[1]", times=3, sleep_time=0.2)
                dict_status_zalo[id_driver] = ""

if __name__ == '__main__':
    print("da bat")
    socketio.run(app, host="103.138.113.76", port=2909, debug=False)

 