import { Component } from '@angular/core';
import { HrChatComponent } from './hr-chat/hr-chat.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [HrChatComponent],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {}