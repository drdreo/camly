import cv2

from flask import current_app as app

# Minimum boxed area for a detected motion to count as actual motion
MIN_MOVEMENT_AREA = 500

def generate_frames(app, streaming):
    cap = cv2.VideoCapture(0)  # Use 0 for the default webcam
    fgbg = cv2.createBackgroundSubtractorMOG2()
    
    while True:
        if streaming:
            success, frame = cap.read()
            if not success:
                app.logger.error('no success - %s', success)
                break
            
            # Apply background subtraction
            fgmask = fgbg.apply(frame)
            contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            movement_detected = False
            for contour in contours:
                if cv2.contourArea(contour) > MIN_MOVEMENT_AREA:
                    movement_detected = True
                    # cv2.drawContours(frame, [contour], -1, (0, 0, 255), 2)  # Red color, thickness 2
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                
            app.logger.info("Movement detected" if movement_detected else "No movement detected")

            # Encode the frame to JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            cap.release() 
            cv2.destroyAllWindows() 
            # If paused, send a blank frame
            #yield (b'--frame\r\n'
            #       b'Content-Type: image/jpeg\r\n\r\n' + b'\r\n')