import gc

import lcd
import sensor
import time
from maix import GPIO
from maix import KPU
from board import board_info
from fpioa_manager import fm

BOUNCE_PROTECTION = 100


def set_key_state(*_):
    global state_machine
    state_machine.emit_event(EVENT.BOOT_KEY)
    time.sleep_ms(BOUNCE_PROTECTION)


class STATE(object):
    IDLE = 0
    INIT = 1
    TRAIN_CLASS_1 = 2
    TRAIN_CLASS_2 = 3
    TRAIN_CLASS_3 = 4
    CLASSIFY = 5
    ST_MAX = 6


class EVENT(object):
    POWER_ON = 0
    BOOT_KEY = 1
    BOOT_KEY_LONG_PRESS = 2
    NEXT_CLASS = 3
    EVT_MAX = 4


class StateMachine(object):
    def __init__(self, state_handlers, event_handlers, transitions):
        self.previous_state = STATE.IDLE
        self.current_state = STATE.IDLE
        self.state_handlers = state_handlers
        self.event_handlers = event_handlers
        self.transitions = transitions
        self.records = dict()

    def get_next_state(self, cur_state, cur_event):
        '''
        根据当着状态和event, 从transitions里查找出下一个状态
        :param cur_state:
        :param cur_event:
        :return:
            next_state: 下一状态
            None: 找不到对应状态
        '''
        for cur, next, event in self.transitions:
            if cur == cur_state and event == cur_event:
                return next
        return None

    def execute_state_action(self, state):
        '''
        执行当前状态action函数
        :param state:
        :return:
        '''
        try:
            self.state_handlers[state](self)
        except Exception as e:
            print("Exception")
            print(e)

    def emit_event(self, event):
        next_state = self.get_next_state(self.current_state, event)
        if next_state == None:
            return
        print("event valid: {}, cur: {}, next: {}".format(event, self.current_state, next_state))
        self.previous_state = self.current_state
        self.current_state = next_state
        self.execute_state_action(self.current_state)

    def engine(self):
        pass


def state_init(self):
    global msg_notification
    print("current state: init")
    msg_notification = "Prepare 3 objects pls\r\nWill take 5 pics each\r\n\r\nPress boot key to\r\nstart"


def state_idle(self):
    global msg_notification
    print("current state: idle")
    msg_notification = None


def state_train_class_1(self):
    global kpu, msg_notification, features, train_pic_cnt
    global state_machine
    print("current state: class 1")
    if train_pic_cnt == 0:  # 0 is used for prompt only
        features.append([])
        train_pic_cnt += 1
        msg_notification = "Train object 1\r\n\r\nBoot key to take #P{}".format(train_pic_cnt)
    elif train_pic_cnt < max_train_pic:
        img = sensor.snapshot()
        feature = kpu.run_with_output(img, get_feature=True)
        features[0].append(feature)
        train_pic_cnt += 1
        msg_notification = "Train object 1\r\n\r\nBoot key to take #P{}".format(train_pic_cnt)
    elif train_pic_cnt == max_train_pic:  # prompt for next
        msg_notification = "Change to another\r\nobject please"
        train_pic_cnt += 1
    else:
        train_pic_cnt = 0
        state_machine.emit_event(EVENT.NEXT_CLASS)


def state_train_class_2(self):
    global kpu, msg_notification, features, train_pic_cnt
    global state_machine
    print("current state: class 2")
    if train_pic_cnt == 0:
        features.append([])
        train_pic_cnt += 1
        msg_notification = "Train object 2\r\n\r\nBoot key to take #P{}".format(train_pic_cnt)
    elif train_pic_cnt < max_train_pic:
        img = sensor.snapshot()
        feature = kpu.run_with_output(img, get_feature=True)
        features[1].append(feature)
        train_pic_cnt += 1
        msg_notification = "Train object 2\r\n\r\nBoot key to take #P{}".format(train_pic_cnt)
    elif train_pic_cnt == max_train_pic:
        msg_notification = "Change to another\r\nobject please"
        train_pic_cnt += 1
    else:
        train_pic_cnt = 0
        state_machine.emit_event(EVENT.NEXT_CLASS)


