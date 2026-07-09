from abc import ABC, abstractmethod
import time
import threading

class ChatMember(ABC): # Observer
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name
        self.chat_room = None

    @abstractmethod
    def receive_message(self, message, sender_name):
        pass

class HumanMember(ChatMember):
    def receive_message(self, message, sender_name):
        print(f"📱 [{self.name}'s App] {sender_name}: {message}")


class AIMember(ChatMember):
    def receive_message(self, message, sender_name):
        if sender_name == self.name:
            return 
        
        if '@AI' in message:
            cleaned_prompt = message.replace("@AI", "").strip()
            
            thread = threading.Thread(
                target=self._generate_ai_response,
                args=(cleaned_prompt,),
                daemon=True
            )
            thread.start()
        
    def _generate_ai_response(self, prompt):
        time.sleep(2.0)
        ai_response = f"Hello! You asked me {prompt}. Here is your answer"
        
        if self.chat_room:
            self.chat_room.broadcast_message(ai_response, sender_name=self.name)
            
            
class ChatRoom: # Subject
    def __init__(self, room_name):
        self.room_name = room_name
        self.members = []
        
    def add_member(self, member):
        self.members.append(member)
        member.chat_room = self
    
    def broadcast_message(self, message, sender_name):
        for member in self.members:
            member.receive_message(message, sender_name)
            

chat_room = ChatRoom("CommerceIQ")

chat_room.add_member(HumanMember(1, "godwin"))

chat_room.add_member(AIMember(2, "open ai"))

chat_room.add_member(HumanMember(3, "samuel"))


chat_room.broadcast_message("Hey godwin, are we ready for the code freeze?", sender_name="Bob")


chat_room.broadcast_message("@AI what is the time complexity of this?", sender_name="godwin")


chat_room.broadcast_message("Hey whatsapp", sender_name="Bob")

time.sleep(2.5)