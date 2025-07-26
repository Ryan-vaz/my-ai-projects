import os
from datetime import datetime

# --- Default Settings --- #
DEFAULT_STYLE = "Photorealistic"
DEFAULT_CAMERA = "DSLR"
DEFAULT_ASPECT_RATIO = "16:9"
DEFAULT_QUALITY = "High"

# --- Session Variables --- #
session_character = ""
session_style = DEFAULT_STYLE
session_camera = DEFAULT_CAMERA
session_aspect = DEFAULT_ASPECT_RATIO
session_quality = DEFAULT_QUALITY

# --- Helper Functions --- #

def get_input(prompt, default=None):
    user_input = input(f"{prompt} [{default}]: ").strip()
    return user_input if user_input else default


def build_prompt(character, scene, style, camera, aspect, quality):
    prompt = f"{character}, {scene}, {style} style, shot on {camera}, aspect ratio {aspect}, {quality} quality"
    return prompt


def save_prompt(prompt_text):
    folder = "prompts"
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder, f"prompt_{timestamp}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(prompt_text)
    print(f"\n✅ Prompt saved to {filename}\n")


# --- Main Flow --- #

def main():
    global session_character, session_style, session_camera, session_aspect, session_quality

    print("\n==============================")
    print(" AI Image Prompt Builder CLI ")
    print("==============================\n")

    # 1. Set up character
    session_character = input("Describe your main character (one-time setup): ").strip()

    # 2. (Optional) Customize style/settings
    if input("\nWould you like to customize settings? (y/n): ").lower() == 'y':
        session_style = get_input("Enter style", DEFAULT_STYLE)
        session_camera = get_input("Enter camera type", DEFAULT_CAMERA)
        session_aspect = get_input("Enter aspect ratio", DEFAULT_ASPECT_RATIO)
        session_quality = get_input("Enter quality", DEFAULT_QUALITY)

    # 3. Loop for creating prompts
    while True:
        print("\n--- New Scene ---")
        scene = input("Describe the scene or action: ").strip()

        final_prompt = build_prompt(
            session_character,
            scene,
            session_style,
            session_camera,
            session_aspect,
            session_quality
        )

        print("\nGenerated Prompt:\n")
        print(final_prompt)

        save_prompt(final_prompt)

        cont = input("\nDo you want to create another prompt? (y/n): ").lower()
        if cont != 'y':
            break

    print("\n🎉 All done! Happy generating!")


if __name__ == "__main__":
    main()