def state_train_class_3(self):
    global kpu, msg_notification, features, train_pic_cnt
    global state_machine
    print("current state: class 2")
    if train_pic_cnt == 0:
        features.append([])
        train_pic_cnt += 1
        msg_notification = "Train object 3\r\n\r\nBoot key to take #P{}".format(train_pic_cnt)
    elif train_pic_cnt < max_train_pic:
        img = sensor.snapshot()
        feature = kpu.run_with_output(img, get_feature=True)
        features[2].append(feature)
        train_pic_cnt += 1
        msg_notification = "Train object 3\r\n\r\nBoot key to take #P{}".format(train_pic_cnt)
    elif train_pic_cnt == max_train_pic:
        msg_notification = "Training is completed!\r\n\r\nPress boot to continue"
        train_pic_cnt += 1
    else:
        train_pic_cnt = 0
        state_machine.emit_event(EVENT.NEXT_CLASS)


def state_classify(self):
    global msg_notification
    print("current state: classify")
    msg_notification = "Classification"


def event_power_on(self, value=None):
    print("emit event power_on")


def event_press_boot_key(self, value=None):
    global state_machine
    print("emit event boot_key")


def event_long_press_boot_key(self, value=None):
    global state_machine
    print("emit event boot_key_long_press")


# state action table
state_handlers = {
    STATE.IDLE: state_idle,
    STATE.INIT: state_init,
    STATE.TRAIN_CLASS_1: state_train_class_1,
    STATE.TRAIN_CLASS_2: state_train_class_2,
    STATE.TRAIN_CLASS_3: state_train_class_3,
    STATE.CLASSIFY: state_classify
}

# event action table, can be enabled while needed
event_handlers = {
    EVENT.POWER_ON: event_power_on,
    EVENT.BOOT_KEY: event_press_boot_key,
    EVENT.BOOT_KEY_LONG_PRESS: event_long_press_boot_key
}

# Transition table
transitions = [
    [STATE.IDLE, STATE.INIT, EVENT.POWER_ON],
    [STATE.INIT, STATE.TRAIN_CLASS_1, EVENT.BOOT_KEY],
    [STATE.TRAIN_CLASS_1, STATE.TRAIN_CLASS_1, EVENT.BOOT_KEY],
    [STATE.TRAIN_CLASS_1, STATE.TRAIN_CLASS_2, EVENT.NEXT_CLASS],
    [STATE.TRAIN_CLASS_2, STATE.TRAIN_CLASS_2, EVENT.BOOT_KEY],
    [STATE.TRAIN_CLASS_2, STATE.TRAIN_CLASS_3, EVENT.NEXT_CLASS],
    [STATE.TRAIN_CLASS_3, STATE.TRAIN_CLASS_3, EVENT.BOOT_KEY],
    [STATE.TRAIN_CLASS_3, STATE.CLASSIFY, EVENT.NEXT_CLASS]
]


