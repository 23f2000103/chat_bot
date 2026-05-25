import ollama

def generate_response(question):

    response = ollama.chat(
        model='qwen2.5:1.5b',
        messages=[
            {
                'role': 'user',
                'content': question
            }
        ]
    )

    return response['message']['content']