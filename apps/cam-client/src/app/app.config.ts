import { ApplicationConfig, importProvidersFrom, provideExperimentalZonelessChangeDetection } from "@angular/core";
import { provideRouter } from "@angular/router";
import { SocketIoConfig, SocketIoModule } from "ngx-socket-io";
import { appRoutes } from "./app.routes";

const config: SocketIoConfig = { url: "http://127.0.0.1:5000", options: {} };

export const appConfig: ApplicationConfig = {
    providers: [
        provideExperimentalZonelessChangeDetection(),
        provideRouter(appRoutes),
        importProvidersFrom(SocketIoModule.forRoot(config)),
    ],
};
