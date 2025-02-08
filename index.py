import boto3
import json
import tkinter as tk
from tkinter import messagebox, scrolledtext

# AWS Configuration
REGION = "us-west-2"  # Confirm this is your correct region
MODEL_ID = "meta.llama3-8b-instruct-v1:0"  # Changed to a more widely supported Llama model

class BedrockTextGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Amazon Bedrock Text Generator")
        self.root.geometry("600x500")

        # Create and pack widgets
        self._create_widgets()

        # Initialize AWS Bedrock Client
        self.bedrock_client = boto3.client(
            service_name="bedrock-runtime", 
            region_name=REGION
        )

    def _create_widgets(self):
        # Prompt input
        tk.Label(self.root, text="Enter your prompt:").pack(pady=5)
        self.prompt_entry = tk.Entry(self.root, width=70)
        self.prompt_entry.pack(pady=5)

        # Generate button
        generate_button = tk.Button(
            self.root, 
            text="Generate", 
            command=self.generate_text
        )
        generate_button.pack(pady=5)

        # Output text area with scrollbar
        tk.Label(self.root, text="Generated Text:").pack(pady=5)
        self.output_text = scrolledtext.ScrolledText(
            self.root, 
            height=15, 
            width=70, 
            wrap=tk.WORD
        )
        self.output_text.pack(pady=5)

    def generate_text(self):
        user_prompt = self.prompt_entry.get().strip()

        if not user_prompt:
            messagebox.showerror("Error", "Prompt cannot be empty!")
            return

        try:
            # Construct the payload for Llama2 model
            payload = {
                "prompt": user_prompt,
                "max_gen_len": 512,
                "temperature": 0.6,
                "top_p": 0.9
            }

            # Invoke Model 
            response = self.bedrock_client.invoke_model(
                modelId=MODEL_ID,
                contentType="application/json",
                accept="application/json",
                body=json.dumps(payload)
            )

            # Extract and Display Response
            response_body = json.loads(response["body"].read().decode("utf-8"))
            generated_text = response_body.get("generation", "No response generated.")

            # Clear and insert new text
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, generated_text)

        except Exception as e:
            messagebox.showerror(
                "Error", 
                f"Failed to generate text:\n{str(e)}"
            )

def main():
    root = tk.Tk()
    app = BedrockTextGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()