
#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Tests with modifying QSpinBox to the desired behavior

It might be possible, but ..."""


#4:29:34 < TLE> Hallo Qt gurus. Resisting the urge to reimplement by hand, I'm looking for a way to make a QSpinBox not change value (not emit the signal and not 
#                actually change it) when text is intered, before enter is pressed or focus is lost
#14:30:47 < TLE> Do you have some pointers for how to accomplish that? I have been toying around with the editingFinished signal and validate, but I can't seem to 
#                figure it out
#14:31:13 < altendky> TLE: the editingFinished signal isn't the one you want to monitor?
#14:32:08 -!- puff [~stevenjow@static-108-32-33-25.pitbpa.fios.verizon.net] has quit [Read error: Connection reset by peer]
#14:32:23 < TLE> altendky: Well, the problem is, that if I want to write 12, the singal valueChanged is emitted on 1
#14:33:08 < altendky> TLE: ok.  you can't just connect everything to editingFinished instead of valueChanged?
#14:33:20 -!- puff [~stevenjow@static-108-32-33-25.pitbpa.fios.verizon.net] has joined #pyqt
#14:33:50 < TLE> altendky: not really, then the steppers don't emit and it will also emit on focus loss even though nothing changed
#14:34:03 < altendky> mm
#14:35:53 < altendky> TLE: and what's the application where this matters?  i'm sure it does, just trying to understand a bit better.  i have a situation that may 
#                     be similar though just with text boxes.
#14:35:56 < TLE> I have tried emitting a custom signal on editing finished and in the stepBy method, but as I said, that doesn't really change the fundamental 
#                problem, that the value of the widget _does_ change on 1, even if I don't emit
#14:37:01 < altendky> TLE: well, you probably can't change the internal workings without rewriting the internal workings.  but you may be able to create an object 
#                     that receives the widget's events and whatever signals you need and outputs your desired interface.
#14:37:16 < TLE> altendky: I working on a GUI toolkit for scientific purposes, specially to drive lab equipment, and there you really don't want to send 
#                intermediate values to the equipment, before the user is done typing
#14:37:18 < altendky> TLE: then you just have to be sure to use that rather than the original widget it wraps
#14:38:23 < altendky> TLE: alrighty, same thing as i had.  https://github.com/altendky/st  they had me make it so you had to press enter in the textbox to confirm 
#                     the value.  losing focus and esc canceled the change and reset the text, iirc.
#14:40:08 < TLE> altendky: sounds similar to the considerations I am having. I think maybe I will have to write from scratch. It is just a shame, because I would 
#                prefer to keep all the functionality that keeping the original widgets gives you
#14:40:29 < altendky> TLE: sure, just create a new interface like i said.
#14:41:23 < altendky> TLE: a separate object that you use to wrap up the existing widget.  it can cache the value and only update the cache when confirmed.  it 
#                     can emit changed only when editing finished or spinbox clicked. etc
#14:41:36 < altendky> TLE: are you familiar with event filters?
#14:41:50 < altendky> TLE: you may or may not need them as well
#14:43:37 < TLE> altendky: event filters, no I will google it
#14:44:15 < altendky> TLE: or, if you prefer, you could inherit and implement a different interface that you use.  signal like valueConfirmed or somesuch
#14:44:49 < altendky> https://github.com/altendky/st/blob/lib/epyqlib/widgets/epc.py#L62
#14:45:09 < altendky> TLE: i'm not sure it's great but it is a little code to look at.
#14:45:36 < altendky> TLE: but do read the docs on eventFilter so you understand how it can 'consume' the event or not etc
#14:47:15 < TLE> altendky: yes, I will experiment a little more with those two ideas. I was just wondering whether there was something I missed with regards to 
#                changing QSpinBox behavior.
#14:47:23 < TLE> altendky: Thanks for all the input.
#14:48:04 < altendky> TLE: i can't say i'm intimately familiar with the spinbox details.  but it does sound like something that may well not be readily available
#14:50:57 < altendky> TLE: or...  http://doc.qt.io/qt-5/qabstractspinbox.html#keyboardTracking-prop
#14:50:59 < TLE> altendky: I guess it is also possible that I could achieve the result by subclassing QAbstractSpinBox myself
#14:51:39 < altendky> found via https://stackoverflow.com/a/10224973/228539
#14:52:56 < TLE> altendky: WOW, that looks like that might just do the trick, thanks


# TODO use keyboard tracking and see what .value gives in the mean time



import sys
from PyQt5.QtWidgets import (
    QSpinBox, QLabel, QDoubleSpinBox,
    QLineEdit, QApplication, QWidget,
)
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtGui import QKeyEvent



class MySpinBox(QDoubleSpinBox):

    ubd_value_changed = pyqtSignal(int)

    def __init__(self, *args, change_on_focus_loss=False, spinners=True,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.change_on_focus_loss = change_on_focus_loss
        self.spinners = spinners
        # This disabled value changes while typing
        self.setKeyboardTracking(False)
        self.installEventFilter(self)
        if not spinners:
            self.setButtonSymbols(2)
        self.editingFinished.connect(self.edf)
        self.valueChanged.connect(self.value_changed)

    def stepBy(self, step):
        # FIXME not really sure about this, figure out some way to
        # disable keyboard shortcuts when spinners are disabled
        if not self.spinners:
            return
        super().stepBy(step)
        self.ubd_value_changed.emit(self.value())

    def eventFilter(self, obj, event):
        if isinstance(event, QKeyEvent):
            print("#Event filter", obj, event, event.key())
        return super().eventFilter(obj, event)

    def value_changed(self, int_):
        print("value changed", int_)

    def edf(self):
        self.ubd_value_changed.emit(self.value())


class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check)
        self.timer.setInterval(1000)
        self.timer.start()

    def check(self):
        print("Value is now", self.qle.value())
        
    def initUI(self):

        self.lbl = QLabel(self)
        qle = MySpinBox(self, spinners=False)
        self.qle = qle
        qle.setKeyboardTracking(False)
        qle2 = MySpinBox(self)
        qle2.setKeyboardTracking(False)
        
        qle.move(60, 100)
        self.lbl.move(60, 40)

        qle.ubd_value_changed.connect(self.onChanged)
        #qle.valueChanged.connect(self.vc)
        #qle.editingFinished.connect(self.edf)
        
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QSpinboxTest')
        self.show()
        
        
    def onChanged(self, int_):
        print("### UBD value changed", int_)
        self.lbl.setText(str(int_))
        self.lbl.adjustSize()

    #def vc(self, int_):
    #    print("VC", int_)
    

    #def edf(self):
    #    print("edf")
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
