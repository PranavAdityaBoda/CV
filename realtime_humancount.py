def count_frame(frame):
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define the range of red color in HSV
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])
    
    # Threshold the HSV image to get only red colors
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    
    # Combine the two masks
    mask = cv2.bitwise_or(mask1, mask2)
    
    # Apply the mask to the original frame
    res = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Detect the person wearing a red shirt
    bounding_box, w = HOGCV.detectMultiScale(res, winStride=(4, 4), padding=(8, 8), scale=1.03)
    
    person = 0
    for x, y, w, h in bounding_box:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f'person {person}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        person += 1
    return frame