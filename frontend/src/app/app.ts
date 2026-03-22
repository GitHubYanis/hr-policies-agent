import { Component, signal, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  imports: [],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
  protected readonly backendMessage = signal('Loading backend status...');

  private readonly http = inject(HttpClient);

  constructor() {
    this.http.get<{ message: string }>('http://localhost:8000/').subscribe({
      next: (data) => this.backendMessage.set(data.message || 'No message'),
      error: (err) => this.backendMessage.set('Backend error: ' + (err?.message ?? err)),
    });
  }
}
