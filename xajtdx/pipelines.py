# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import codecs
import csv
import os
import requests

#将关键字存入列表
bre_man = "家庭氧疗、呼吸操、呼吸锻炼、呼吸功能锻炼、呼吸训练、腹式呼吸、缩唇呼吸、全身操呼吸"
dis_man = "用药常识、免疫力、养生、家庭护理、服药、吃药时间、药效、高温防中暑、急救电话、copd、不良习惯、老人"
pre_cold_man = "流行性感冒、流感、感冒、冬天、冬季、戴口罩、保暖、肺炎球菌疫苗"
away_harm_man = "抽烟、吸烟、烟民、戒烟、二手烟、雾霾、空气污染、煮妇肺"
dis_cog_man = "慢阻肺、慢性阻塞性肺病、慢性阻塞性肺疾病、COPD"
men_man = "心理、失眠、快乐、心态、心境、乐观、积极、生气、情绪、开心、抑郁"
eat_man = "蔬菜、水果、维生素、饮食、食品、食物、喝水、糖、盐、脂肪、膳食、营养、吃、喝"
sports_man = "老年人运动、健步走、步行、锻炼、太极拳"

bre_man_lists = bre_man.split("、")
dis_man_lists = dis_man.split("、")
pre_cold_man_lists = pre_cold_man.split("、")
away_harm_man_lists = away_harm_man.split("、")
dis_cog_man_lists = dis_cog_man.split("、")
men_man_lists = men_man.split("、")
eat_man_lists = eat_man.split("、")
sports_man_lists = sports_man.split("、")

manage_lists = list()
manage_lists.append(bre_man_lists)
manage_lists.append(dis_man_lists)
manage_lists.append(pre_cold_man_lists)
manage_lists.append(away_harm_man_lists)
manage_lists.append(dis_cog_man_lists)
manage_lists.append(men_man_lists)
manage_lists.append(eat_man_lists)
manage_lists.append(sports_man_lists)

class GetwantedartPipeline(object):

    def csv_write(self, data, file_path):
        with codecs.open(file_path, "ab", encoding="utf8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data)

    def dir_path_jud(self, manage_list):
        if manage_list == dis_man_lists:
            path = "dis_man"
        elif manage_list == bre_man_lists:
            path = "bre_man"
        elif manage_list == pre_cold_man_lists:
            path = "pre_cold_man"
        elif manage_list == away_harm_man_lists:
            path = "away_harm_man"
        elif manage_list == dis_cog_man_lists:
            path = "dis_cog_man"
        elif manage_list == men_man_lists:
            path = "men_man"
        elif manage_list == eat_man_lists:
            path = "eat_man"
        else:
            path = "sports_man"
        return path

    def file_write(self, title, content,dir_path):
        file_path = dir_path + "/xianjiaoda.csv"
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        if not os.path.exists(file_path):
            self.csv_write(["title_html", "article_html"], file_path)
        self.csv_write([title, content], file_path)




    def process_item(self, item, spider):
        title = item["title"]
        content = item["html"]
        image_urls_ful = item["image_urls_ful"]
        image_urls_old = item["image_urls_old"]
        imag_url_len = len(image_urls_ful)
        #########将html中的图片不完整链接替换成完整链接
        for i in range(0,imag_url_len):
            content = content.replace(image_urls_old[i],imag_url_len[i])
        for manage_list in manage_lists:
            for i in manage_list:
                if i in title:
                    path = self.dir_path_jud(manage_list)
                    dir_path = "./" + path
                    self.file_write(title, content, dir_path)
                    break
        return item