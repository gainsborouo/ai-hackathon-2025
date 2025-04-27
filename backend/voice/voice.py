import boto3
import json
import os
from dotenv import load_dotenv
load_dotenv()

class VoiceAssistant:
    def __init__(self):
        self.access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        self.secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        
        # 初始化 Bedrock 客戶端
        self.bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-west-2",
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key
        )
        
        # 初始化 Polly 客戶端
        self.polly_client = boto3.Session(
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
            region_name="us-west-2"
        ).client('polly')

    def toBedrock(self, input_text):
        prompt = f"""
        You are an AI voice assistant specialized in preparing expressive SSML for a cool, mature virtual idol character.  
        Given the following text, enhance it with sophisticated SSML elements suitable for a confident and composed speaking style.

        Use the following SSML rules:
        - Insert <break time="200ms"/> for short natural pauses at commas or between phrases.
        - Insert <break time="400ms"/> for deeper emotional pauses, especially after impactful statements or to shift emotional tone.
        - Wrap important, serious, or emotionally intense words or phrases with <emphasis level="moderate">...</emphasis>.
        - Adjust speaking style dynamically using <prosody>:
          - Use rate="medium" for confident delivery.
          - Use rate="slow" for emotional, heartfelt lines.
          - Use pitch="low" or "medium" to reflect a calm, mature, and grounded tone.
          - Avoid using pitch="high" unless for very light, hopeful notes.
          - Use volume="soft" for comforting or intimate moments, and "loud" for dramatic emphasis only.
        - End with a warm, heartfelt tone to emotionally connect with the listener.

        Format instructions:
        - Wrap your entire output inside <speak>...</speak> tags.
        - Do not include any extra text, explanations, greetings, or comments outside the SSML.
        - Carefully analyze the meaning, tone, and pacing of each sentence.
        - Make the virtual idol sound charismatic, composed, and emotionally mature.

        Here is the text:

        {input_text}
        """

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }

        response_bedrock = self.bedrock_client.invoke_model(
            modelId="us.amazon.nova-lite-v1:0",
            body=json.dumps(payload)
        )

        result = json.loads(response_bedrock["body"].read())
        result = result['output']['message']['content'][0]['text']
        print(result)
        return result

    def toPolly(self, input_text):
        response_polly = self.polly_client.synthesize_speech(
            Text=input_text,
            TextType='ssml',
            OutputFormat='mp3',
            VoiceId='Joey'
        )

        with open('output.mp3', 'wb') as file:
            file.write(response_polly['AudioStream'].read())

        print("語音檔案產生完成！")

if __name__ == "__main__":
    assistant = VoiceAssistant()
    text = "Hi everyone! I'm so happy to see you here! Every day, I sing and dance with all my heart, just to bring a little more sparkle into your world. No matter where you are, remember — you're never alone. Let's chase our dreams together and make every moment shine bright! Thank you for believing in me. I'll keep growing to become your shining star!"
    ssml_output = assistant.toBedrock(text)
    assistant.toPolly(ssml_output)