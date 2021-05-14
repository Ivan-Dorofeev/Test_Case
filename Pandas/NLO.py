import pandas as pd
import numpy as np
import pycountry
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from yandex_translate import YandexTranslate
from yandex_translate import YandexTranslateException

# Размер надписей на графиках
PLOT_LABEL_FONT_SIZE = 14


# Генерация цветовой схемы. Возвращает список цветов
def getColors(n):
    COLORS = []
    cm = plt.cm.get_cmap('hsv', n)
    for i in np.arange(n):
        COLORS.append(cm(i))
    return COLORS


def translate(string, translator_obj=None):
    if translator_class == None:
        return string
    t = translator_class.translate(string, 'en-ru')
    return t['text'][0]
