import cv2
import time
import os

def simulate_drone_stream(video_path, output_dir, frame_rate=1):
    """
    Simulates a drone video stream by saving frames as images.

    Args:
        video_path (str): Path to the input video file.
        output_dir (str): Directory to save the output images.
        frame_rate (int): Number of frames to process per second.
    """
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Save a frame every second
        if frame_count % (int(cap.get(cv2.CAP_PROP_FPS)) // frame_rate) == 0:
            image_path = f"{output_dir}/frame_{frame_count}.jpg"
            cv2.imwrite(image_path, frame)
            print(f"Saved frame: {image_path}")
            # Stop after the first frame for the PoC
            print("Stopping after one frame for PoC MVP.")
            break

        frame_count += 1
        time.sleep(1 / frame_rate)  # Pause to simulate real-time processing

    cap.release()
    print("Simulation complete.")

if __name__ == "__main__":
    # Ensure you have a sample video file in your project
    # simulate_drone_stream("../aerial_images/sample_video.mp4", "../aerial_images/")

    simulate_drone_stream("land_encroachment_poc/data/aerial_images/sample_video.mp4", "land_encroachment_poc/data/aerial_images")