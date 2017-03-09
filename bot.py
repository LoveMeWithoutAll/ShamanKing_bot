 # -*- coding: utf-8 -*-
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler)
from random import randint
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

PICK, DONE  = range(2)
list = [0,True,True,True,True,True,True]
dic64 = {'111111' : '건乾',
         '011111' : '쾌夬',
         '101111' : '대유大有',
         '001111' : '대장大壯',
         '110111' : '소축小畜',
         '010111' : '수需',
         '100111' : '대축大畜',
         '000111' : '태泰',
         '111011' : '이履',
         '011011' : '태兌',
         '101011' : '규睽',
         '001011' : '귀매歸妹',
         '110011' : '중부中孚',
         '010011' : '절節',
         '100011' : '손巽',
         '000011' : '임臨',
         '111101' : '동인同人',
         '011101' : '혁革',
         '101101' : '리離',
         '001101' : '풍豊',
         '110101' : '가인家人',
         '010101' : '기제旣濟',
         '100101' : '비賁',
         '000101' : '명이明夷',
         '111001' : '무망无妄',
         '011001' : '수隨',
         '101001' : '서합噬嗑',
         '001001' : '진震',
         '110001' : '익益',
         '010001' : '둔屯',
         '100001' : '이頤',
         '000001' : '복復',
         '111110' : '구姤',
         '011110' : '대과大過',
         '101110' : '정鼎',
         '001110' : '항恒',
         '110110' : '손巽',
         '010110' : '정井',
         '100110' : '고蠱',
         '000110' : '승升',
         '111010' : '송訟',
         '011010' : '곤困',
         '101010' : '미제未濟',
         '001010' : '해解',
         '110010' : '환渙',
         '010010' : '수水',
         '100010' : '몽蒙',
         '000010' : '사師',
         '111100' : '둔遯',
         '011100' : '함咸',
         '101100' : '려旅',
         '001100' : '소과小過',
         '110100' : '점漸',
         '010100' : '건蹇',
         '100100' : '산山',
         '000100' : '겸謙',
         '111000' : '비否',
         '011000' : '췌萃',
         '101000' : '진晋',
         '001000' : '예豫',
         '110000' : '관觀',
         '010000' : '비比',
         '100000' : '박剝',
         '000000' : '곤'
        }

def start(bot, update, user_data):
    reply_keyboard = [['효를 뽑아요']]
    
    update.message.reply_text(
        '안녕하세요. 주역봇입니다.\n\n'
        '주역 64괘 중 하나를 뽑아드려요.\n\n'
        '효를 뽑아요 버튼을 눌러주세요!',        
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    return PICK

def pick(bot, update):
    reply_keyboard = [['효를 뽑아요']]
    
    picked = randint(0,1)
    text = record(picked)
        
    update.message.reply_text(str(list[0]) + ': ' +text,reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    
    if list[0] < 6:
        return PICK
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
    update.message.reply_text('다시 점을 보시려면 채팅창에 /start 을 누르세요! 안녕!')
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

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('안녕 다음에 다시 만나요.', reply_markup=ReplyKeyboardRemove())
        
    return ConversationHandler.END    
    
def clear():
    list[0] = 0
    for i in range(1,7):
        i = True

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    updater = Updater("Token")
    dp = updater.dispatcher
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start, pass_user_data=True)],
        states={
            PICK: [RegexHandler('^(효를 뽑아요)$', pick)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    dp.add_handler(conv_handler)
    dp.add_error_handler(error)
    
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()