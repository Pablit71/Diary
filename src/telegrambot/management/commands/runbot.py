import logging
import os
from datetime import datetime
from enum import IntEnum, auto

from django.core.management import BaseCommand
from pydantic import BaseModel

from goals.models import BoardParticipant, Goal, GoalCategory
from telegrambot.fsm.memory import Memory
from telegrambot.models import TgUser
from telegrambot.tg.client import TgClient
from telegrambot.tg.models import Message
from todolist import settings

logger = logging.getLogger(__name__)



class StateEnum(IntEnum):
    CREATE_CATEGORY_SELECT = auto()
    CHOSEN_CATEGORY = auto()


class NewGoal(BaseModel):
    cat_id: int | None = None
    goal_title: str | None = None

    @property
    def is_completed(self) -> bool:
        return None not in [self.cat_id, self.goal_title]


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)
        self.storage = Memory()

    @staticmethod
    def _gen_code() -> str:
        return os.urandom(12).hex()

    def handle_unver_user(self, msg: Message, tg_user: TgUser):
        code: str = self._gen_code()
        tg_user.verification_code = code
        tg_user.save(update_fields=('verification_code',))
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f' code: {tg_user.verification_code}'
        )

    def handle_goals_list(self, msg: Message, tg_user: TgUser):
        goals: list[str] = [
            f'#{goal.id} {goal.title}'
            for goal in Goal.objects.filter(user_id=tg_user.user_id)
        ]
        if goals:
            self.tg_client.send_message(msg.chat.id, '\n'.join(goals))
        else:
            self.tg_client.send_message(msg.chat.id, 'no goals ')

    def handle_goal_cat_list(self, msg: Message, tg_user: TgUser):
        res_cat: list[str] = [
            f'# {cat.id}: {cat.title}'
            for cat in GoalCategory.objects.filter(
                board__participants__user_id=tg_user.user_id,
                is_deleted=False
            )
        ]
        if res_cat:
            self.tg_client.send_message(msg.chat.id, '\n'.join(res_cat))
        else:
            self.tg_client.send_message(msg.chat.id, 'no category')

    def handle_save_select_cat(self, msg: Message, tg_user: TgUser):
        if msg.text.isdigit():
            cat_id = int(msg.text)
            if GoalCategory.objects.filter(
                    board__participants__user_id=tg_user.user_id,
                    board__participants__role__in=[BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                    is_deleted=False,
                    id=cat_id
            ).exists():
                self.storage.update_data(chat_id=msg.chat.id, cat_id=cat_id)
                self.tg_client.send_message(msg.chat.id, 'set title')
                self.storage.set_state(msg.chat.id, state=StateEnum.CHOSEN_CATEGORY)
            else:
                self.tg_client.send_message(msg.chat.id, 'invalid category ')

        else:
            self.tg_client.send_message(msg.chat.id, 'invalid category id')

    def handle_save_new_cat(self, msg: Message, tg_user: TgUser):
        goal = NewGoal(**self.storage.get_data(tg_user.chat_id))
        goal.goal_title = msg.text
        if goal.is_completed:
            Goal.objects.create(
                title=goal.goal_title,
                category_id=goal.cat_id,
                user_id=tg_user.user_id,
                due_date=datetime.now()
            )
            self.tg_client.send_message(msg.chat.id, 'New goal ')
        else:
            self.tg_client.send_message(msg.chat.id, 'error ')

    def handle_ver_user(self, msg: Message, tg_user: TgUser):
        if msg.text == '/goals':
            self.handle_goals_list(msg, tg_user)
        elif msg.text == '/create':
            self.handle_goal_cat_list(msg, tg_user)
            self.storage.set_state(msg.chat.id, state=StateEnum.CREATE_CATEGORY_SELECT)
            self.storage.set_data(msg.chat.id, data=NewGoal().dict())
        elif msg.text == '/cancel' and self.storage.get_state(tg_user.chat_id):
            self.storage.reset(tg_user.chat_id)
            self.tg_client.send_message(msg.chat.id, 'canceled')

        elif state := self.storage.get_state(tg_user.chat_id):
            match state:
                case StateEnum.CREATE_CATEGORY_SELECT:
                    self.handle_save_select_cat(msg, tg_user)
                case StateEnum.CHOSEN_CATEGORY:
                    self.handle_save_new_cat(msg, tg_user)
                case _:
                    logger.warning('%s', state)

        elif msg.text.startswith('/'):
            self.tg_client.send_message(msg.chat.id, 'unknown command')

    def handle_message(self, msg: Message):

        tg_user, _ = TgUser.objects.select_related('user').get_or_create(
            chat_id=msg.chat.id,
            defaults={
                'username': msg.from_.username
            }
        )
        if tg_user.user:
            self.handle_ver_user(msg=msg, tg_user=tg_user)
        else:
            self.handle_unver_user(msg=msg, tg_user=tg_user)

    def handle(self, *args, **options):
        offset = 0
        tg_client = TgClient('token')
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(msg=item.message)
            # self.tg_client.send_message(chat_id=item.message.chat.id, text=item.message.text)
            # print(item.message)
