### Compensation Z

Дополнение Compensation Z к интерфейсу Gmoccapy используется для отслеживания <br />
с высокой точностью перепада высот обрабатываемой детали по Z в таких операциях, <br />
как поверхностная гравировка, фрезеровка дорожек печатных плат и других случаях, <br />
когда необходимо ‘повторять’ неровную поверхность детали и нельзя срезать лишнее. <br />

Процесс состоит из двух частей:
1. Сканирование поверхности с помощью щупа (probe). <br />
Позже добавлю программы в папку programs и pyngcgui. <br />

2. Фрезеровка с включенной функцией Compensation Z. <br />
Нажимаем «Open», затем «Enable» <br />
Автоматическая компенсация включена. <br />
Запускаем свою программу обработки поверхности .ngc <br />
Для выключения компенсации ещё раз нажимаем «Enable» <br />

### Установка

Скопировать в папку станка: <br />
compensation_z.glade <br />
compensation_z.hal <br />
compensation_z.py <br />
filename.txt <br />

Добавить в .ini файл: <br />
[DISPLAY] <br />
EMBED_TAB_NAME = my_new_panel <br />
EMBED_TAB_LOCATION = box_spindle <br />
EMBED_TAB_COMMAND = gladevcp -x {XID} -u compensation_z.py -H compensation_z.hal compensation_z.glade <br />

EMBED_TAB_NAME = Представляет имя вкладки или боковой панели. <br />
EMBED_TAB_LOCATION = Место, где ваша программа будет размещена в графическом интерфейсе. <br />

ntb_user_tabs (как основная вкладка, покрывающая весь экран) <br />
ntb_preview (как вкладка на стороне предварительного просмотра) <br />
hbox_jog (скроет кнопки пробежки и представит здесь ваш Glade-файл) <br />
box_left (слева, по всей высоте экрана) <br />
box_right (справа, между обычным экраном и списком кнопок) <br />
box_tool_and_code_info (скроет информацию об инструменте и кадры G-кода и представит ваш Glade-файл здесь) <br />
box_tool_info (скроет фрейм информации об инструменте и представит здесь ваш Glade-файл) <br />
box_code_info (скроет информационный кадр G-кода и представит здесь ваш Glade-файл) <br />
box_vel_info (скроет кадры скорости и представит ваш Glade-файл) <br />
box_coolant_and_spindle (скроет рамки СОЖ и шпинделя и поместит ваш файл Glade здесь) <br />
box_cooling (скроет рамку охлаждения и представит ваш Glade-файл) <br />
box_spindle (скроет рамку шпинделя и представит ваш файл Glade) <br />
box_custom_1 (слева от vel_frame) <br />
box_custom_2 (слева от cooling_frame) <br />
box_custom_3 (слева от spindle_frame) <br />
box_custom_4 (справа от spindle_frame) <br />
box_dro_side (справа от DRO) <br />
