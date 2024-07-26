import { ChangeDetectionStrategy, Component, inject, viewChild } from "@angular/core";
import { CommonModule } from "@angular/common";
import { CamService } from "./cam.service";

const MEDIA_CONSTRAINTS = { video: true, audio: true };

@Component({
    selector: "cam-input",
    standalone: true,
    imports: [CommonModule],
    templateUrl: "./cam-input.component.html",
    styleUrl: "./cam-input.component.scss",
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CamInputComponent {
    camService = inject(CamService);
    processedFrame = this.camService.processedFrame();

    startRecording() {
        navigator.mediaDevices.getUserMedia(MEDIA_CONSTRAINTS).then((stream) => {
            const mediaRecorder = new MediaRecorder(stream, { mimeType: "video/mjpeg" });
            this.startMediaRecorderStream(mediaRecorder);
        });
    }

    startMediaRecorderStream(mediaRecorder: MediaRecorder) {
        mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) {
                const reader = new FileReader();
                reader.onload = () => {
                    const arrayBuffer = reader.result as ArrayBuffer;
                    this.camService.recordedFrame(arrayBuffer);
                };
                reader.readAsArrayBuffer(e.data);
            }
        };
        mediaRecorder.start(500); // Record in chunks of 500ms
        console.log("Recorder started");
    }

    startCanvasRecording() {
        navigator.mediaDevices
            .getUserMedia(MEDIA_CONSTRAINTS)
            .then((stream) => {
                const video = document.createElement("video");
                video.srcObject = stream;
                video.play();

                const canvas = document.createElement("canvas");
                const context = canvas.getContext("2d")!;

                setInterval(() => {
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);

                    canvas.toBlob((blob) => {
                        if (blob) {
                            const reader = new FileReader();
                            reader.onload = () => {
                                const arrayBuffer = reader.result as ArrayBuffer;
                                this.camService.recordedFrame(arrayBuffer);
                            };
                            reader.readAsArrayBuffer(blob);
                        }
                    }, "image/jpeg");
                }, 33); // Capture frame every 500ms
            })
            .catch((err) => console.error("Error accessing media devices.", err));
    }
}