####################################################################################################################
class Button(object):
    DEBOUNCE_THRESHOLD = 30
    LONG_PRESS_THRESHOLD = 2000
    # Internal  key states
    IDLE = 0
    DEBOUNCE = 1
    SHORT_PRESS = 2
    LONG_PRESS = 3

    def __init__(self):
        self._state = Button.IDLE
        self._key_ticks = 0
        self._pre_key_state = 1
        self.SHORT_PRESS_BUFF = None

    def reset(self):
        self._state = Button.IDLE
        self._key_ticks = 0
        self._pre_key_state = 1
        self.SHORT_PRESS_BUFF = None

    def key_up(self, delta):
        global state_machine
        # print("up:{}".format(delta))
        # key up时，有缓存的key信息就发出去，没有的话直接复位状态
        if self.SHORT_PRESS_BUFF:
            state_machine.emit_event(self.SHORT_PRESS_BUFF)
        self.reset()

    def key_down(self, delta):
        global state_machine
        # print("dn:{},t:{}".format(delta, self._key_ticks))
        if self._state == Button.IDLE:
            self._key_ticks += delta
            if self._key_ticks > Button.DEBOUNCE_THRESHOLD:
                # main loop period过大时，会直接跳过去抖阶段
                self._state = Button.SHORT_PRESS
                self.SHORT_PRESS_BUFF = EVENT.BOOT_KEY  # key_up 时发送
            else:
                self._state = Button.DEBOUNCE
        elif self._state == Button.DEBOUNCE:
            self._key_ticks += delta
            if self._key_ticks > Button.DEBOUNCE_THRESHOLD:
                self._state = Button.SHORT_PRESS
                self.SHORT_PRESS_BUFF = EVENT.BOOT_KEY  # key_up 时发送
        elif self._state == Button.SHORT_PRESS:
            self._key_ticks += delta
            if self._key_ticks > Button.LONG_PRESS_THRESHOLD:
                self._state = Button.LONG_PRESS
                self.SHORT_PRESS_BUFF = None  # 检测到长按，将之前可能存在的短按buffer清除，以防发两个key event出去
                state_machine.emit_event(EVENT.BOOT_KEY_LONG_PRESS)
        elif self._state == Button.LONG_PRESS:
            self._key_ticks += delta
            # 最迟 LONG_PRESS 发出信号，再以后就忽略，不需要处理。key_up时再退出状态机。
            pass
        else:
            pass


####################################################################################################################
lcd_show_fps = True
msg_notification = None
features = []
THRESHOLD = 98.5
train_pic_cnt = 0
max_train_pic = 5

fm.register(board_info.BOOT_KEY, fm.fpioa.GPIOHS0)
boot_gpio = GPIO(GPIO.GPIOHS0, GPIO.IN)

lcd.init()
sensor.reset()  # Reset and initialize the sensor. It will
# run automatically, call sensor.run(0) to stop
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.set_windowing((224, 224))
# sensor.set_vflip(1)
sensor.skip_frames(time=500)  # Wait for settings take effect.
clock = time.clock()  # Create a clock object to track the FPS.

kpu = KPU()
print("ready load model")
kpu.load_kmodel("/sd/KPU/self_learn_classifier/mb-0.25.kmodel")

state_machine = StateMachine(state_handlers, event_handlers, transitions)
state_machine.emit_event(EVENT.POWER_ON)

i = 0
fps = 0
btn_ticks_prev = time.ticks_ms()
boot_btn = Button()
while True:
    i += 1
    gc.collect()
    clock.tick()  # Update the FPS clock.

    # query key status during main loop
    btn_ticks_cur = time.ticks_ms()
    delta = time.ticks_diff(btn_ticks_cur, btn_ticks_prev)
    btn_ticks_prev = btn_ticks_cur
    if boot_gpio.value() == 0:
        boot_btn.key_down(delta)
    else:
        boot_btn.key_up(delta)

    img = sensor.snapshot()
    if state_machine.current_state == STATE.CLASSIFY:
        scores = []
        feature = kpu.run_with_output(img, get_feature=True)
        high = 0
        index = 0
        for j in range(len(features)):
            for f in features[j]:
                score = kpu.feature_compare(f, feature)
                if score > high:
                    high = score
                    index = j
        if high > THRESHOLD:
            a = img.draw_string(0, 200, "class:{},score:{:2.1f}".format(index + 1, high), color=(0, 255, 0), scale=2)
    if lcd_show_fps:
        img.draw_string(0, 0, "{:.2f}fps".format(fps), color=(0, 255, 0), scale=1.0)
    if msg_notification:
        img.draw_string(0, 60, msg_notification, color=(255, 0, 0), scale=2)
    lcd.display(img)
    fps = clock.fps()
