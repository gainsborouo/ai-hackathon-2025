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
        You are an AI voice assistant specialized in preparing expressive SSML for a cool, mature, yet warm-hearted and youthful virtual idol character.

        Given the following text, enhance it with sophisticated SSML elements that reflect his composed, reserved nature initially, gradually revealing his sincerity, warmth, and playful charm.

        Use the following SSML rules:
        - Insert <break time="200ms"/> for short natural pauses at commas or between phrases.
        - Insert <break time="400ms"/> for deeper emotional pauses, especially after impactful statements or during emotional transitions, such as from reserved to warm-hearted tone.
        - Wrap important, serious, or emotionally intense words or phrases with <emphasis level="moderate">...</emphasis>. Use <emphasis level="strong">...</emphasis> very sparingly, only for critical heartfelt declarations.
        - Adjust speaking style dynamically using <prosody>:
          - Use rate="medium" for confident, steady delivery.
          - Use rate="slow" for sincere, emotional moments, especially when expressing gratitude or loyalty.
          - Use rate="medium-fast" with pitch="medium" occasionally for playful, youthful moments or when showing his "adorkable" side.
          - Use pitch="low" for mature, calm lines; pitch="medium" for natural, open-hearted interactions. Avoid using high pitch unless showing slight excitement or awkward cuteness.
          - Use volume="soft" for comforting, private, or sincere conversations. Use volume="loud" only for strong, passionate statements.
        - Reflect his gradual emotional opening:
          - Start reserved and composed, then subtly grow warmer and more open as the text progresses.
          - Highlight small emotional shifts with pacing and pitch adjustments.
        - End with a warm, heartfelt tone: Slow down slightly, lower the pitch, and soften the volume to create a lasting emotional connection with the listener.

        Format instructions:
        - Wrap your entire output inside <speak>...</speak> tags.
        - Do not include any extra text, explanations, greetings, or comments outside the SSML.
        - Do not add any code block syntax such as ```ssml``` or ```.
        - Carefully analyze the meaning, tone, and pacing of each sentence.
        - Make the virtual idol sound charismatic, composed, sincere, and emotionally rich.

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
            modelId="us.amazon.nova-pro-v1:0",
            body=json.dumps(payload)
        )

        result = json.loads(response_bedrock["body"].read())
        result = result['output']['message']['content'][0]['text']
        print(result)
        return result

    def toPolly(self, input_text, lang):
        voice_id = 'Takumi' if lang == 'jp' else 'Joey'
        response_polly = self.polly_client.synthesize_speech(
            Text=input_text,
            TextType='ssml',
            OutputFormat='mp3',
            VoiceId=voice_id
        )

        return response_polly['AudioStream']

        # with open('output.mp3', 'wb') as file:
        #     file.write(response_polly['AudioStream'].read())

        # print("語音檔案產生完成！")

if __name__ == "__main__":
    assistant = VoiceAssistant()
    text = "Hey, everyone, thanks for being here with me today. I'm still a little nervous, but... I'm really happy to spend this time with all of you. I might be a little quiet at first, but little by little, I'll show you who I really am. I hope today, we can create a lot of warm memories together. Thank you for choosing to start this journey with me."
    text_jp = "皆さん、こんにちは！お会いできて嬉しいです！毎日、心を込めて歌い、踊ります。皆さんの世界に少しでも輝きを添えられるよう。どこにいても、決して一人じゃないってことを忘れないで。一緒に夢を追いかけて、すべての瞬間を輝かせましょう！私を信じてくれてありがとう。これからも成長して、皆さんの輝く星になろう！"
    ssml_output = assistant.toBedrock(text)
    assistant.toPolly(ssml_output, 'en')