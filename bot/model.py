from dataclasses import dataclass

from aiogram import types


@dataclass
class MessageContainer:
    _message: types.Message = None

    @property
    def message(self) -> types.Message:
        return self._message

    @message.setter
    def message(self, message: types.Message) -> None:
        if self._message and message:
            raise AttributeError('Message already set, unset message first')
        self._message = message
