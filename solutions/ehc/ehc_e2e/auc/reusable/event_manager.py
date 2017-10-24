#  Copyright 2016 EMC HCE SW Automation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


class Event(object):
    """
    Provide eventing functionality to achieve register and notification
    pattern.

    Example:
    class EventPublisher(object):
        '''
        the event handler can be instance member of class member. This depends
        on the actual scenarios needs the event is used.
        '''

        def __init__(self):
            self.event_handler = Event(name='publisher')

        def do_work(self, *args):
            self.on_raise_event(*args)

        def on_raise_event(self, *args):
            '''
            Wrap event invocation.
            '''
            if self.event_handler:
                self.event_handler(*args)


    def foo_callback(*args):
        ''' callback to register to the event.
        The signature of the function needs to be identical when
        subscribing to one event.'''
        print 'example event fired to foo_callback with args: {}'.format(
        ''.join([str(i) for i in args]))

    def bar_callback(*args):
        ''' callback to register to the event.
        The signature of the function needs to be identical when
        subscribing to one event.'''
        print 'example event fired to bar_callback with args: {}'.format(
        ''.join([str(i) for i in args]))

    pub = EventPublisher()
    pub.event_handler += foo_callback
    pub.event_handler += bar_callback
    pub.do_work('let us go')
    """
    def __init__(self, name, *args):
        self._handlers = set()
        self._args = args
        self.name = name

    def add(self, callback):
        self._handlers.add(callback)
        return self

    def remove(self, callback):
        self._handlers.remove(callback)
        del callback
        return self

    def clear(self):
        self._handlers.clear()

    def fire(self, *args):
        final_args = ('Event:{}'.format(self.name),) + self._args + args
        if self._handlers:
            for handler in self._handlers:
                handler(final_args)
        else:
            return None

    __iadd__ = add
    __isub__ = remove
    __call__ = fire


class EventPublisher(object):
    def __init__(self):
        self.event_handler = Event(name='publisher')

    def do_work(self, *args):
        self.on_raise_event(*args)

    def on_raise_event(self, *args):
        if self.event_handler:
            self.event_handler(*args)


def foo_callback(*args):
    print 'Event fired to foo_callback with args: {}'.format(''.join([str(i) for i in args]))


def bar_callback(*args):
    print 'Event fired to bar_callback with args: {}'.format(''.join([str(i) for i in args]))


if __name__ == '__main__':
    pub = EventPublisher()
    pub.event_handler += foo_callback
    pub.event_handler += bar_callback
    pub.do_work('let us go')
