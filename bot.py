 # -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
from random import randint
import re
import logging

from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
from msrest.authentication import CognitiveServicesCredentials

from googlesearch import search

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

PICK, NLL, DONE  = range(3)
list = [0,True,True,True,True,True,True]
dic64 = {'111111' : '건 乾',
         '011111' : '쾌 夬',
         '101111' : '대유 大有',
         '001111' : '대장 大壯',
         '110111' : '소축 小畜',
         '010111' : '수 需',
         '100111' : '대축 大畜',
         '000111' : '태 泰',
         '111011' : '이 履',
         '011011' : '태 兌',
         '101011' : '규 睽',
         '001011' : '귀매 歸妹',
         '110011' : '중부 中孚',
         '010011' : '절 節',
         '100011' : '손 巽',
         '000011' : '임 臨',
         '111101' : '동인 同人',
         '011101' : '혁 革',
         '101101' : '리 離',
         '001101' : '풍 豊',
         '110101' : '가인 家人',
         '010101' : '기제 旣濟',
         '100101' : '비 賁',
         '000101' : '명이 明夷',
         '111001' : '무망 无妄',
         '011001' : '수 隨',
         '101001' : '서합 噬嗑',
         '001001' : '진 震',
         '110001' : '익 益',
         '010001' : '둔 屯',
         '100001' : '이 頤',
         '000001' : '복 復',
         '111110' : '구 姤',
         '011110' : '대과 大過',
         '101110' : '정 鼎',
         '001110' : '항 恒',
         '110110' : '손 巽',
         '010110' : '정 井',
         '100110' : '고 蠱',
         '000110' : '승 升',
         '111010' : '송 訟',
         '011010' : '곤 困',
         '101010' : '미제 未濟',
         '001010' : '해 解',
         '110010' : '환 渙',
         '010010' : '수 水',
         '100010' : '몽 蒙',
         '000010' : '사 師',
         '111100' : '둔 遯',
         '011100' : '함 咸',
         '101100' : '려 旅',
         '001100' : '소과 小過',
         '110100' : '점 漸',
         '010100' : '건 蹇',
         '100100' : '산 山',
         '000100' : '겸 謙',
         '111000' : '비 否',
         '011000' : '췌 萃',
         '101000' : '진 晋',
         '001000' : '예 豫',
         '110000' : '관 觀',
         '010000' : '비 比',
         '100000' : '박 剝',
         '000000' : '곤 坤'
        }

def start(bot, update, user_data):
    reply_keyboard = [['효를 뽑아요']]
    
    user_full_name = update.message.from_user.first_name + " " + update.message.from_user.last_name
    
    update.message.reply_text(
        '안녕하세요. ' + user_full_name + '님! 점쟁이봇입니다.\n\n'
        '주역 64괘 중 하나를 뽑아드려요.\n\n'
        '효를 뽑아요 버튼을 눌러주세요!',        
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    return PICK

def pick(bot, update):
    picked = randint(0,1)
    text = record(picked)
        
    update.message.reply_text(str(list[0]) + ': ' +text)
    
    if list[0] < 6:
        return pick(bot, update)
    else:
        update.message.reply_text("6효를 다 뽑았어요!", reply_markup=ReplyKeyboardRemove())
        return done(bot, update)

def record(picked):
    list[0] += 1
    if picked == 0:
        text = "양陽"
        list[list[0]] = True
    else:
        text = "음陰"
        list[list[0]] = False
        
    return text
    
def done(bot, update):
    result = calculate()
    update.message.reply_text('점괘는 ' + result + ' 입니다. '
                              '구글에서 [주역 ' + result + ']로 검색하시면 점괘 해석을 볼 수 있어요!')
    update.message.reply_text('주역 ' + result)
    update.message.reply_text(getImgUrl(result))
    update.message.reply_text('점괘 해석 link: ' + getExplain(result))
    update.message.reply_text('다시 점을 보시려면 /start 를 누르시거나 점봐주세요~ 라고 해주세요~ 안녕!')
    clear()
    
    return ConversationHandler.END
    
def calculate():
    hyo = ""
    for i in range(6,0,-1):
        if list[i] == True:
            hyo += "1"
        else:
            hyo += "0"
    logger.info("hyo : %s" % hyo)
    
    return dic64[hyo]

def getImgUrl(result):
    search_term = '주역 ' + result.split(' ')[0] + '괘'
    
    subscription_key = "ee6cdff6d00440ba84a5040435d90d6b"

    client = ImageSearchAPI(CognitiveServicesCredentials(subscription_key))
    image_results = client.images.search(query=search_term)

    if image_results.value:
        first_image_result = image_results.value[0]
        return first_image_result.content_url
    else:
        return 'http://cfile208.uf.daum.net/image/18630D3950C82953265E8A'

def getExplain(result):
    search_term = '주역 ' + result.split(' ')[0] + '괘'
    search_results = search(query='site:http://www.kookje.co.kr '+search_term,tld='co.kr',lang='ko',num=10,stop=1,pause=2)

    result_arr = []

    for i in search_results:
        result_arr.append(i)

    return result_arr[0]

def tellMeWish(bot, update):
    p = re.compile('점.')
    m = p.match(update.message.text)
    if m:
        pick(bot, update)
    else:
        update.message.reply_text('다시 점을 치고 싶으시면 점봐주세요~ 라고 해주세요~')

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('안녕 다음에 다시 만나요.', reply_markup=ReplyKeyboardRemove())
    clear()
    
    return ConversationHandler.END    
    
def clear():
    list[0] = 0
    for i in range(1,7):
        i = True

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))

def main():
    updater = Updater("361981337:AAHgUIWBfmLq9rh3Dqad2CjJDcJrAOVrKVU")
    dp = updater.dispatcher
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_user_data=True)],
        states={
            PICK: [RegexHandler('^(효를 뽑아요)$', pick)],
            NLL: [RegexHandler('^(.)$', pick)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.text, tellMeWish))
    dp.add_error_handler(error)
    
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()