# -*- coding: utf-8 -*-
from django.test import TestCase
from apps.defaultapp.tools.number import NumberFinder

__author__ = 'erhmutlu'


class NumberFinderTest(TestCase):

    def setUp(self):
        self.finder = NumberFinder()

    #MILLIONS
    def test_find_numbers_with_million_successfully(self):
        sentence = u'beş milyon'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 5000000)
        self.assertEqual(dict["word"], u"beş milyon")

    def test_find_numbers_with_million_successfully_case2(self):
        sentence = u'beş yüz altmış dört milyon'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 564000000)
        self.assertEqual(dict["word"], u"beş yüz altmış dört milyon")

    def test_find_numbers_with_million_successfully_case3(self):
        sentence = u'bir milyon'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 1000000)
        self.assertEqual(dict["word"], u"bir milyon")

    def test_find_numbers_with_million_successfully_case4(self):
        sentence = u'1 milyon'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 1000000)
        self.assertEqual(dict["word"], u"1 milyon")

    def test_find_numbers_with_million_successfully_case5(self):
        sentence = u'564 milyon'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 564000000)
        self.assertEqual(dict["word"], u"564 milyon")

    def test_find_numbers_with_million_successfully_case6(self):
        sentence = u'altmış milyon'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 60000000)
        self.assertEqual(dict["word"], u"altmış milyon")

    def test_find_numbers_with_million_successfully_case7(self):
        sentence = u'altmış sekiz milyon'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 68000000)
        self.assertEqual(dict["word"], u"altmış sekiz milyon")

    def test_find_numbers_with_million_successfully_case8(self):
        sentence = u'68000000'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 68000000)
        self.assertEqual(dict["word"], u"68000000")

    def test_find_numbers_with_million_successfully_case9(self):
        sentence = u'5 yüz altmış dört milyon'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 564000000)
        self.assertEqual(dict["word"], u"5 yüz altmış dört milyon")

    def test_find_numbers_with_million_successfully_case10(self):
        sentence = u'5 yüz 64 milyon'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 564000000)
        self.assertEqual(dict["word"], u"5 yüz 64 milyon")

    def test_find_numbers_with_million_successfully_case11(self):
        sentence = u'5 yüz altmış 4 milyon'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 564000000)
        self.assertEqual(dict["word"], u"5 yüz altmış 4 milyon")

    def test_find_numbers_with_million_successfully_case12(self):
        sentence =u'500 altmış 4 milyon'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 564000000)
        self.assertEqual(dict["word"], u"500 altmış 4 milyon")

    def test_find_numbers_with_million_successfully_case13(self):
        sentence = u'yüz elli 2 milyon'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 152000000)
        self.assertEqual(dict["word"], u"yüz elli 2 milyon")

    #THOUSANDS
    def test_find_numbers_with_thousand_successfully_case1(self):
        sentence = u'2 bin'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 2000)
        self.assertEqual(dict["word"], u"2 bin")

    def test_find_numbers_with_thousand_successfully_case2(self):
        sentence = u'bin'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 1000)
        self.assertEqual(dict["word"], u"bin")

    def test_find_numbers_with_thousand_successfully_case3(self):
        sentence = u'5 yüz 88 bin'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 588000)
        self.assertEqual(dict["word"], u"5 yüz 88 bin")

    def test_find_numbers_with_thousand_successfully_case4(self):
        sentence = u'altı bin'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 6000)
        self.assertEqual(dict["word"], u"altı bin")

    def test_find_numbers_with_thousand_successfully_case5(self):
        sentence = u'999 bin kalem'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 999000)
        self.assertEqual(dict["word"], u"999 bin")

    #HUNDREDS
    def test_find_numbers_with_hundred_successfully_case1(self):
        sentence = u'999'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 999)
        self.assertEqual(dict["word"], u"999")

    def test_find_numbers_with_hundred_successfully_case2(self):
        sentence = u'9 yüz on 4'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 914)
        self.assertEqual(dict["word"], u"9 yüz on 4")

    def test_find_numbers_with_hundred_successfully_case3(self):
        sentence = u'yerde 9 yüz kırk kalem'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 940)
        self.assertEqual(dict["word"], u"9 yüz kırk")

    def test_find_numbers_with_hundred_successfully_case4(self):
        sentence = u'100'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 100)
        self.assertEqual(dict["word"], u"100")

    # TENS
    def test_find_numbers_with_ten_successfully_case1(self):
        sentence = u'10'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 10)
        self.assertEqual(dict["word"], u"10")

    def test_find_numbers_with_ten_successfully_case2(self):
        sentence = u'70'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 70)
        self.assertEqual(dict["word"], u"70")

    def test_find_numbers_with_ten_successfully_case3(self):
        sentence = u'elli'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 50)
        self.assertEqual(dict["word"], u"elli")

    def test_find_numbers_with_ten_successfully_case4(self):
        sentence = u'79'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 79)
        self.assertEqual(dict["word"], u"79")

    def test_find_numbers_with_ten_successfully_case5(self):
        sentence = u'otuz üç'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 33)
        self.assertEqual(dict["word"], u"otuz üç")

    def test_find_numbers_with_ten_successfully_case6(self):
        sentence = u'otuz 3'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 33)
        self.assertEqual(dict["word"], u"otuz 3")

    def test_find_numbers_with_ten_successfully_case7(self):
        sentence = u'otuz üç insan'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 33)
        self.assertEqual(dict["word"], u"otuz üç")

    def test_find_numbers_with_ten_successfully_case8(self):
        sentence = u'altmış kedi'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 60)
        self.assertEqual(dict["word"], u"altmış")

    def test_find_numbers_with_ten_successfully_case9(self):
        sentence = u'altmışken gel'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 0)

    def test_find_numbers_with_ten_successfully_case10(self):
        sentence = u'yetmişken gelme'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 0)

    def test_find_numbers_with_ten_successfully_case11(self):
        sentence = u'belli gelme'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 0)

    def test_find_numbers_with_ten_successfully_case12(self):
        sentence = u'yerde otuz üç'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 33)
        self.assertEqual(dict["word"], u"otuz üç")

    def test_find_numbers_with_ten_successfully_case13(self):
        sentence = u'30da'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 30)
        self.assertEqual(dict["word"], u"30")

    # ONE DIGIT
    def test_find_numbers_with_onedigit_successfully_case1(self):
        sentence = u'güç'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 0)

    def test_find_numbers_with_onedigit_successfully_case2(self):
        sentence = u'üçlü kedi'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 0)

    def test_find_numbers_with_onedigit_successfully_case3(self):
        sentence = u'üç'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 3)
        self.assertEqual(dict["word"], u"üç")

    def test_find_numbers_with_onedigit_successfully_case4(self):
        sentence = u'altında'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 0)

    def test_find_numbers_with_onedigit_successfully_case5(self):
        sentence = u'9'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 9)
        self.assertEqual(dict["word"], u"9")

    def test_find_numbers_with_onedigit_successfully_case6(self):
        sentence = u'1 keçi'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 1)
        self.assertEqual(dict["word"], u"1")

    def test_find_numbers_with_onedigit_successfully_case7(self):
        sentence = u'saat 7de'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 7)
        self.assertEqual(dict["word"], u"7")


    # MIXED
    def test_find_numbers_mix_successfully_case1(self):
        sentence = u'2 milyon beş yüz bin'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 2500000)
        self.assertEqual(dict["word"], u"2 milyon beş yüz bin")

    def test_find_numbers_mix_successfully_case2(self):
        sentence = u'2 milyon beş yüz 60 bin 3 yüz'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 2560300)
        self.assertEqual(dict["word"], u"2 milyon beş yüz 60 bin 3 yüz")

    def test_find_numbers_mix_successfully_case3(self):
        sentence = u'altı milyon 1'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 6000001)
        self.assertEqual(dict["word"], u"altı milyon 1")

    def test_find_numbers_mix_successfully_case4(self):
        sentence = u'altı milyon 71 kalem'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 1)
        dict = result[0]
        self.assertEqual(dict["digit"], 6000071)
        self.assertEqual(dict["word"], u"altı milyon 71")

    #MULTIPLE NUMBERS
    def test_find_multiple_numbers_successfully_case1(self):
        sentence = u'altı milyon 71 kalem 63'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 2)

        dict1 = result[0]
        self.assertEqual(dict1["digit"], 6000071)
        self.assertEqual(dict1["word"], u"altı milyon 71")

        dict2 = result[1]
        self.assertEqual(dict2["digit"], 63)
        self.assertEqual(dict2["word"], u"63")

    def test_find_multiple_numbers_successfully_case2(self):
        sentence = u'iki kalem 66 silgi'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 2)

        dict1 = result[0]
        self.assertEqual(dict1["digit"], 2)
        self.assertEqual(dict1["word"], u"iki")

        dict2 = result[1]
        self.assertEqual(dict2["digit"], 66)
        self.assertEqual(dict2["word"], "66")

    def test_find_multiple_numbers_successfully_case3(self):
        sentence = u'iki kalem 66 silgi 3 milyon türk lirası'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 3)

        dict1 = result[0]
        self.assertEqual(dict1["digit"], 2)
        self.assertEqual(dict1["word"], u"iki")

        dict2 = result[1]
        self.assertEqual(dict2["digit"], 66)
        self.assertEqual(dict2["word"], u"66")

        dict3 = result[2]
        self.assertEqual(dict3["digit"], 3000000)
        self.assertEqual(dict3["word"], u"3 milyon")

    def test_find_multiple_numbers_successfully_case4(self):
        sentence = u'bin 66 silgi on sekiz türk lirası'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 2)

        dict1 = result[0]
        self.assertEqual(dict1["digit"], 1066)
        self.assertEqual(dict1["word"], u"bin 66")

        dict2 = result[1]
        self.assertEqual(dict2["digit"], 18)
        self.assertEqual(dict2["word"], u"on sekiz")

    def test_find_multiple_numbers_successfully_case5(self):
        sentence = u'saat 3 45'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 2)

        dict1 = result[0]
        self.assertEqual(dict1["digit"], 3)
        self.assertEqual(dict1["word"], u"3")

        dict2 = result[1]
        self.assertEqual(dict2["digit"], 45)
        self.assertEqual(dict2["word"], u"45")

    def test_find_multiple_numbers_successfully_case6(self):
        sentence = u'kalemin fiyatı 2 tl olmuş 2016 yılında'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 2)

        dict1 = result[0]
        self.assertEqual(dict1["digit"], 2)
        self.assertEqual(dict1["word"], u"2")

        dict2 = result[1]
        self.assertEqual(dict2["digit"], 2016)
        self.assertEqual(dict2["word"], u"2016")

    def test_find_multiple_numbers_successfully_case7(self):
        sentence = u'kalemin fiyatı 2 tl olmuş 2 milyon yılda'
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 2)

        dict1 = result[0]
        self.assertEqual(dict1["digit"], 2)
        self.assertEqual(dict1["word"], u'2')

        dict2 = result[1]
        self.assertEqual(dict2["digit"], 2000000)
        self.assertEqual(dict2["word"], u"2 milyon")

    def test_find_multiple_numbers_successfully_case8(self):
        sentence = u"İstanbulda 3 Mart'ta saat 3 hava durumu nasıl"
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 2)

        dict1 = result[0]
        self.assertEqual(dict1["digit"], 3)
        self.assertEqual(dict1["word"], u"3")

        dict2 = result[1]
        self.assertEqual(dict2["digit"], 3)
        self.assertEqual(dict2["word"], u"3")

    def test_find_time1(self):
        sentence = u"saat 19 30 6"
        result = self.finder.find(sentence)
        self.assertEqual(len(result), 2)

        dict1 = result[0]
        self.assertEqual(dict1["digit"], 19)

        dict2 = result[1]
        self.assertEqual(dict2["digit"], 36)




