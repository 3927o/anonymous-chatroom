import unittest
import time

from test.base import BaseTestCase
from chatroom.models import User, Message, Room, db


def add_tool(*item):
    for i in item:
        db.session.add(i)


class DatabaseTestCase(BaseTestCase):

    def test_user(self):
        user1 = User('user1', '123456')
        user2 = User('user2', '123456')
        user3 = User('user1', '123456')
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()
        self.assertEqual(user1.id, 1)
        self.assertEqual(user2.id, 2)
        self.assertEqual(user1.username, 'user1')
        print(user1.register_at)
        print(user2.register_at)
        self.assertTrue(user1.validate_password('123456'))

    def test_room(self):
        room1 = Room('room1')
        room2 = Room('room2', 'room2')
        add_tool(room1, room2)
        db.session.commit()
        print(room1.id)
        print(room2.id)
        self.assertEqual(room1.name, 'room1')
        self.assertEqual(room2.name, 'room2')
        self.assertEqual(room1.introduce, ' ')
        self.assertEqual(room2.introduce, 'room2')

    def test_message(self):
        message1 = Message('message1', 1, '1')
        time.sleep(1)
        message2 = Message('message2', 1, '1')
        time.sleep(1)
        message3 = Message('message3', 2, '1')
        add_tool(message1, message2, message3)
        db.session.commit()
        print(message1.id)
        print(message3.id)
        print(message2.timestamp)
        print(message3.timestamp)
        self.assertEqual(message1.content, 'message1')
        self.assertEqual(message2.content, 'message2')
        self.assertEqual(message2.author_id, 1)
        self.assertEqual(message3.author_id, 2)

    def test_user_room(self):
        user1 = User('user1', '123456')
        user2 = User('user2', '123456')
        user3 = User('user3', '123456')
        room1 = Room('room1')
        room2 = Room('room2')
        add_tool(user1, user2, user3, room1, room2)
        db.session.commit()
        room1.users.append(user1)
        room1.users.append(user3)
        room2.users.append(user2)
        room2.users.append(user3)
        self.assertEqual(user1.rooms[0].name, 'room1')
        self.assertEqual(user2.rooms[0].name, 'room2')
        self.assertEqual(user3.rooms[0].name, 'room1')
        self.assertEqual(user3.rooms[1].name, 'room2')

    def test_user_message(self):
        user1 = User('user1', '123456')
        user2 = User('user2', '123456')
        message1 = Message('message1', 1, '1')
        message2 = Message('message2', 1, '1')
        message3 = Message('message3', 2, '1')
        user1.messages.append(message1)
        user2.messages.append(message2)
        user2.messages.append(message3)
        add_tool(user1, user2)
        db.session.commit()

        print(message2.author_id)
        self.assertEqual(message1.author.username, 'user1')
        self.assertEqual(message2.author.username, 'user2')
        self.assertEqual(message3.author.username, 'user2')
        db.session.delete(user2)
        db.session.commit()
        self.assertEqual(len(Message.query.all()), 1)

    def test_room_message(self):
        room1 = Room('room1')
        room2 = Room('room2')
        message1 = Message('message1', 1, '1')
        message2 = Message('message2', 1, '1')
        message3 = Message('message3', 2, '1')
        room1.messages.append(message1)
        room2.messages.append(message2)
        room2.messages.append(message3)
        add_tool(room1, room2)
        db.session.commit()

        print(message1.room_id)
        self.assertEqual(message1.room.name, 'room1')
        self.assertEqual(message2.room.name, 'room2')
        self.assertEqual(message3.room.name, 'room2')
        db.session.delete(room2)
        db.session.commit()
        self.assertEqual(len(Message.query.all()), 1)


if __name__ == '__main__':
    unittest.main()
