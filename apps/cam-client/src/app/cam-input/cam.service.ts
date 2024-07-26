import { inject, Injectable } from "@angular/core";
import { Socket } from "ngx-socket-io";
import { filter, map, Observable, tap } from "rxjs";

@Injectable({ providedIn: "root" })
export class CamService {
    socket = inject(Socket);

    processedFrame(): Observable<string> {
        return this.socket.fromEvent<ArrayBuffer>("response_frame").pipe(
            filter((data) => !!data),
            tap(console.log),
            map((data: ArrayBuffer) => this.convertToFrame(data))
        );
    }
    private convertToFrame(data: ArrayBuffer): string {
        const bytes = new Uint8Array(data);
        const binaryString = Array.from(bytes)
            .map((byte) => String.fromCharCode(byte))
            .join("");
        return `data:image/jpeg;base64,${btoa(binaryString)}`;
    }

    recordedFrame(e: any) {
        this.sendFrame(e);
    }

    private sendFrame(frame: any) {
        this.socket.emit("frame", frame);
    }
}
