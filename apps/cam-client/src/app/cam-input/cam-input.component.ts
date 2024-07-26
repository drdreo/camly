import { ChangeDetectionStrategy, Component } from "@angular/core";
import { CommonModule } from "@angular/common";

@Component({
    selector: "cam-input",
    standalone: true,
    imports: [CommonModule],
    templateUrl: "./cam-input.component.html",
    styleUrl: "./cam-input.component.scss",
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CamInputComponent {}
