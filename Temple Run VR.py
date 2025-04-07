import cv2
import mediapipe as mp
import pyautogui
import time

# Set up pose detection
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(confidence_thresholds=[0.5, 0.5])
camera = cv2.VideoCapture(0)

# Game control settings
JUMP_LINE_HEIGHT = 0.4  # Top line for jumping
SLIDE_LINE_HEIGHT = 0.6  # Bottom line for sliding
MOVE_SENSITIVITY = 50    # How much you need to lean to turn
JUMP_DELAY = 0.5         # Prevents jump spamming
SLIDE_DELAY = 0.5        # Prevents slide spamming

# Track when we last jumped or slid
last_jump = 0
last_slide = 0

# For adjusting lines with mouse
adjusting_jump_line = False
adjusting_slide_line = False

# Make a big window for better visibility
cv2.namedWindow('Game Controller', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Game Controller', 1280, 720)

def handle_mouse_click(event, x, y, flags, params):
    global JUMP_LINE_HEIGHT, SLIDE_LINE_HEIGHT
    global adjusting_jump_line, adjusting_slide_line
    
    screen_height = params['screen_height']
    
    # Check if we clicked near either control line
    if event == cv2.EVENT_LBUTTONDOWN:
        if abs(y - int(screen_height * JUMP_LINE_HEIGHT)) < 20:
            adjusting_jump_line = True
        elif abs(y - int(screen_height * SLIDE_LINE_HEIGHT)) < 20:
            adjusting_slide_line = True
            
    # Move the line we're dragging
    elif event == cv2.EVENT_MOUSEMOVE:
        if adjusting_jump_line:
            JUMP_LINE_HEIGHT = max(0.1, min(0.9, y / screen_height))
        elif adjusting_slide_line:
            SLIDE_LINE_HEIGHT = max(0.1, min(0.9, y / screen_height))
            
    # Stop dragging when mouse button released
    elif event == cv2.EVENT_LBUTTONUP:
        adjusting_jump_line = False
        adjusting_slide_line = False

# Connect the mouse to our click handler
cv2.setMouseCallback('Game Controller', handle_mouse_click, {'screen_height': 720})

while camera.isOpened():
    success, video_frame = camera.read()
    if not success:
        break
    
    # Flip the image so movements feel natural
    video_frame = cv2.flip(video_frame, 1)
    height, width, _ = video_frame.shape
    
    # Update screen height for mouse tracking
    cv2.setMouseCallback('Game Controller', handle_mouse_click, {'screen_height': height})
    
    # Calculate where to draw the control lines
    jump_line = int(height * JUMP_LINE_HEIGHT)
    slide_line = int(height * SLIDE_LINE_HEIGHT)
    
    # Make the line we're adjusting thicker
    jump_line_width = 5 if adjusting_jump_line else 3
    slide_line_width = 5 if adjusting_slide_line else 3
    
    # Draw the control lines
    cv2.line(video_frame, (0, jump_line), (width, jump_line), 
             (0, 255, 255), jump_line_width)  # Yellow jump line
    cv2.line(video_frame, (0, slide_line), (width, slide_line), 
             (0, 0, 255), slide_line_width)   # Red slide line
    cv2.line(video_frame, (width//2, 0), (width//2, height), 
             (0, 255, 0), 2)                  # Center guide
    
    # Add handles to the control lines
    cv2.circle(video_frame, (50, jump_line), 8, (0, 255, 255), -1)
    cv2.circle(video_frame, (width-50, jump_line), 8, (0, 255, 255), -1)
    cv2.circle(video_frame, (50, slide_line), 8, (0, 0, 255), -1)
    cv2.circle(video_frame, (width-50, slide_line), 8, (0, 0, 255), -1)
    
    # Detect body position
    frame_rgb = cv2.cvtColor(video_frame, cv2.COLOR_BGR2RGB)
    pose_results = pose.process(frame_rgb)
    
    if pose_results.pose_landmarks:
        body_points = pose_results.pose_landmarks.landmark
        nose = body_points[mp_pose.PoseLandmark.NOSE]
        nose_y = int(nose.y * height)
        nose_x = int(nose.x * width)
        
        # Show where your nose is
        cv2.circle(video_frame, (nose_x, nose_y), 15, (255, 0, 255), -1)
        
        # Only control game when not adjusting lines
        if not (adjusting_jump_line or adjusting_slide_line):
            # Jump when nose crosses top line
            if nose_y < jump_line and (time.time() - last_jump > JUMP_DELAY):
                pyautogui.press('up')
                last_jump = time.time()
                cv2.putText(video_frame, "JUMP!", (width//2-100, 100), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            
            # Slide when nose crosses bottom line
            elif nose_y > slide_line and (time.time() - last_slide > SLIDE_DELAY):
                pyautogui.press('down')
                last_slide = time.time()
                cv2.putText(video_frame, "SLIDE!", (width//2-100, slide_line+50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
            
            # Steer left or right
            if nose_x < width//2 - MOVE_SENSITIVITY:
                pyautogui.press('left')
                cv2.putText(video_frame, "<-- LEFT", (100, height//2), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif nose_x > width//2 + MOVE_SENSITIVITY:
                pyautogui.press('right')
                cv2.putText(video_frame, "RIGHT -->", (width-300, height//2), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Show instructions
    cv2.putText(video_frame, "JUMP: Nose above yellow", (50, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(video_frame, "SLIDE: Nose below red", (50, 70), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    cv2.putText(video_frame, "MOVE: Lean left/right", (50, 110), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(video_frame, "ADJUST: Drag the lines", (50, 150), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    
    # Show the camera view
    cv2.imshow('Game Controller', video_frame)
    
    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
camera.release()
cv2.destroyAllWindows()