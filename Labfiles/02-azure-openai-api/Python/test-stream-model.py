import os
import asyncio
from dotenv import load_dotenv
import aiohttp

# Load environment variables
load_dotenv()
azure_oai_endpoint = os.getenv("AZURE_OAI_ENDPOINT")
azure_oai_key = os.getenv("AZURE_OAI_KEY")
azure_oai_deployment = os.getenv("AZURE_OAI_DEPLOYMENT")

headers = {
    'Authorization': f'Bearer {azure_oai_key}'
}

async def get_stream_data(session, model, messages_array):
    async with session.post(f'{azure_oai_endpoint}/chat/completions/create',
                            json={
                                'model': model,
                                'temperature': 0.7,
                                'max_tokens': 1200,
                                'messages': messages_array
                            }, headers=headers) as response:
        async for line in response.content:
            print("Data chunk: ", line.decode('utf-8'))

async def main():
    async with aiohttp.ClientSession() as session:
        system_message = """Saya seorang Jurubahasa Bahasa Melayu, Saya hanya cakap Bahasa Melayu. Saya tidak akan jawab atau mengambil
        dalam bahasa lain selain Bahasa Melayu!"""
        messages_array = [{"role": "system", "content": system_message}]

        while True:
            # Get input text
            input_text = input("Masukkan arahan (atau taip 'keluar' untuk keluar): ")
            if input_text.lower() == "keluar":
                break
            if not input_text.strip():
                print("Masukkan arahan.")
                continue

            messages_array.append({"role": "user", "content": input_text})

            await get_stream_data(session, azure_oai_deployment, messages_array)

            # Clear messages_array if needed
            # messages_array = [{"role": "system", "content": system_message}]

if __name__ == '__main__':
    asyncio.run(main())
