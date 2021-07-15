# -*- coding:utf-8 -*-
# @Time : 2021/7/13 10:46 下午
# @Author : tonysu
import pandas as pd
from pyhanlp import *
from ngram import NGram
import os

# 显示所有列
pd.set_option('display.max_columns', None)


def main_fun(input, output, keyword, n=2):
    """
    :param input: 文件夹路径
    :param output: 输出文件路径
    :param keyword: 文件名称包含关键词
    :param n: ngram中的n
    :return:
    """
    bgram = NGram(N=n)
    poetrys = list()
    for file in os.listdir(input):
        file = input + '/' + file
        if keyword is not None and keyword != '':
            if keyword in file:
                df = pd.read_json(file)
                try:
                    preprocess(df, ngram=bgram)
                except Exception:
                    print(file)
                poetrys.append(df['simple_paragraphs_bgram'].to_list())
        else:
            df = pd.read_json(file)
            try:
                preprocess(df, ngram=bgram)
            except Exception:
                print(file)
            poetrys.append(df['simple_paragraphs_bgram'].to_list())

    result = word_count(poetrys)
    lines = []
    for word in result:
        lines.append(str(word[0] + "：" + str(word[1]) + "\n"))
        print(word[0] + "：" + str(word[1]))
    print("开始输出结果")
    write_to_txt(output, lines)
    print("结果输出成功")


def write_to_txt(output, lines):
    """
    写出lines到文件
    :param output: 输出路径
    :param lines: 数据
    :return:
    """
    print(output)
    file = open(output, 'w')
    file.writelines(lines)


def preprocess(df, ngram):
    """
    数据预处理
    :param df: 数据dataframe
    :param ngram: ngrame
    :return:
    """
    df['paragraphs'] = df['paragraphs'].str.join('')
    df['tags'] = df['tags'].str.join(',')
    df['simple_author'] = df['author'].map(HanLP.convertToSimplifiedChinese)
    df['simple_paragraphs'] = df['paragraphs'].map(HanLP.convertToSimplifiedChinese)
    df['simple_title'] = df['title'].map(HanLP.convertToSimplifiedChinese)
    df['simple_paragraphs_bgram'] = df['simple_paragraphs'].map(ngram.split).map(list)
    return df


def replace_stop_word(line):
    """
    去除停用词
    :param line:
    :return:
    """
    line = line.replace(',', '')\
        .replace('，', '') \
        .replace('.', '') \
        .replace('。', '') \
        .replace('$', '') \
        .replace('[', '') \
        .replace(']', '') \
        .replace('□', '') \
        .replace('《', '') \
        .replace('》', '') \
        .replace('/', '') \
        .replace('|', '') \
        .replace('{', '') \
        .replace('}', '') \
        .replace('〖', '') \
        .replace('〗', '') \
        .replace('『', '') \
        .replace('』', '') \
        .replace('、', '') \
        .replace('〈', '') \
        .replace('〉', '') \
        .replace('…', '') \
        .replace('”', '') \
        .replace('“', '') \
        .replace('（', '') \
        .replace('）', '') \
        .replace('·', '') \
        .replace('-', '') \
        .replace('=', '') \
        .replace('○', '') \
        .replace('？', '') \
        .replace('⿰', '') \
        .replace('+', '') \
        .replace('1', '') \
        .replace('●', '')
    return line


def word_count(datas):
    """
    进行词频统计
    :param datas: 数据
    :return:
    """
    result = {}
    for data in datas:
        for words in data:
            for word in words:
                word = replace_stop_word(word)
                if word != '':
                    if word in result.keys():
                        result[word] = result[word] + 1
                    else:
                        result[word] = 1

    result = sorted(result.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    return result


if __name__ == "__main__":
    input_path = '/Users/ssh/Documents/private/project/github/name_service/data/chinese-poetry-master/json'
    output_path = "/Users/ssh/Documents/private/project/github/name_service/data/output/tangsi.txt"
    main_fun(input=input_path, output=output_path, keyword='poet.tang', n=2)
    # file = open("/Users/ssh/Documents/private/project/github/name_service/data/output/tangsi.txt", "w")
